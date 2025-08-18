"""
Gestion de la base de données pour le chatbot avec recherche vectorielle
Système RAG (Retrieval-Augmented Generation) avec SQLite/MySQL
Compatible avec l'architecture existante (intents.json)
Version simplifiée utilisant TF-IDF au lieu de sentence-transformers
"""

import os
import json
import sqlite3
import numpy as np
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import pickle

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base SQLAlchemy
Base = declarative_base()

# Configuration de la base de données
class DatabaseConfig:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' ou 'mysql'
        self.SQLITE_PATH = os.path.join(self.BASE_DIR, 'chatbot_knowledge.db')
        
        # Configuration MySQL (pour déploiement externe)
        self.MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
        self.MYSQL_USER = os.getenv('MYSQL_USER', 'chatbot_user')
        self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'secure_password')
        self.MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'chatbot_db')

# Modèles de base de données
class KnowledgeBase(Base):
    """Table principale pour stocker les questions/réponses avec embeddings"""
    __tablename__ = 'knowledge_base'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(100), nullable=False)  # Catégorie/intention
    question = Column(Text, nullable=False)    # Question/pattern
    response = Column(Text, nullable=False)    # Réponse
    embedding = Column(Text, nullable=True)    # Embedding vectoriel sérialisé
    confidence_threshold = Column(Float, default=0.7)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    usage_count = Column(Integer, default=0)  # Compteur d'utilisation
    extra_data = Column(Text, nullable=True)    # Métadonnées additionnelles (JSON string)

