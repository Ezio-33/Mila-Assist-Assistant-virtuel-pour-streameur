#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVICE CHATBOT PRINCIPAL - VERSION RNCP-6
=====================================================

Service principal du chatbot Mila Assist avec chargement asynchrone du modèle Keras
REFORMULATION DÉSACTIVÉE - Les réponses sont retournées directement

Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import time
import requests
import os
import random
import pickle
import json
import numpy as np
import re
import threading
from typing import Optional, Dict, Any, List, Tuple
import logging
from datetime import datetime
from enum import Enum
from .api_client import ApiClient

# Import conditionnel de TensorFlow
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TENSORFLOW_AVAILABLE = True
    logger_tf = logging.getLogger(__name__)
    logger_tf.info("✅ TensorFlow disponible pour le fallback Keras")
except ImportError:
    TENSORFLOW_AVAILABLE = False
    load_model = None
    logger_tf = logging.getLogger(__name__)
    logger_tf.warning("⚠️ TensorFlow non disponible - fallback Keras désactivé")

# Import conditionnel de NLTK
try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    class WordNetLemmatizer:
        def lemmatize(self, word, pos='n'):
            return word.lower()
    
    def word_tokenize(text, language='french'):
        return text.split()

logger = logging.getLogger(__name__)

class ModelStatus(Enum):
    """États du modèle Keras"""
    NOT_INITIALIZED = "not_initialized"
    LOADING = "loading"
    READY = "ready"
    ERROR = "error"
    DISABLED = "disabled"

