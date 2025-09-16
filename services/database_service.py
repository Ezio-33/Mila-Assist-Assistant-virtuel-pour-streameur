#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service de base de données pour Mila Assist
Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import pymysql
import logging
import json
from datetime import datetime
from typing import Optional, Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service de gestion de la base de données française"""
    
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.vectorizer = None
        self.question_vectors = None
        self.cached_questions = []
        
        # Configuration de la base de données à partir des variables d'environnement
        self.db_config = {
            'host': getattr(self.config, 'MYSQL_HOST', 'localhost'),
            'user': getattr(self.config, 'MYSQL_USER', 'chatbot_user'),
            'password': getattr(self.config, 'MYSQL_PASSWORD', 'motdepasse_securise'),
            'database': getattr(self.config, 'MYSQL_DATABASE', 'mila_assist_db'),
            'charset': 'utf8mb4',
            'port': int(getattr(self.config, 'MYSQL_PORT', 3306)),
            'autocommit': True
        }
        
        self._init_connection()
        self._init_vectorizer()
    
    def _init_connection(self):
        """Initialise la connexion à la base de données"""
        try:
            self.connection = pymysql.connect(**self.db_config)
            logger.info("✅ Connexion à la base de données MySQL établie")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur de connexion à la base de données : {e}")
            return False
    
    def _init_vectorizer(self):
        """Initialise le vectoriseur TF-IDF avec les données de la base"""
        try:
            questions = self.get_all_questions()
            if questions:
                self.vectorizer = TfidfVectorizer(max_features=1000, stop_words=None)
                self.question_vectors = self.vectorizer.fit_transform(questions)
                self.cached_questions = questions
                logger.info(f"📊 Vectoriseur initialisé avec {len(questions)} questions")
            else:
                logger.warning("⚠️ Aucune question trouvée pour initialiser le vectoriseur")
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation du vectoriseur : {e}")
    
    def reconnect(self):
        """Reconnecte à la base de données si nécessaire"""
        try:
            if self.connection:
                self.connection.ping(reconnect=True)
            else:
                self._init_connection()
        except Exception as e:
            logger.error(f"Erreur de reconnexion : {e}")
            self._init_connection()
    
    def get_all_questions(self) -> List[str]:
        """Récupère toutes les questions de la base de connaissances"""
        try:
            self.reconnect()
            with self.connection.cursor() as cursor:
                # Utiliser les nouveaux noms de tables françaises
                cursor.execute("SELECT question FROM base_connaissances WHERE question IS NOT NULL")
                results = cursor.fetchall()
                return [row[0] for row in results if row[0]]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des questions : {e}")
            return []
    
    def get_best_response(self, user_question: str, threshold: float = 0.3) -> Optional[Dict]:
        """Trouve la meilleure réponse pour une question utilisateur"""
        try:
            if not self.vectorizer or not self.question_vectors.any():
                logger.warning("Vectoriseur non initialisé, recherche directe en base")
                return self._get_direct_response(user_question)
            
            # Vectorisation de la question utilisateur
            user_vector = self.vectorizer.transform([user_question])
            
            # Calcul de similarité cosinus
            similarities = cosine_similarity(user_vector, self.question_vectors).flatten()
            
            # Trouve la meilleure correspondance
            best_match_index = np.argmax(similarities)
            best_similarity = similarities[best_match_index]
            
            if best_similarity >= threshold:
                # Récupère les détails de la réponse depuis la base
                return self._get_response_details(self.cached_questions[best_match_index], best_similarity)
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche de réponse : {e}")
            return self._get_direct_response(user_question)
    
    def _get_direct_response(self, user_question: str) -> Optional[Dict]:
        """Recherche directe dans la base sans vectorisation"""
        try:
            self.reconnect()
            with self.connection.cursor() as cursor:
                # Recherche par correspondance partielle
                query = """
                SELECT id, etiquette, question, reponse, nombre_utilisations 
                FROM base_connaissances 
                WHERE question LIKE %s 
                ORDER BY nombre_utilisations DESC 
                LIMIT 1
                """
                cursor.execute(query, (f"%{user_question}%",))
                result = cursor.fetchone()
                
                if result:
                    return {
                        'id': result[0],
                        'tag': result[1],
                        'question': result[2],
                        'response': result[3],
                        'similarity': 0.5,  # Score arbitraire pour recherche directe
                        'usage_count': result[4]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la recherche directe : {e}")
            return None
    
    def _get_response_details(self, matched_question: str, similarity: float) -> Optional[Dict]:
        """Récupère les détails complets d'une réponse"""
        try:
            self.reconnect()
            with self.connection.cursor() as cursor:
                query = """
                SELECT id, etiquette, question, reponse, nombre_utilisations 
                FROM base_connaissances 
                WHERE question = %s
                """
                cursor.execute(query, (matched_question,))
                result = cursor.fetchone()
                
                if result:
                    # Incrémenter le compteur d'utilisation
                    self._increment_usage_count(result[0])
                    
                    return {
                        'id': result[0],
                        'tag': result[1],
                        'question': result[2],
                        'response': result[3],
                        'similarity': similarity,
                        'usage_count': result[4]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des détails : {e}")
            return None
    
    def _increment_usage_count(self, knowledge_id: int):
        """Incrémente le compteur d'utilisation d'une entrée"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE base_connaissances SET nombre_utilisations = nombre_utilisations + 1 WHERE id = %s",
                    (knowledge_id,)
                )
        except Exception as e:
            logger.error(f"Erreur lors de l'incrémentation du compteur : {e}")
    
    def log_conversation(self, session_id: str, question: str, reponse: str, 
                        id_connaissance: Optional[int] = None, score_confiance: Optional[float] = None,
                        temps_reponse_ms: Optional[float] = None) -> bool:
        """Enregistre une conversation dans le journal"""
        try:
            self.reconnect()
            with self.connection.cursor() as cursor:
                query = """
                INSERT INTO journal_conversation 
                (id_session, question, reponse, id_connaissance, score_confiance, temps_reponse_ms)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (session_id, question, reponse, id_connaissance, score_confiance, temps_reponse_ms))
                
                # Mettre à jour les statistiques de session
                self._update_session_stats(session_id, score_confiance, temps_reponse_ms)
                
                logger.info(f"📝 Conversation enregistrée - Session: {session_id}")
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement de la conversation : {e}")
            return False
    
    def _update_session_stats(self, session_id: str, score_confiance: Optional[float], temps_reponse_ms: Optional[float]):
        """Met à jour les statistiques de session"""
        try:
            with self.connection.cursor() as cursor:
                # Vérifier si la session existe
                cursor.execute("SELECT id FROM sessions WHERE session_id = %s", (session_id,))
                session_exists = cursor.fetchone()
                
                if not session_exists:
                    # Créer une nouvelle session
                    cursor.execute(
                        "INSERT INTO sessions (session_id, nombre_questions, score_moyen, temps_reponse_moyen_ms) VALUES (%s, 1, %s, %s)",
                        (session_id, score_confiance or 0.0, temps_reponse_ms or 0.0)
                    )
                else:
                    # Mettre à jour les statistiques existantes
                    cursor.execute("""
                        UPDATE sessions 
                        SET nombre_questions = nombre_questions + 1,
                            score_moyen = (
                                SELECT AVG(score_confiance) 
                                FROM journal_conversation 
                                WHERE id_session = %s AND score_confiance IS NOT NULL
                            ),
                            temps_reponse_moyen_ms = (
                                SELECT AVG(temps_reponse_ms) 
                                FROM journal_conversation 
                                WHERE id_session = %s AND temps_reponse_ms IS NOT NULL
                            )
                        WHERE session_id = %s
                    """, (session_id, session_id, session_id))
                    
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des stats de session : {e}")
    
    def save_feedback(self, question: str, reponse_attendue: str, reponse_donnee: str = None) -> bool:
        """Sauvegarde un feedback utilisateur"""
        try:
            self.reconnect()
            with self.connection.cursor() as cursor:
                query = """
                INSERT INTO retours_utilisateur 
                (question, reponse_attendue, reponse_donnee, statut, priorite)
                VALUES (%s, %s, %s, 'nouveau', 'moyenne')
                """
                cursor.execute(query, (question, reponse_attendue, reponse_donnee))
                logger.info("📝 Feedback utilisateur enregistré")
                return True
                
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement du feedback : {e}")
            return False
    
    def get_session_stats(self, session_id: str) -> Optional[Dict]:
        """Récupère les statistiques d'une session"""
        try:
            self.reconnect()
            with self.connection.cursor() as cursor:
                query = """
                SELECT nombre_questions, score_moyen, temps_reponse_moyen_ms, date_creation
                FROM sessions 
                WHERE session_id = %s
                """
                cursor.execute(query, (session_id,))
                result = cursor.fetchone()
                
                if result:
                    return {
                        'nombre_questions': result[0],
                        'score_moyen': result[1],
                        'temps_reponse_moyen_ms': result[2],
                        'date_creation': result[3]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats de session : {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test de la connexion à la base de données"""
        try:
            self.reconnect()
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except Exception as e:
            logger.error(f"Test de connexion échoué : {e}")
            return False
    
    def close(self):
        """Ferme la connexion à la base de données"""
        try:
            if self.connection:
                self.connection.close()
                logger.info("🔒 Connexion à la base de données fermée")
        except Exception as e:
            logger.error(f"Erreur lors de la fermeture de la connexion : {e}")