class ConversationLog(Base):
    """Table pour les logs de conversation (optionnel pour analyse)"""
    __tablename__ = 'conversation_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False)
    user_input = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    matched_kb_id = Column(Integer, nullable=True)
    confidence_score = Column(Float, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class UserFeedback(Base):
    """Table pour les feedbacks utilisateurs"""
    __tablename__ = 'user_feedback'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    expected_response = Column(Text, nullable=False)
    current_response = Column(Text, nullable=True)
    is_processed = Column(Integer, default=0)  # 0 = non traité, 1 = traité
    created_at = Column(DateTime, default=datetime.now)

class ChatbotDatabase:
    """Classe principale pour gérer la base de données du chatbot"""
    
    def __init__(self, config: DatabaseConfig = None):
        self.config = config or DatabaseConfig()
        self.engine = None
        self.Session = None
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words=None)
        self.question_vectors = None
        self.questions_cache = []
        self._init_database()
    
    def _init_database(self):
        """Initialise la connexion à la base de données"""
        try:
            if self.config.DB_TYPE == 'sqlite':
                database_url = f"sqlite:///{self.config.SQLITE_PATH}"
            else:
                database_url = (f"mysql+pymysql://{self.config.MYSQL_USER}:"
                              f"{self.config.MYSQL_PASSWORD}@{self.config.MYSQL_HOST}/"
                              f"{self.config.MYSQL_DATABASE}")
            
            self.engine = create_engine(database_url, echo=False)
            self.Session = sessionmaker(bind=self.engine)
            
            # Création des tables
            Base.metadata.create_all(self.engine)
            logger.info(f"Base de données initialisée ({self.config.DB_TYPE})")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
            raise
    
    def migrate_from_intents_json(self, intents_path: str = None) -> bool:
        """Migre les données depuis intents.json vers la base de données"""
        try:
            if intents_path is None:
                intents_path = os.path.join(self.config.BASE_DIR, 'intents.json')
            
            if not os.path.exists(intents_path):
                logger.warning(f"Fichier intents.json non trouvé: {intents_path}")
                return False
            
            with open(intents_path, 'r', encoding='utf-8') as f:
                intents_data = json.load(f)
            
            session = self.Session()
            migrated_count = 0
            
            for intent in intents_data['intents']:
                tag = intent['tag']
                responses = intent['responses']
                
                for pattern in intent['patterns']:
                    for response in responses:
                        # Vérifier si l'entrée existe déjà
                        existing = session.query(KnowledgeBase).filter_by(
                            tag=tag, 
                            question=pattern, 
                            response=response
                        ).first()
                        
                        if not existing:
                            # Créer l'entrée sans embedding pour l'instant
                            kb_entry = KnowledgeBase(
                                tag=tag,
                                question=pattern,
                                response=response,
                                embedding="",  # Sera calculé lors de la mise à jour du cache
                                extra_data=json.dumps({'source': 'intents.json'})
                            )
                            session.add(kb_entry)
                            migrated_count += 1
            
            session.commit()
            session.close()
            
            # Mettre à jour le cache vectoriel
            self._update_vector_cache()
            
            logger.info(f"Migration terminée: {migrated_count} entrées ajoutées")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la migration: {e}")
            return False
    
    def _update_vector_cache(self):
        """Met à jour le cache des vecteurs TF-IDF"""
        try:
            session = self.Session()
            all_entries = session.query(KnowledgeBase).all()
            
            if not all_entries:
                session.close()
                return
            
            questions = [entry.question for entry in all_entries]
            self.questions_cache = all_entries
            
            # Créer les vecteurs TF-IDF
            self.question_vectors = self.vectorizer.fit_transform(questions)
            session.close()
            
            logger.info(f"Cache vectoriel mis à jour: {len(questions)} questions")
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du cache: {e}")

    def search_similar_questions(self, query: str, top_k: int = 5, threshold: float = 0.1) -> List[Dict]:
        """Recherche les questions similaires avec TF-IDF + similarité cosinus"""
        try:
            if self.question_vectors is None or not self.questions_cache:
                logger.warning("Cache vectoriel non initialisé")
                return []
            
            # Vectoriser la requête
            query_vector = self.vectorizer.transform([query])
            
            # Calculer la similarité cosinus avec toutes les questions
            similarities = cosine_similarity(query_vector, self.question_vectors)[0]
            
            # Filtrer et trier les résultats
            results = []
            for i, similarity in enumerate(similarities):
                if similarity >= threshold:
                    entry = self.questions_cache[i]
                    results.append({
                        'id': entry.id,
                        'tag': entry.tag,
                        'question': entry.question,
                        'response': entry.response,
                        'similarity': float(similarity),
                        'usage_count': entry.usage_count
                    })
            
            # Trier par similarité décroissante
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {e}")
            return []
    
    def get_best_response(self, query: str, threshold: float = 0.1, mode: str = "balanced") -> Optional[Dict]:
        """Obtient la meilleure réponse pour une requête donnée avec amélioration selon le mode"""
        similar_questions = self.search_similar_questions(query, top_k=1, threshold=threshold)
        
        if similar_questions:
            best_match = similar_questions[0]
            
            # Amélioration de la réponse selon le mode choisi
            try:
                from response_modes import create_response_system
                response_system = create_response_system(mode)
                enhanced_result = response_system.get_enhanced_response(
                    best_match['response'], 
                    query, 
                    best_match['similarity']
                )
                
                # Mise à jour de la réponse avec la version améliorée
                best_match['response'] = enhanced_result['response']
                best_match['original_response'] = enhanced_result['original_response']
                best_match['enhancement_mode'] = enhanced_result['mode']
                best_match['question_type'] = enhanced_result['question_type']
                best_match['enhancement_applied'] = enhanced_result['enhancement_applied']
                
            except Exception as e:
                logger.warning(f"Erreur lors de l'amélioration de la réponse: {e}")
                # Garde la réponse originale en cas d'erreur
            
            # Incrémenter le compteur d'utilisation
            self._increment_usage_count(best_match['id'])
            return best_match
        
        return None
    
    def _increment_usage_count(self, kb_id: int):
        """Incrémente le compteur d'utilisation d'une entrée"""
        try:
            session = self.Session()
            entry = session.query(KnowledgeBase).filter_by(id=kb_id).first()
            if entry:
                entry.usage_count += 1
                session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Erreur lors de l'incrémentation du compteur: {e}")
    
    def add_knowledge(self, tag: str, question: str, response: str, metadata: Dict = None) -> bool:
        """Ajoute une nouvelle connaissance à la base"""
        try:
            session = self.Session()
            
            kb_entry = KnowledgeBase(
                tag=tag,
                question=question,
                response=response,
                embedding="",  # Sera mis à jour dans le cache
                extra_data=json.dumps(metadata or {})
            )
            
            session.add(kb_entry)
            session.commit()
            session.close()
            
            # Mettre à jour le cache vectoriel
            self._update_vector_cache()
            
            logger.info(f"Nouvelle connaissance ajoutée: {tag} - {question[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de connaissance: {e}")
            return False
    
    def save_feedback(self, question: str, expected_response: str, current_response: str = None) -> bool:
        """Sauvegarde un feedback utilisateur"""
        try:
            session = self.Session()
            
            feedback = UserFeedback(
                question=question,
                expected_response=expected_response,
                current_response=current_response
            )
            
            session.add(feedback)
            session.commit()
            session.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du feedback: {e}")
            return False
    
    def process_pending_feedbacks(self) -> bool:
        """Traite les feedbacks en attente et met à jour la base de connaissances"""
        try:
            session = self.Session()
            pending_feedbacks = session.query(UserFeedback).filter_by(is_processed=0).all()
            
            processed_count = 0
            for feedback in pending_feedbacks:
                # Rechercher des questions similaires
                similar = self.search_similar_questions(feedback.question, threshold=0.5)
                
                if similar:
                    # Mettre à jour une entrée existante si très similaire
                    kb_id = similar[0]['id']
                    kb_entry = session.query(KnowledgeBase).filter_by(id=kb_id).first()
                    if kb_entry and feedback.expected_response not in kb_entry.response:
                        kb_entry.response = feedback.expected_response
                        kb_entry.updated_at = datetime.now()
                else:
                    # Créer une nouvelle entrée (sans appeler add_knowledge pour éviter les conflits)
                    tag = f"feedback_{datetime.now().strftime('%Y%m%d')}"
                    new_entry = KnowledgeBase(
                        tag=tag,
                        question=feedback.question,
                        response=feedback.expected_response,
                        embedding="",
                        extra_data=json.dumps({'source': 'user_feedback'})
                    )
                    session.add(new_entry)
                
                feedback.is_processed = 1
                processed_count += 1
            
            session.commit()
            session.close()
            
            logger.info(f"Feedbacks traités: {processed_count}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement des feedbacks: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Retourne des statistiques sur la base de connaissances"""
        try:
            session = self.Session()
            
            total_entries = session.query(KnowledgeBase).count()
            total_feedbacks = session.query(UserFeedback).count()
            pending_feedbacks = session.query(UserFeedback).filter_by(is_processed=0).count()
            
            # Top tags
            tags_query = session.query(KnowledgeBase.tag).all()
            tags_count = {}
            for tag_tuple in tags_query:
                tag = tag_tuple[0]
                tags_count[tag] = tags_count.get(tag, 0) + 1
            
            session.close()
            
            return {
                'total_entries': total_entries,
                'total_feedbacks': total_feedbacks,
                'pending_feedbacks': pending_feedbacks,
                'top_tags': sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10],
                'vectorizer_features': getattr(self.vectorizer, 'vocabulary_', None) and len(self.vectorizer.vocabulary_) or 0
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des stats: {e}")
            return {}

# Fonctions utilitaires pour la compatibilité avec l'existant
def init_database(migrate_intents: bool = True) -> ChatbotDatabase:
    """Initialise la base de données et migre les données si nécessaire"""
    config = DatabaseConfig()
    db = ChatbotDatabase(config)
    
    if migrate_intents:
        intents_path = os.path.join(config.BASE_DIR, 'intents.json')
        if os.path.exists(intents_path):
            db.migrate_from_intents_json(intents_path)
    
    return db

if __name__ == "__main__":
    # Test de la base de données
    print("Initialisation de la base de données...")
    db = init_database()
    
    print("Statistiques:", db.get_stats())
    
    # Test de recherche
    test_query = "Bonjour"
    results = db.search_similar_questions(test_query)
    print(f"Résultats pour '{test_query}':", results)