class ChatbotService:
    """Service principal du chatbot - VERSION SANS REFORMULATION"""
    
    def __init__(self, config):
        self.config = config
        # REFORMULATION DÉSACTIVÉE - Mode fixé sur minimal (pas de reformulation)
        self.current_mode = "minimal"
        
        # État du modèle Keras
        self.model_status = ModelStatus.NOT_INITIALIZED
        self.model_loading_thread = None
        self.model_error_message = None
        
        # Initialiser le client API
        self.api_client = ApiClient(config)
        
        # Variables pour le modèle Keras local (fallback)
        self.model = None
        self.words = None
        self.classes = None
        self.lemmatizer = WordNetLemmatizer() if NLTK_AVAILABLE else WordNetLemmatizer()
        self.training_patterns = None
        
        # Cache pour optimiser les prédictions
        self.prediction_cache = {}
        self.cache_size_limit = 1000
        
        # Statistiques détaillées
        self.stats = {
            'messages_traites': 0,
            'temps_reponse_total': 0.0,
            'api_success': 0,
            'api_failures': 0,
            'keras_fallback_used': 0,
            'keras_predictions_cached': 0,
            'conversations_enregistrees': 0,
            'predictions_precises': 0,
            'predictions_incertaines': 0,
            'model_loading_time': 0.0,
            'requests_during_loading': 0,
            'api_used_during_loading': 0
        }
        
        logger.info("✅ Service chatbot initialisé avec chargement asynchrone")
        logger.info("🚫 Reformulation désactivée - réponses directes uniquement")
        logger.info(f"🌐 URL API: {self.config.API_URL}")
        logger.info(f"🧠 Fallback Keras: {'Activé (chargement asynchrone)' if self.config.USE_LEGACY_FALLBACK else 'Désactivé'}")
        
        # Démarrer le chargement asynchrone du modèle Keras si activé
        if self.config.USE_LEGACY_FALLBACK and TENSORFLOW_AVAILABLE:
            self._demarrer_chargement_modele_async()
        else:
            if not self.config.USE_LEGACY_FALLBACK:
                self.model_status = ModelStatus.DISABLED
                logger.info("🚫 Fallback Keras désactivé par configuration")
            else:
                self.model_status = ModelStatus.ERROR
                self.model_error_message = "TensorFlow non disponible"
                logger.warning("⚠️ TensorFlow non disponible - fallback impossible")
        
        # Test de connexion au démarrage (non bloquant)
        if self.api_client.test_connection():
            logger.info("🔗 Connexion API vérifiée")
        else:
            logger.warning("⚠️ API non accessible au démarrage")
            if self.model_status in [ModelStatus.LOADING, ModelStatus.NOT_INITIALIZED]:
                logger.info("🧠 Chargement du modèle Keras en cours pour le fallback...")
    
    def _demarrer_chargement_modele_async(self):
        """Démarre le chargement du modèle Keras en arrière-plan"""
        if self.model_loading_thread and self.model_loading_thread.is_alive():
            return  # Déjà en cours
        
        self.model_status = ModelStatus.LOADING
        self.model_loading_thread = threading.Thread(
            target=self._charger_modele_keras_async,
            daemon=True,
            name="ModelLoader"
        )
        self.model_loading_thread.start()
        logger.info("🔄 Chargement asynchrone du modèle Keras démarré")
    
    def _charger_modele_keras_async(self):
        """Charger le modèle Keras de manière asynchrone"""
        start_time = time.time()
        
        try:
            logger.info("🧠 Début du chargement asynchrone du modèle Keras...")
            
            # Vérifier l'existence des fichiers
            files_to_check = [
                (self.config.MODEL_PATH, "Modèle Keras"),
                (self.config.WORDS_PATH, "Vocabulaire"),
                (self.config.CLASSES_PATH, "Classes")
            ]
            
            missing_files = []
            for file_path, description in files_to_check:
                if not os.path.exists(file_path):
                    missing_files.append(f"{description} ({file_path})")
            
            if missing_files:
                raise FileNotFoundError(f"Fichiers manquants: {', '.join(missing_files)}")
            
            # Charger le modèle
            logger.info(f"📂 Chargement du modèle: {self.config.MODEL_PATH}")
            self.model = load_model(self.config.MODEL_PATH)
            logger.info("✅ Modèle Keras chargé")
            
            # Charger les mots
            logger.info(f"📂 Chargement du vocabulaire: {self.config.WORDS_PATH}")
            with open(self.config.WORDS_PATH, 'rb') as f:
                self.words = pickle.load(f)
            logger.info(f"✅ Vocabulaire chargé: {len(self.words)} mots")
            
            # Charger les classes
            logger.info(f"📂 Chargement des classes: {self.config.CLASSES_PATH}")
            with open(self.config.CLASSES_PATH, 'rb') as f:
                self.classes = pickle.load(f)
            logger.info(f"✅ Classes chargées: {len(self.classes)} catégories")
            
            # Charger les patterns d'entraînement (optionnel)
            patterns_path = os.path.join(self.config.BASE_DIR, "training_patterns.pkl")
            if os.path.exists(patterns_path):
                try:
                    with open(patterns_path, 'rb') as f:
                        self.training_patterns = pickle.load(f)
                    logger.info(f"✅ Patterns d'entraînement chargés: {len(self.training_patterns)} catégories")
                except Exception as e:
                    logger.warning(f"⚠️ Erreur chargement patterns: {e}")
                    self.training_patterns = None
            
            # Test rapide du modèle
            test_input = np.zeros((1, len(self.words)), dtype=np.float32)
            test_prediction = self.model.predict(test_input, verbose=0)
            logger.info(f"🧪 Test du modèle réussi (sortie: {test_prediction.shape})")
            
            # Marquer comme prêt
            loading_time = time.time() - start_time
            self.stats['model_loading_time'] = loading_time
            self.model_status = ModelStatus.READY
            
            logger.info(f"🎉 Modèle Keras prêt ! Temps de chargement: {loading_time:.2f}s")
            logger.info("🔄 Le fallback local est maintenant disponible")
            
        except Exception as e:
            loading_time = time.time() - start_time
            self.stats['model_loading_time'] = loading_time
            self.model_status = ModelStatus.ERROR
            self.model_error_message = str(e)
            
            # Nettoyer les ressources partiellement chargées
            self.model = None
            self.words = None
            self.classes = None
            self.training_patterns = None
            
            logger.error(f"❌ Erreur lors du chargement asynchrone du modèle: {e}")
            logger.error(f"⏱️ Temps avant échec: {loading_time:.2f}s")
            logger.info("🌐 L'application continuera avec l'API uniquement")
    
    def get_model_status(self) -> Dict[str, Any]:
        """Obtenir le statut actuel du modèle"""
        status_messages = {
            ModelStatus.NOT_INITIALIZED: "Non initialisé",
            ModelStatus.LOADING: "Chargement en cours...",
            ModelStatus.READY: "Prêt",
            ModelStatus.ERROR: f"Erreur: {self.model_error_message}",
            ModelStatus.DISABLED: "Désactivé"
        }
        
        return {
            "status": self.model_status.value,
            "message": status_messages[self.model_status],
            "loading_time": self.stats.get('model_loading_time', 0.0),
            "files_loaded": {
                "model": self.model is not None,
                "words": self.words is not None,
                "classes": self.classes is not None,
                "patterns": self.training_patterns is not None
            },
            "is_ready": self.model_status == ModelStatus.READY,
            "can_fallback": self.model_status == ModelStatus.READY and self.model is not None
        }
    
    def obtenir_reponse(self, message: str, session_id: str) -> str:
        """Obtenir une réponse du chatbot - SANS REFORMULATION"""
        start_time = time.time()
        
        try:
            # Validation et nettoyage du message
            if not message or len(message.strip()) == 0:
                return "Veuillez saisir un message."
            
            message = self._nettoyer_message_utilisateur(message.strip())
            logger.info(f"📨 Traitement message pour session: {session_id[:12]}...")
            
            # Statistiques pour les requêtes pendant le chargement
            if self.model_status == ModelStatus.LOADING:
                self.stats['requests_during_loading'] += 1
            
            # 1. Tentative via API externe (priorité)
            reponse_api = self._obtenir_reponse_api(message, session_id)
            response_time = (time.time() - start_time) * 1000
            
            if reponse_api:
                self.stats['api_success'] += 1
                if self.model_status == ModelStatus.LOADING:
                    self.stats['api_used_during_loading'] += 1
                
                # Enregistrer la conversation via l'API française
                self._enregistrer_conversation_api(
                    session_id, 
                    message, 
                    reponse_api['reponse'],
                    reponse_api.get('id_connaissance'),
                    reponse_api.get('confiance'),
                    response_time
                )
                
                # RÉPONSE DIRECTE SANS REFORMULATION
                reponse_finale = reponse_api['reponse'].strip()
                
                logger.info(f"🌐 Réponse obtenue via API: {len(reponse_finale)} caractères")
                return reponse_finale
            
            # 2. Fallback sur le modèle Keras local si disponible
            elif self.model_status == ModelStatus.READY and self.model is not None:
                self.stats['api_failures'] += 1
                self.stats['keras_fallback_used'] += 1
                
                logger.info("🧠 API indisponible - utilisation du modèle Keras (prêt)")
                reponse_keras = self._obtenir_reponse_keras_amelioree(message)
                
                if reponse_keras:
                    response_time = (time.time() - start_time) * 1000
                    self._enregistrer_conversation_api(
                        session_id, 
                        message, 
                        reponse_keras,
                        None,
                        0.7,
                        response_time
                    )
                    
                    logger.info(f"🧠 Réponse obtenue via Keras: {len(reponse_keras)} caractères")
                    return reponse_keras
            
            # 3. Gestion du cas où le modèle est en cours de chargement
            elif self.model_status == ModelStatus.LOADING:
                self.stats['api_failures'] += 1
                logger.info("🔄 API indisponible et modèle en cours de chargement...")
                
                # Réponse temporaire intelligente
                reponse_temporaire = self._reponse_chargement_en_cours(message)
                
                response_time = (time.time() - start_time) * 1000
                self._enregistrer_conversation_api(
                    session_id, 
                    message, 
                    reponse_temporaire,
                    None,
                    0.5,
                    response_time
                )
                
                return reponse_temporaire
            
            # 4. Réponse par défaut en dernier recours
            else:
                self.stats['api_failures'] += 1
                logger.warning("⚠️ API et Keras indisponibles - utilisation des réponses par défaut")
                reponse_defaut = self._reponse_par_defaut(message)
                
                response_time = (time.time() - start_time) * 1000
                self._enregistrer_conversation_api(
                    session_id, 
                    message, 
                    reponse_defaut,
                    None,
                    0.0,
                    response_time
                )
                
                return reponse_defaut
            
        except Exception as e:
            logger.error(f"Erreur dans obtenir_reponse: {e}")
            return "Désolé, une erreur s'est produite. Veuillez réessayer."
        
        finally:
            # Mise à jour des statistiques
            response_time = (time.time() - start_time) * 1000
            self.stats['messages_traites'] += 1
            self.stats['temps_reponse_total'] += response_time
    
    def _reponse_chargement_en_cours(self, message: str) -> str:
        """Réponse intelligente pendant le chargement du modèle"""
        message_lower = message.lower()
        
        # Réponses contextuelles pendant le chargement
        if any(mot in message_lower for mot in ['bonjour', 'salut', 'hello']):
            reponses = [
                "Bonjour ! Je me prépare pour mieux vous aider. En attendant, je peux essayer de vous répondre.",
                "Salut ! Mon système de fallback se charge. Que puis-je faire pour vous ?",
                "Hello ! Je suis en train d'optimiser mes capacités. Comment puis-je vous aider ?"
            ]
        elif any(mot in message_lower for mot in ['merci', 'thanks']):
            reponses = [
                "De rien ! Mon système se perfectionne pour vous offrir de meilleures réponses.",
                "Avec plaisir ! Je finalise mon chargement pour être plus efficace."
            ]
        elif any(mot in message_lower for mot in ['qui', 'quel', 'comment']):
            reponses = [
                "Je suis Mila, votre assistant pour le streaming. Mes capacités avancées se chargent en arrière-plan.",
                "Je suis en train d'initialiser mon système de fallback. Reformulez votre question dans quelques instants.",
                "Mon système d'IA local se charge. Cela me permettra de mieux vous aider même en cas de problème réseau."
            ]
        else:
            reponses = [
                "Je traite votre demande. Mon système se charge en arrière-plan pour de meilleures réponses.",
                "Veuillez patienter, j'optimise mes capacités. Reformulez votre question dans un moment.",
                "Mon intelligence locale se charge pour vous offrir un service plus robuste. Essayez dans quelques secondes.",
                "Système de fallback en cours d'activation. Cela m'aidera à mieux vous servir !"
            ]
        
        return random.choice(reponses)
    
    def _nettoyer_message_utilisateur(self, message: str) -> str:
        """Nettoyage amélioré du message utilisateur pour le domaine du streaming"""
        # Normalisation des termes spécialisés
        termes_specialises = {
            'ai_licia': 'ailicia',
            'ai-licia': 'ailicia',
            'ai licia': 'ailicia',
            'alicia': 'ailicia',
            'tts': 'synthèse vocale',
            'text-to-speech': 'synthèse vocale',
            'obs': 'OBS Studio',
            'plusieurs pc': 'plusieurs ordinateurs',
            'multiples pc': 'plusieurs ordinateurs',
            'en même temps': 'simultanément'
        }
        
        message_normalise = message.lower()
        for ancien, nouveau in termes_specialises.items():
            message_normalise = message_normalise.replace(ancien, nouveau)
        
        return message_normalise
    
    def _obtenir_reponse_api(self, message: str, session_id: str) -> Optional[Dict]:
        """Obtenir une réponse via l'API externe - une seule tentative"""
        try:
            logger.debug(f"🌐 Appel API chatbot pour session: {session_id[:12]}...")
            
            # Une seule tentative - basculement immédiat vers le fallback
            reponse = self.api_client.obtenir_reponse_chatbot(message, session_id)
            
            if reponse:
                logger.info(f"✅ Réponse API reçue (confiance: {reponse.get('confiance', 0):.2f})")
                return reponse
            else:
                logger.warning("❌ API indisponible - basculement immédiat vers fallback")
                
        except Exception as e:
            logger.error(f"Erreur API: {e}")
        
        return None
    
    def _obtenir_reponse_keras_amelioree(self, message: str) -> Optional[str]:
        """Obtenir une réponse via le modèle Keras local - SANS REFORMULATION"""
        try:
            if not self.model or not self.words or not self.classes:
                logger.warning("🧠 Modèle Keras non entièrement chargé")
                return None
            
            # Vérifier le cache de prédictions
            cache_key = self._generer_cache_key(message)
            if cache_key in self.prediction_cache:
                cached_result = self.prediction_cache[cache_key]
                self.stats['keras_predictions_cached'] += 1
                logger.debug(f"💾 Prédiction récupérée du cache")
                return self._generer_reponse_par_classe_amelioree(
                    cached_result['intent'], 
                    message, 
                    float(cached_result['probability'])
                )
            
            # Prédire la classe avec le modèle amélioré
            ints = self._predire_classe_keras_amelioree(message)
            if not ints:
                return None
            
            # Mettre en cache le résultat
            self._mettre_en_cache_prediction(cache_key, ints[0])
            
            # Générer la réponse DIRECTE SANS REFORMULATION
            intent = ints[0]['intent']
            confidence = ints[0]['probability']
            
            if confidence > 0.5:
                self.stats['predictions_precises'] += 1
            else:
                self.stats['predictions_incertaines'] += 1
            
            reponse = self._generer_reponse_par_classe_amelioree(intent, message, confidence)
            
            # RETOUR DIRECT SANS REFORMULATION
            return reponse.strip() if reponse else None
            
        except Exception as e:
            logger.error(f"Erreur dans le modèle Keras amélioré: {e}")
            return None
    
    def _generer_cache_key(self, message: str) -> str:
        """Générer une clé de cache pour les prédictions"""
        import hashlib
        message_simple = re.sub(r'[^\w\s]', '', message.lower()).strip()
        return hashlib.md5(message_simple.encode()).hexdigest()[:16]
    
    def _mettre_en_cache_prediction(self, cache_key: str, prediction: dict):
        """Mettre en cache une prédiction"""
        if len(self.prediction_cache) >= self.cache_size_limit:
            # Supprimer la plus ancienne entrée
            oldest_key = next(iter(self.prediction_cache))
            del self.prediction_cache[oldest_key]
        
        self.prediction_cache[cache_key] = prediction
    
    def _predire_classe_keras_amelioree(self, message: str) -> Optional[list]:
        """Prédiction de classe améliorée avec seuils adaptatifs"""
        try:
            # Nettoyage de la phrase avec améliorations
            mots_phrase = self._nettoyer_phrase_amelioree(message)
            
            # Créer le bag of words
            bag = self._creer_bag_of_words_ameliore(mots_phrase)
            
            # Prédiction avec le modèle
            res = self.model.predict(np.array([bag]), verbose=0)[0]
            
            # Seuils adaptatifs selon la longueur et le contenu du message
            seuil = self._calculer_seuil_adaptatif(message, mots_phrase)
            
            # Filtrage des résultats
            resultats = [[i, r] for i, r in enumerate(res) if r > seuil]
            
            # Si aucun résultat, essayer avec un seuil plus bas
            if not resultats:
                seuil_minimum = 0.1
                resultats = [[i, r] for i, r in enumerate(res) if r > seuil_minimum]
                logger.info(f"🧠 Utilisation du seuil minimum: {seuil_minimum}")
            
            # Trier par probabilité
            resultats.sort(key=lambda x: x[1], reverse=True)
            
            if resultats:
                predictions = [
                    {"intent": self.classes[r[0]], "probability": float(r[1])} 
                    for r in resultats[:3]  # Top 3 prédictions
                ]
                
                # Logging des prédictions pour debug
                if logger.isEnabledFor(logging.DEBUG):
                    top_predictions = [(p['intent'], p['probability']) for p in predictions]
                    logger.debug(f"🧠 Top prédictions: {top_predictions}")
                
                return predictions
            
            logger.info(f"🧠 Aucune prédiction fiable pour: '{message}'")
            return None
            
        except Exception as e:
            logger.error(f"Erreur prédiction Keras améliorée: {e}")
            return None
    
    def _calculer_seuil_adaptatif(self, message: str, mots_phrase: list) -> float:
        """Calcul d'un seuil adaptatif selon le contexte"""
        # Seuil de base
        seuil_base = 0.25
        
        # Ajustements selon le message
        message_lower = message.lower()
        
        # Messages très courts -> seuil plus bas
        if len(mots_phrase) <= 2:
            seuil_base = 0.15
        
        # Messages avec des mots-clés spécialisés -> seuil plus élevé
        mots_cles_precis = ['ailicia', 'synthèse vocale', 'obs studio', 'configuration']
        if any(mot in message_lower for mot in mots_cles_precis):
            seuil_base = 0.35
        
        # Questions claires -> seuil standard
        if any(mot in message_lower for mot in ['comment', 'que', 'qui', 'où', 'quand', 'pourquoi']):
            seuil_base = 0.25
        
        # Salutations simples -> seuil plus bas
        if any(mot in message_lower for mot in ['bonjour', 'salut', 'hello', 'merci']):
            seuil_base = 0.20
        
        return seuil_base
    
    def _nettoyer_phrase_amelioree(self, phrase: str) -> list:
        """Nettoyage de phrase amélioré avec préservation des termes techniques"""
        try:
            # Normalisation
            phrase = phrase.lower().strip()
            
            # Préservation des termes techniques avant tokenisation
            termes_preserves = {
                'ailicia': 'AILICIA_TOKEN',
                'synthèse vocale': 'TTS_TOKEN',
                'obs studio': 'OBS_TOKEN',
                'plusieurs ordinateurs': 'MULTI_PC_TOKEN',
                'simultanément': 'SIMULTANE_TOKEN'
            }
            
            phrase_preservee = phrase
            for terme, token in termes_preserves.items():
                phrase_preservee = phrase_preservee.replace(terme, token)
            
            # Suppression des caractères spéciaux mais conservation de l'important
            phrase_preservee = re.sub(r'[^\w\s]', ' ', phrase_preservee)
            
            # Tokenisation
            if NLTK_AVAILABLE:
                try:
                    mots_phrase = word_tokenize(phrase_preservee, language='french')
                except:
                    mots_phrase = phrase_preservee.split()
            else:
                mots_phrase = phrase_preservee.split()
            
            # Restauration des termes techniques et lemmatisation
            mots_nettoyes = []
            for mot in mots_phrase:
                if mot.endswith('_TOKEN'):
                    # Restaurer le terme technique original
                    for terme, token in termes_preserves.items():
                        if mot == token:
                            mots_nettoyes.append(terme.replace(' ', ''))
                            break
                elif len(mot) > 1:
                    mot_lemma = self.lemmatizer.lemmatize(mot.lower())
                    mots_nettoyes.append(mot_lemma)
            
            logger.debug(f"🧠 Phrase nettoyée: '{phrase}' -> {mots_nettoyes}")
            return mots_nettoyes
            
        except Exception as e:
            logger.error(f"Erreur nettoyage phrase amélioré: {e}")
            return phrase.lower().split()
    
    def _creer_bag_of_words_ameliore(self, mots_phrase: list) -> np.ndarray:
        """Création d'un bag of words avec pondération des termes importants"""
        try:
            bag = np.zeros(len(self.words), dtype=np.float32)
            
            # Mots-clés importants pour le domaine
            mots_cles_importants = [
                'ailicia', 'tts', 'obs', 'configuration', 'utiliser', 
                'plusieurs', 'ordinateur', 'simultanément', 'aide'
            ]
            
            for mot in mots_phrase:
                for i, word in enumerate(self.words):
                    if word == mot:
                        # Pondération spéciale pour les mots-clés
                        if mot in mots_cles_importants:
                            bag[i] = 1.2  # Boost pour mots-clés
                        else:
                            bag[i] = 1.0
                        break
            
            return bag
            
        except Exception as e:
            logger.error(f"Erreur création bag of words amélioré: {e}")
            return np.zeros(len(self.words) if self.words else 0, dtype=np.float32)
    
    def _generer_reponse_par_classe_amelioree(
        self, 
        classe_predite: str, 
        message: str, 
        confidence: float
    ) -> Optional[str]:
        """Génération de réponse DIRECTE utilisant les patterns d'entraînement"""
        try:
            # Utiliser les patterns d'entraînement si disponibles
            if self.training_patterns and classe_predite in self.training_patterns:
                responses = self.training_patterns[classe_predite].get('responses', [])
                if responses:
                    reponse = random.choice(responses)
                    logger.info(f"🧠 Réponse depuis patterns d'entraînement: {classe_predite}")
                    return reponse
            
            # Fallback sur les réponses contextuelles intégrées
            message_lower = message.lower()
            
            # Réponses contextuelles par domaine
            reponses_contextuelles = {
                'greeting': [
                    "Bonjour ! Je suis Mila, votre assistant pour le streaming. Comment puis-je vous aider ?",
                    "Salut ! Je suis là pour vous assister avec vos questions de streaming et configuration.",
                    "Hello ! Que puis-je faire pour améliorer votre setup de streaming ?"
                ],
                'goodbye': [
                    "Au revoir ! N'hésitez pas à revenir si vous avez d'autres questions sur le streaming !",
                    "À bientôt ! Bon stream et bonne journée !",
                    "À plus tard ! Que votre streaming soit parfait !"
                ],
                'thanks': [
                    "De rien ! C'est un plaisir de vous aider avec votre setup de streaming !",
                    "Je vous en prie ! N'hésitez pas pour d'autres questions techniques.",
                    "Avec plaisir ! Bon streaming !"
                ],
                'help': [
                    "Je suis Mila, votre assistant spécialisé dans le streaming. Je peux vous aider avec OBS, TTS, audio et bien plus !",
                    "Je suis là pour vous aider ! Posez-moi vos questions sur la configuration de streaming.",
                    "Comment puis-je vous assister ? Je connais bien OBS, les configurations audio et les outils de streaming."
                ],
                'identity': [
                    "Je suis Mila, votre assistant virtuel spécialisé dans le streaming et les configurations techniques.",
                    "Je m'appelle Mila. Je suis votre assistant IA pour tout ce qui concerne le streaming.",
                    "Je suis Mila, créée pour vous aider avec vos questions de streaming, OBS, TTS et configuration."
                ]
            }
            
            # Essayer de trouver une réponse contextuelle
            if classe_predite in reponses_contextuelles:
                reponse = random.choice(reponses_contextuelles[classe_predite])
                logger.info(f"🧠 Réponse contextuelle pour classe '{classe_predite}'")
                return reponse
            
            # Génération de réponse intelligente selon le contenu
            if any(keyword in message_lower for keyword in ['comment', 'how', 'aide', 'help']):
                reponses_aide = [
                    f"Concernant {classe_predite}, je peux vous fournir des informations détaillées. Soyez plus spécifique sur votre besoin de streaming.",
                    f"Pour {classe_predite}, j'ai des connaissances qui peuvent vous aider. Que voulez-vous configurer exactement ?",
                    f"Je comprends votre question sur {classe_predite}. Précisez votre setup actuel pour un conseil personnalisé."
                ]
                return random.choice(reponses_aide)
            
            # Réponse générale avec mention de la confiance si faible
            if confidence < 0.3:
                reponses_incertaines = [
                    f"Je pense que votre question concerne {classe_predite}, mais pouvez-vous être plus précis pour votre streaming ?",
                    f"Votre question semble liée à {classe_predite}. Reformulez pour que je puisse mieux vous aider avec votre setup.",
                ]
                return random.choice(reponses_incertaines)
            else:
                reponses_generales = [
                    f"Je détecte que votre question concerne {classe_predite}. Je peux vous aider avec cet aspect de votre streaming.",
                    f"Votre question semble liée à {classe_predite}. Comment puis-je vous assister pour votre setup ?",
                ]
                return random.choice(reponses_generales)
            
        except Exception as e:
            logger.error(f"Erreur génération réponse par classe améliorée: {e}")
            return "Je comprends votre question, mais je ne peux pas y répondre précisément. Pouvez-vous reformuler ?"
    
    def _enregistrer_conversation_api(self, session_id: str, question: str, reponse: str,
                                     id_connaissance: Optional[int] = None,
                                     score_confiance: Optional[float] = None,
                                     temps_reponse_ms: Optional[float] = None):
        """Enregistrer la conversation via l'API française"""
        try:
            # Utiliser le client API français pour enregistrer
            success = self.api_client.enregistrer_conversation(
                session_id, question, reponse, 
                id_connaissance, score_confiance, temps_reponse_ms
            )
            
            if success:
                self.stats['conversations_enregistrees'] += 1
                logger.debug(f"📝 Conversation enregistrée (total: {self.stats['conversations_enregistrees']})")
            else:
                logger.warning("⚠️ Échec enregistrement conversation via API")
                
        except Exception as e:
            logger.error(f"Erreur enregistrement conversation API: {e}")
    
    def _reponse_par_defaut(self, message: str) -> str:
        """Réponses par défaut contextuelles pour le domaine du streaming"""
        message_lower = message.lower()
        
        # Réponses spécialisées selon le contexte détecté
        if any(mot in message_lower for mot in ['obs', 'streaming', 'stream']):
            reponses = [
                "Je suis spécialisée dans l'aide au streaming, mais je n'ai pas trouvé de réponse précise. Pouvez-vous reformuler votre question sur OBS ou votre configuration ?",
                "Concernant le streaming, ma base de connaissances ne couvre pas votre question spécifique. Décrivez votre setup ou votre problème plus précisément."
            ]
        elif any(mot in message_lower for mot in ['audio', 'micro', 'son']):
            reponses = [
                "Pour les questions audio, je peux généralement aider avec la configuration. Précisez votre matériel ou votre problème spécifique.",
                "L'audio est important pour le streaming. Reformulez votre question en mentionnant votre équipement ou configuration actuelle."
            ]
        elif any(mot in message_lower for mot in ['tts', 'synthèse', 'voix']):
            reponses = [
                "Pour la synthèse vocale, je peux normalement vous guider. Précisez quel logiciel TTS vous utilisez ou voulez utiliser.",
                "Concernant le TTS, reformulez votre question en précisant votre setup ou l'intégration souhaitée."
            ]
        else:
            # Réponses par défaut générales
            reponses = [
                "Je ne trouve pas de réponse précise dans ma base de connaissances. Reformulez votre question ou soyez plus spécifique.",
                "Ma base de données ne couvre pas cette question. Précisez votre demande ou posez une question différente.",
                "Je n'ai pas trouvé d'information correspondante. Pouvez-vous détailler votre question ou votre problème ?",
                "Service temporairement limité. Reformulez votre question de manière plus précise pour une meilleure assistance."
            ]
        
        return random.choice(reponses)
    
    # FONCTIONS DE GESTION DES MODES - SUPPRIMÉES CAR REFORMULATION DÉSACTIVÉE
    def changer_mode(self, nouveau_mode: str) -> bool:
        """DÉSACTIVÉ - Les modes de reformulation ne sont plus disponibles"""
        logger.info(f"🚫 Tentative de changement de mode refusée - reformulation désactivée")
        return False
    
    def get_current_mode(self) -> str:
        """Retourne toujours 'minimal' car reformulation désactivée"""
        return "minimal"
    
    def test_api_connection(self) -> bool:
        """Tester la connexion à l'API avec timeout approprié"""
        if not self.config.USE_API:
            return False
        
        try:
            return self.api_client.test_connection()
        except Exception as e:
            logger.warning(f"Test API échoué: {e}")
            return False
    
    def obtenir_statistiques(self) -> Dict[str, Any]:
        """Obtenir les statistiques complètes du service"""
        temps_moyen = (
            self.stats['temps_reponse_total'] / self.stats['messages_traites']
            if self.stats['messages_traites'] > 0 else 0
        )
        
        # Calcul du taux de précision des prédictions Keras
        total_predictions = self.stats['predictions_precises'] + self.stats['predictions_incertaines']
        taux_precision = (
            self.stats['predictions_precises'] / total_predictions * 100
            if total_predictions > 0 else 0
        )
        
        # Calcul du taux d'utilisation de l'API pendant le chargement
        taux_api_pendant_chargement = (
            self.stats['api_used_during_loading'] / self.stats['requests_during_loading'] * 100
            if self.stats['requests_during_loading'] > 0 else 0
        )
        
        return {
            'messages_traites': self.stats['messages_traites'],
            'temps_reponse_moyen': temps_moyen,
            'api_success': self.stats['api_success'],
            'api_failures': self.stats['api_failures'],
            'keras_fallback_used': self.stats['keras_fallback_used'],
            'keras_predictions_cached': self.stats['keras_predictions_cached'],
            'predictions_precises': self.stats['predictions_precises'],
            'predictions_incertaines': self.stats['predictions_incertaines'],
            'taux_precision_keras': round(taux_precision, 1),
            'conversations_cache': 0,  # Pas de cache local
            'mode_actuel': self.current_mode,
            'reformulation_active': False,  # NOUVEAU: indique que reformulation est désactivée
            'api_connectee': self.test_api_connection(),
            'db_connectee': 'API_EXTERNE',
            'logging_mode': 'API_FRANCAISE',
            'modele_local_charge': self.model is not None,
            'fallback_keras_actif': self.config.USE_LEGACY_FALLBACK and self.model is not None,
            'tensorflow_disponible': TENSORFLOW_AVAILABLE,
            'nltk_disponible': NLTK_AVAILABLE,
            'patterns_entrainement_charges': self.training_patterns is not None,
            'taille_cache_predictions': len(self.prediction_cache),
            
            # Nouvelles statistiques pour le chargement asynchrone
            'model_status': self.model_status.value,
            'model_loading_time': self.stats['model_loading_time'],
            'requests_during_loading': self.stats['requests_during_loading'],
            'api_used_during_loading': self.stats['api_used_during_loading'],
            'taux_api_pendant_chargement': round(taux_api_pendant_chargement, 1),
            'chargement_asynchrone': True,
            'model_error_message': self.model_error_message
        }
    
    def vider_cache_predictions(self):
        """Vider le cache des prédictions"""
        self.prediction_cache.clear()
        logger.info("🗑️ Cache des prédictions vidé")
    
    def fermer(self):
        """Fermeture propre du service avec statistiques finales"""
        logger.info(f"Fermeture du service chatbot (sans reformulation):")
        logger.info(f"  - {self.stats['conversations_enregistrees']} conversations enregistrées")
        logger.info(f"  - {self.stats['api_success']} succès API, {self.stats['api_failures']} échecs")
        logger.info(f"  - {self.stats['keras_fallback_used']} utilisations du fallback Keras")
        logger.info(f"  - {self.stats['keras_predictions_cached']} prédictions mises en cache")
        logger.info(f"  - {self.stats['predictions_precises']} prédictions précises")
        logger.info(f"  - Statut du modèle: {self.model_status.value}")
        logger.info(f"  - Temps de chargement: {self.stats['model_loading_time']:.2f}s")
        logger.info(f"  - Requêtes pendant chargement: {self.stats['requests_during_loading']}")
        logger.info(f"  - Reformulation: DÉSACTIVÉE")
        
        # Statistiques de performance
        if self.stats['messages_traites'] > 0:
            temps_moyen = self.stats['temps_reponse_total'] / self.stats['messages_traites']
            logger.info(f"  - Temps de réponse moyen: {temps_moyen:.2f}ms")
        
        # Attendre la fin du chargement si nécessaire
        if self.model_loading_thread and self.model_loading_thread.is_alive():
            logger.info("⏳ Attente de la fin du chargement du modèle...")
            self.model_loading_thread.join(timeout=5.0)
        
        logger.info("✅ Service chatbot fermé proprement (reformulation désactivée)")