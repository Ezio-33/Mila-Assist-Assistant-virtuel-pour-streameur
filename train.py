#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRAIN_V2.PY - ENTRAÎNEMENT UNIFIÉ POUR MILA ASSIST (VERSION RNCP6)
========================================================================

- Gestion intelligente des backups (limitation à 3 versions)
- Suppression automatique des anciennes sauvegardes
- Métriques d'entraînement avancées
- Logging amélioré avec historique
- Validation croisée optionnelle
- Monitoring des performances

Fonctionnalités:
- Récupération des données depuis l'API/base de données
- Entraînement du modèle Keras pour le fallback local
- Mise à jour automatique de words.pkl et classes.pkl
- Sauvegarde et versioning intelligent des modèles
- Architecture robuste avec gestion d'erreurs

Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import os
import sys
import json
import pickle
import random
import shutil
import requests
import urllib3
import numpy as np
import nltk
import logging
import time
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from dotenv import load_dotenv

# Imports TensorFlow avec gestion d'erreur
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, Input, BatchNormalization
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    from tensorflow.keras.regularizers import l2
    TENSORFLOW_AVAILABLE = True
except ImportError as e:
    print(f"❌ TensorFlow non disponible: {e}")
    print("💡 Installez avec: pip install tensorflow")
    TENSORFLOW_AVAILABLE = False

# Imports NLTK avec gestion d'erreur
try:
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    print("❌ NLTK non disponible")
    print("💡 Installez avec: pip install nltk")
    NLTK_AVAILABLE = False

# Désactiver les avertissements SSL pour le NAS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Charger la configuration depuis .env
load_dotenv()

@dataclass
class TrainingMetrics:
    """Métriques d'entraînement pour suivi des performances"""
    start_time: float
    end_time: float = 0.0
    total_knowledge: int = 0
    valid_tags: int = 0
    vocabulary_size: int = 0
    total_patterns: int = 0
    model_accuracy: float = 0.0
    training_loss: float = 0.0
    epochs_completed: int = 0
    data_augmentation_factor: float = 0.0
    
    @property
    def duration(self) -> float:
        return self.end_time - self.start_time if self.end_time > 0 else 0.0
    
    def to_dict(self) -> dict:
        return {
            **asdict(self),
            'duration_seconds': self.duration,
            'timestamp': datetime.now().isoformat()
        }

class TrainingLogger:
    """Logger centralisé pour l'entraînement avec historique"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configuration du logging
        timestamp = datetime.now().strftime('%d-%m-%Y_%Hh%Mmin%Ss')
        log_file = self.log_dir / f"training_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🚀 Démarrage du logging d'entraînement v2.0")
    
    def log_metrics(self, metrics: TrainingMetrics):
        """Sauvegarde les métriques d'entraînement avec historique"""
        metrics_file = self.log_dir / "training_metrics_history.json"
        
        try:
            # Charger l'historique existant
            if metrics_file.exists():
                with open(metrics_file, 'r', encoding='utf-8') as f:
                    all_metrics = json.load(f)
            else:
                all_metrics = []
            
            # Ajouter les nouvelles métriques
            all_metrics.append(metrics.to_dict())
            
            # Limiter l'historique (garder les 50 derniers entraînements)
            if len(all_metrics) > 50:
                all_metrics = all_metrics[-50:]
            
            # Sauvegarder
            with open(metrics_file, 'w', encoding='utf-8') as f:
                json.dump(all_metrics, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"📊 Métriques sauvegardées: précision={metrics.model_accuracy:.4f}, durée={metrics.duration:.2f}s")
            
            # Nettoyage des anciens logs (garder 10 fichiers)
            self._cleanup_old_logs()
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde métriques: {e}")
    
    def _cleanup_old_logs(self):
        """Nettoie les anciens fichiers de log"""
        try:
            log_files = sorted([f for f in self.log_dir.glob("training_*-*-*_*h*min*s.log")], 
                             key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Garder seulement les 10 plus récents
            for old_log in log_files[10:]:
                old_log.unlink()
                self.logger.info(f"🗑️ Ancien log supprimé: {old_log.name}")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Erreur nettoyage logs: {e}")

class BackupManager:
    """Gestionnaire de sauvegardes intelligent avec limitation automatique"""
    
    def __init__(self, base_dir: str, max_backups: int = 3):
        self.base_dir = Path(base_dir)
        self.backup_dir = self.base_dir / "data" / "Backup"
        self.max_backups = max_backups
        self.logger = logging.getLogger(__name__)
        self._create_backup_structure()
    
    def _create_backup_structure(self):
        """Crée la structure des répertoires de sauvegarde"""
        backup_dirs = [
            "Model", "Words", "Classes", "Patterns", "Metrics"
        ]
        
        for dir_name in backup_dirs:
            dir_path = self.backup_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
        self.logger.info(f"📁 Structure de backup créée dans {self.backup_dir}")
    
    def _get_backup_files(self, backup_type: str, pattern: str) -> List[Path]:
        """Récupère la liste des fichiers de backup d'un type donné"""
        backup_path = self.backup_dir / backup_type
        return sorted(backup_path.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)
    
    def _cleanup_old_backups(self, backup_type: str, pattern: str):
        """Supprime les anciens backups au-delà de la limite"""
        backup_files = self._get_backup_files(backup_type, pattern)
        
        if len(backup_files) > self.max_backups:
            files_to_remove = backup_files[self.max_backups:]
            
            for old_file in files_to_remove:
                try:
                    old_file.unlink()
                    self.logger.info(f"🗑️ Ancien backup supprimé: {old_file.name}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Erreur suppression {old_file.name}: {e}")
            
            self.logger.info(f"🧹 Nettoyage {backup_type}: {len(files_to_remove)} fichiers supprimés")
    
    def backup_model(self) -> bool:
        """Sauvegarde le modèle existant avec gestion automatique des versions"""
        model_path = self.base_dir / "chatbot_model.keras"
        
        if not model_path.exists():
            self.logger.info("ℹ️ Aucun modèle existant à sauvegarder")
            return False
        
        timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
        backup_path = self.backup_dir / "Model" / f"chatbot_model_{timestamp}.keras"
        
        try:
            shutil.copy2(model_path, backup_path)
            self.logger.info(f"💾 Modèle sauvegardé: {backup_path.name}")
            
            # Nettoyage automatique
            self._cleanup_old_backups("Model", "chatbot_model_*.keras")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde modèle: {e}")
            return False
    
    def backup_vocabulary_files(self) -> bool:
        """Sauvegarde words.pkl et classes.pkl avec gestion des versions"""
        timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
        success = True
        
        files_to_backup = [
            ("words.pkl", "Words"),
            ("classes.pkl", "Classes")
        ]
        
        for filename, backup_type in files_to_backup:
            source_path = self.base_dir / filename
            
            if source_path.exists():
                backup_path = self.backup_dir / backup_type / f"{filename}_{timestamp}"
                
                try:
                    shutil.copy2(source_path, backup_path)
                    self.logger.info(f"💾 {filename} sauvegardé: {backup_path.name}")
                    
                    # Nettoyage automatique
                    self._cleanup_old_backups(backup_type, f"{filename}_*")
                    
                except Exception as e:
                    self.logger.error(f"❌ Erreur sauvegarde {filename}: {e}")
                    success = False
            else:
                self.logger.info(f"ℹ️ {filename} n'existe pas encore")
        
        return success
    
    def backup_training_patterns(self, donnees_tags: Dict[str, Any]) -> bool:
        """Sauvegarde les patterns d'entraînement avec métadonnées"""
        timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
        
        # Préparer les données avec métadonnées
        backup_data = {
            "timestamp": timestamp,
            "total_tags": len(donnees_tags),
            "total_patterns": sum(len(d['patterns']) for d in donnees_tags.values()),
            "total_responses": sum(len(d['responses']) for d in donnees_tags.values()),
            "data": donnees_tags
        }
        
        backup_path = self.backup_dir / "Patterns" / f"training_patterns_{timestamp}.pkl"
        
        try:
            with open(backup_path, 'wb') as f:
                pickle.dump(backup_data, f)
            
            self.logger.info(f"💾 Patterns sauvegardés: {backup_path.name}")
            
            # Nettoyage automatique
            self._cleanup_old_backups("Patterns", "training_patterns_*.pkl")
            
            # Mise à jour du fichier actuel
            current_path = self.base_dir / "training_patterns.pkl"
            with open(current_path, 'wb') as f:
                pickle.dump(donnees_tags, f)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde patterns: {e}")
            return False
    
    def backup_metrics(self, metrics: TrainingMetrics) -> bool:
        """Sauvegarde les métriques d'entraînement"""
        timestamp = datetime.now().strftime("%d-%m-%Y_%Hh%Mmin%Ss")
        backup_path = self.backup_dir / "Metrics" / f"training_metrics_{timestamp}.json"
        
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(metrics.to_dict(), f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📊 Métriques sauvegardées: {backup_path.name}")
            
            # Nettoyage automatique
            self._cleanup_old_backups("Metrics", "training_metrics_*.json")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde métriques: {e}")
            return False
    
    def get_backup_summary(self) -> Dict[str, int]:
        """Retourne un résumé des sauvegardes disponibles"""
        summary = {}
        
        backup_types = [
            ("Model", "chatbot_model_*-*-*_*h*min*s.keras"),
            ("Words", "words.pkl_*-*-*_*h*min*s"),
            ("Classes", "classes.pkl_*-*-*_*h*min*s"),
            ("Patterns", "training_patterns_*-*-*_*h*min*s.pkl"),
            ("Metrics", "training_metrics_*-*-*_*h*min*s.json")
        ]
        
        for backup_type, pattern in backup_types:
            files = self._get_backup_files(backup_type, pattern)
            summary[backup_type] = len(files)
        
        return summary

class ConfigurationManager:
    """Gestionnaire de configuration centralisé"""
    
    def __init__(self):
        self.API_URL = os.getenv('API_URL', 'http://localhost:5000/api')
        self.API_KEY = os.getenv('API_KEY', 'your-api-key-here')
        self.USE_API = os.getenv('USE_API', 'true').lower() == 'true'
        self.USE_LEGACY_FALLBACK = os.getenv('USE_LEGACY_FALLBACK', 'true').lower() == 'true'
        self.DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
        self.MAX_BACKUPS = int(os.getenv('MAX_BACKUPS', '3'))
        self.ENABLE_CROSS_VALIDATION = os.getenv('ENABLE_CROSS_VALIDATION', 'false').lower() == 'true'
        
        # Validation de la configuration
        if not self.USE_LEGACY_FALLBACK:
            print("⚠️ USE_LEGACY_FALLBACK=false - Le fallback Keras ne sera pas utilisé")
        
        if not self.USE_API:
            print("⚠️ USE_API=false - L'API ne sera pas utilisée")

class APIClient:
    """Client API pour récupérer les données d'entraînement"""
    
    def __init__(self, config: ConfigurationManager):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': config.API_KEY,
            'Content-Type': 'application/json'
        })
        self.logger = logging.getLogger(__name__)
    
    def test_connection(self) -> bool:
        """Test de connexion à l'API"""
        try:
            response = self.session.get(
                f"{self.config.API_URL}/health",
                timeout=10,
                verify=False
            )
            return response.status_code == 200
        except Exception as e:
            if self.config.DEBUG:
                self.logger.debug(f"Erreur connexion API: {e}")
            return False
    
    def recuperer_toutes_connaissances(self) -> List[Dict[str, Any]]:
        """Récupère toutes les connaissances de la base de données"""
        self.logger.info("🔍 Récupération des connaissances depuis l'API...")
        
        toutes_connaissances = []
        connaissances_vues = set()
        
        # Requêtes larges pour couvrir le maximum de données
        requetes_recherche = [
            "bonjour", "salut", "hello", "comment", "que", "qui", "où", "quand",
            "pourquoi", "aide", "merci", "ai_licia", "ailicia", "alicia", "mila",
            "stream", "streaming", "TTS", "OBS", "configuration", "configurer",
            "utiliser", "plusieurs", "pc", "ordinateur", "audio", "voice", "vocal",
            "test", "erreur", "problème", "solution", ""  # Requête vide pour tout
        ]
        
        for i, requete in enumerate(requetes_recherche):
            self.logger.info(f"   📋 Recherche {i+1}/{len(requetes_recherche)}: '{requete}'...")
            
            try:
                payload = {
                    "query": requete,
                    "top_k": 1000,
                    "threshold": 0.0  # Récupérer tout
                }
                
                response = self.session.post(
                    f"{self.config.API_URL}/search",
                    json=payload,
                    timeout=30,
                    verify=False
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and 'results' in data:
                        for resultat in data['results']:
                            # Créer une clé unique pour éviter les doublons
                            cle_unique = (
                                resultat.get('tag', '').strip(),
                                resultat.get('question', '').strip()
                            )
                            
                            if (cle_unique not in connaissances_vues and 
                                all(cle_unique) and 
                                len(resultat.get('question', '')) > 2 and
                                len(resultat.get('response', '')) > 2):
                                
                                connaissances_vues.add(cle_unique)
                                toutes_connaissances.append(resultat)
                        
                        self.logger.info(f"      ✅ {len(data['results'])} résultats trouvés")
                    else:
                        self.logger.warning(f"Pas de résultats: {data}")
                else:
                    self.logger.warning(f"Erreur HTTP {response.status_code}")
                    
            except Exception as e:
                self.logger.error(f"Erreur requête: {e}")
        
        self.logger.info(f"📊 Total connaissances uniques: {len(toutes_connaissances)}")
        return toutes_connaissances

class DataProcessor:
    """Processeur de données pour l'entraînement"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.lemmatizer = WordNetLemmatizer() if NLTK_AVAILABLE else None
        self.logger = logging.getLogger(__name__)
        
        # Télécharger les ressources NLTK si nécessaire
        if NLTK_AVAILABLE:
            self._download_nltk_resources()
    
    def _download_nltk_resources(self):
        """Télécharge les ressources NLTK nécessaires"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            self.logger.info("📦 Téléchargement des ressources NLTK...")
            nltk.download('punkt', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('omw-1.4', quiet=True)
    
    def nettoyer_texte(self, texte: str) -> str:
        """Nettoyage de texte optimisé pour le domaine du streaming"""
        if not texte:
            return ""
        
        # Normalisation de base
        texte = texte.lower().strip()
        
        # Normalisation des termes spécialisés
        termes_specialises = {
            'ai_licia': 'ailicia',
            'ai-licia': 'ailicia',
            'ai licia': 'ailicia',
            'tts': 'texttospeech',
            'text-to-speech': 'texttospeech',
            'text to speech': 'texttospeech',
            'obs': 'obscapture',
            'obs studio': 'obscapture',
            'plusieurs pc': 'plusieurspc',
            'multiples pc': 'plusieurspc',
            'en même temps': 'simultanement',
            'même temps': 'simultanement'
        }
        
        for ancien, nouveau in termes_specialises.items():
            texte = texte.replace(ancien, nouveau)
        
        # Suppression des caractères non pertinents
        import re
        texte = re.sub(r'[^\w\s]', ' ', texte)
        texte = re.sub(r'\s+', ' ', texte)
        
        return texte.strip()
    
    def convertir_donnees_vers_format_entrainement(
        self, 
        connaissances: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convertit les données de la base vers le format d'entraînement"""
        self.logger.info("🔄 Conversion des données vers format d'entraînement...")
        
        # Grouper par tag
        donnees_par_tag = {}
        
        for connaissance in connaissances:
            tag = connaissance.get('tag', 'general').strip()
            question = self.nettoyer_texte(connaissance.get('question', ''))
            reponse = connaissance.get('response', '').strip()
            
            # Validation
            if not tag or not question or not reponse:
                continue
            
            if len(question) < 3 or len(reponse) < 3:
                continue
            
            if tag not in donnees_par_tag:
                donnees_par_tag[tag] = {
                    'patterns': [],
                    'responses': []
                }
            
            # Ajouter si pas déjà présent
            if question not in donnees_par_tag[tag]['patterns']:
                donnees_par_tag[tag]['patterns'].append(question)
            
            if reponse not in donnees_par_tag[tag]['responses']:
                donnees_par_tag[tag]['responses'].append(reponse)
        
        # Filtrer les tags avec données insuffisantes
        donnees_valides = {}
        for tag, donnees in donnees_par_tag.items():
            if len(donnees['patterns']) > 0 and len(donnees['responses']) > 0:
                donnees_valides[tag] = donnees
            elif self.debug:
                self.logger.warning(f"Tag '{tag}' ignoré (données insuffisantes)")
        
        # Statistiques
        total_patterns = sum(len(d['patterns']) for d in donnees_valides.values())
        total_responses = sum(len(d['responses']) for d in donnees_valides.values())
        
        self.logger.info(f"📋 {len(donnees_valides)} tags valides")
        self.logger.info(f"📊 {total_patterns} patterns, {total_responses} responses")
        
        return donnees_valides
    
    def augmenter_donnees(self, donnees_tags: Dict[str, Any]) -> Dict[str, Any]:
        """Augmentation intelligente des données d'entraînement"""
        self.logger.info("🔄 Augmentation des données d'entraînement...")
        
        # Synonymes contextuels pour le domaine
        synonymes = {
            'comment': ['de quelle manière', 'comment faire', 'comment puis-je'],
            'configurer': ['paramétrer', 'régler', 'ajuster', 'installer'],
            'utiliser': ['employer', 'se servir de', 'faire fonctionner'],
            'ailicia': ['ia', 'assistant', 'bot', 'chatbot'],
            'plusieurs': ['multiples', 'différents', 'nombreux'],
            'ordinateur': ['pc', 'machine', 'poste'],
            'simultanement': ['en parallèle', 'conjointement'],
            'aide': ['assistance', 'support', 'aider'],
            'problème': ['souci', 'erreur', 'bug', 'dysfonctionnement']
        }
        
        donnees_augmentees = {}
        
        for tag, donnees in donnees_tags.items():
            nouvelles_donnees = {
                'patterns': donnees['patterns'].copy(),
                'responses': donnees['responses'].copy()
            }
            
            # Créer des variations avec synonymes
            patterns_originaux = nouvelles_donnees['patterns'].copy()
            for pattern in patterns_originaux:
                mots = pattern.split()
                
                # Appliquer les synonymes (maximum 2 par mot)
                for i, mot in enumerate(mots):
                    if mot in synonymes:
                        for synonyme in synonymes[mot][:2]:
                            nouveaux_mots = mots.copy()
                            nouveaux_mots[i] = synonyme
                            nouveau_pattern = ' '.join(nouveaux_mots)
                            
                            if nouveau_pattern not in nouvelles_donnees['patterns']:
                                nouvelles_donnees['patterns'].append(nouveau_pattern)
            
            donnees_augmentees[tag] = nouvelles_donnees
        
        # Statistiques de l'augmentation
        patterns_avant = sum(len(d['patterns']) for d in donnees_tags.values())
        patterns_après = sum(len(d['patterns']) for d in donnees_augmentees.values())
        
        self.logger.info(f"📈 Patterns avant: {patterns_avant}, après: {patterns_après}")
        self.logger.info(f"🎯 Augmentation: +{patterns_après - patterns_avant} patterns")
        
        return donnees_augmentees

class ModelTrainer:
    """Entraîneur de modèle Keras optimisé"""
    
    def __init__(self, config: ConfigurationManager):
        self.config = config
        self.lemmatizer = WordNetLemmatizer() if NLTK_AVAILABLE else None
        self.logger = logging.getLogger(__name__)
    
    def entrainer_modele(
        self, 
        donnees_tags: Dict[str, Any]
    ) -> Tuple[List[str], List[str], Optional[object], TrainingMetrics]:
        """Entraînement du modèle Keras optimisé avec métriques"""
        
        if not TENSORFLOW_AVAILABLE:
            self.logger.error("TensorFlow non disponible - impossible d'entraîner le modèle")
            return [], [], None, TrainingMetrics(start_time=time.time())
        
        # Initialisation des métriques
        metrics = TrainingMetrics(start_time=time.time())
        
        self.logger.info("🤖 Entraînement du modèle Keras...")
        
        # Préparation des données
        words = []
        classes = []
        documents = []
        ignore_words = ['?', '.', ',', '!', ':', ';', '(', ')', '[', ']', '"', "'"]
        
        # Extraction des features
        for tag, donnees in donnees_tags.items():
            for pattern in donnees['patterns']:
                if NLTK_AVAILABLE:
                    word_list = word_tokenize(pattern, language='french')
                else:
                    word_list = pattern.split()
                
                words.extend(word_list)
                documents.append((word_list, tag))
            
            if tag not in classes:
                classes.append(tag)
        
        # Nettoyage et lemmatisation
        if self.lemmatizer:
            words_cleaned = [
                self.lemmatizer.lemmatize(w.lower()) 
                for w in words 
                if w not in ignore_words and len(w) > 1 and w.isalpha()
            ]
        else:
            words_cleaned = [
                w.lower() 
                for w in words 
                if w not in ignore_words and len(w) > 1 and w.isalpha()
            ]
        
        # Filtrage des mots rares (sauf mots-clés importants)
        mots_cles = ['ailicia', 'texttospeech', 'obscapture', 'simultanement', 'plusieurspc']
        word_freq = Counter(words_cleaned)
        words_filtered = [
            word for word, freq in word_freq.items()
            if freq >= 2 or word in mots_cles
        ]
        
        words = sorted(list(set(words_filtered)))
        classes = sorted(list(set(classes)))
        
        # Mise à jour des métriques
        metrics.vocabulary_size = len(words)
        metrics.valid_tags = len(classes)
        metrics.total_patterns = sum(len(d['patterns']) for d in donnees_tags.values())
        
        self.logger.info(f"📊 Vocabulaire: {len(words)} mots")
        self.logger.info(f"📊 Classes: {len(classes)} tags")
        self.logger.info(f"📊 Documents: {len(documents)} exemples")
        
        # Création des données d'entraînement
        training_data = []
        output_empty = [0] * len(classes)
        
        for doc in documents:
            bag = []
            pattern_words = doc[0]
            
            if self.lemmatizer:
                pattern_words = [self.lemmatizer.lemmatize(w.lower()) for w in pattern_words]
            else:
                pattern_words = [w.lower() for w in pattern_words]
            
            # Bag of words avec pondération
            for w in words:
                count = pattern_words.count(w)
                if count > 0:
                    # Boost pour les mots-clés importants
                    if w in mots_cles:
                        bag.append(min(1.5, count * 0.8))
                    else:
                        bag.append(min(1.0, count * 0.6))
                else:
                    bag.append(0.0)
            
            # Output vector
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1
            training_data.append([bag, output_row])
        
        # Préparation finale des données
        random.shuffle(training_data)
        train_x = np.array([item[0] for item in training_data], dtype=np.float32)
        train_y = np.array([item[1] for item in training_data], dtype=np.float32)
        
        self.logger.info(f"🏋️ Données préparées: X={train_x.shape}, Y={train_y.shape}")
        
        # Construction du modèle optimisé
        model = Sequential([
            Input(shape=(len(train_x[0]),)),
            Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Dropout(0.4),
            
            Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Dropout(0.3),
            
            Dense(128, activation='relu'),
            Dropout(0.2),
            
            Dense(64, activation='relu'),
            Dropout(0.1),
            
            Dense(len(train_y[0]), activation='softmax')
        ])
        
        # Compilation
        optimizer = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999)
        model.compile(
            loss='categorical_crossentropy',
            optimizer=optimizer,
            metrics=['accuracy']
        )
        
        # Callbacks pour un entraînement optimal
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=50,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=20,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        self.logger.info("🚀 Lancement de l'entraînement...")
        
        # Entraînement
        history = model.fit(
            train_x, train_y,
            epochs=300,
            batch_size=8,
            verbose=1,
            validation_split=0.2,
            callbacks=callbacks
        )
        
        # Mise à jour des métriques finales
        final_loss, final_accuracy = model.evaluate(train_x, train_y, verbose=0)
        metrics.model_accuracy = final_accuracy
        metrics.training_loss = final_loss
        metrics.epochs_completed = len(history.history['loss'])
        metrics.end_time = time.time()
        
        self.logger.info("✅ Entraînement terminé")
        self.logger.info(f"📊 Précision finale: {final_accuracy:.4f}")
        self.logger.info(f"📊 Perte finale: {final_loss:.4f}")
        self.logger.info(f"📊 Epochs: {metrics.epochs_completed}")
        self.logger.info(f"📊 Durée: {metrics.duration:.2f}s")
        
        return words, classes, model, metrics

def main():
    """Fonction principale d'entraînement améliorée"""
    print("=" * 90)
    print("🚀 MILA ASSIST - ENTRAÎNEMENT VERSION 2.0 (GESTION BACKUPS INTELLIGENTE)")
    print("=" * 90)
    print("📚 Concepteur Développeur d'Applications - Niveau 6")
    print("🎯 Entraînement du modèle Keras depuis la base de données")
    print("⚡ Mise à jour automatique des fichiers avec gestion intelligente des backups")
    print("🗑️ Suppression automatique des anciennes versions (limite: 3 backups)")
    print()
    
    # Vérification des dépendances
    if not TENSORFLOW_AVAILABLE:
        print("❌ TensorFlow requis pour l'entraînement")
        print("💡 Installez avec: pip install tensorflow")
        return False
    
    if not NLTK_AVAILABLE:
        print("⚠️ NLTK non disponible - utilisation de la tokenisation simple")
    
    try:
        # Initialisation des composants
        config = ConfigurationManager()
        
        # Configuration du logging
        training_logger = TrainingLogger()
        logger = logging.getLogger(__name__)
        
        # Initialisation des gestionnaires
        api_client = APIClient(config)
        data_processor = DataProcessor(debug=config.DEBUG)
        model_trainer = ModelTrainer(config)
        backup_manager = BackupManager(
            os.path.dirname(os.path.abspath(__file__)),
            max_backups=config.MAX_BACKUPS
        )
        
        logger.info(f"🔧 Configuration:")
        logger.info(f"   - API URL: {config.API_URL}")
        logger.info(f"   - Utiliser API: {config.USE_API}")
        logger.info(f"   - Fallback activé: {config.USE_LEGACY_FALLBACK}")
        logger.info(f"   - Mode debug: {config.DEBUG}")
        logger.info(f"   - Max backups: {config.MAX_BACKUPS}")
        logger.info(f"   - Validation croisée: {config.ENABLE_CROSS_VALIDATION}")
        
        if not config.USE_LEGACY_FALLBACK:
            logger.warning("Le fallback Keras est désactivé - entraînement tout de même effectué")
        
        # Affichage de l'état des backups
        backup_summary = backup_manager.get_backup_summary()
        print("\n📊 État actuel des backups:")
        for backup_type, count in backup_summary.items():
            print(f"   - {backup_type}: {count} fichiers")
        print()
        
        # Test de connexion API
        if config.USE_API:
            logger.info("🔍 Test de connexion à l'API...")
            if api_client.test_connection():
                logger.info("✅ API accessible")
            else:
                logger.error("❌ API non accessible")
                logger.error("💡 Vérifiez que l'API fonctionne sur le NAS")
                return False
        else:
            logger.warning("API désactivée dans la configuration")
            return False
        
        # Initialisation des métriques
        metrics = TrainingMetrics(start_time=time.time())
        
        # Récupération des données
        connaissances = api_client.recuperer_toutes_connaissances()
        if not connaissances:
            logger.error("Aucune donnée récupérée - impossible d'entraîner")
            return False
        
        metrics.total_knowledge = len(connaissances)
        
        # Traitement des données
        donnees_tags = data_processor.convertir_donnees_vers_format_entrainement(connaissances)
        donnees_augmentees = data_processor.augmenter_donnees(donnees_tags)
        
        # Calcul du facteur d'augmentation
        patterns_avant = sum(len(d['patterns']) for d in donnees_tags.values())
        patterns_après = sum(len(d['patterns']) for d in donnees_augmentees.values())
        metrics.data_augmentation_factor = patterns_après / patterns_avant if patterns_avant > 0 else 1.0
        
        # Sauvegarde des fichiers existants
        logger.info("💾 Sauvegarde des fichiers existants...")
        backup_manager.backup_model()
        backup_manager.backup_vocabulary_files()
        
        # Entraînement du modèle
        words, classes, model, training_metrics = model_trainer.entrainer_modele(donnees_augmentees)
        
        if not words or not classes:
            logger.error("Erreur lors de l'entraînement")
            return False
        
        # Fusion des métriques
        metrics.end_time = training_metrics.end_time
        metrics.valid_tags = training_metrics.valid_tags
        metrics.vocabulary_size = training_metrics.vocabulary_size
        metrics.total_patterns = training_metrics.total_patterns
        metrics.model_accuracy = training_metrics.model_accuracy
        metrics.training_loss = training_metrics.training_loss
        metrics.epochs_completed = training_metrics.epochs_completed
        
        # Sauvegarde des nouveaux fichiers
        logger.info("💾 Sauvegarde des nouveaux fichiers...")
        
        # Sauvegarde du modèle
        if model is not None:
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_model.keras")
            model.save(model_path)
            logger.info(f"💾 Nouveau modèle sauvegardé: {model_path}")
        
        # Sauvegarde des vocabulaires
        base_dir = os.path.dirname(os.path.abspath(__file__))
        for filename, data in [("words.pkl", words), ("classes.pkl", classes)]:
            file_path = os.path.join(base_dir, filename)
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            logger.info(f"📄 Nouveau {filename} créé")
        
        # Sauvegarde des patterns et métriques
        backup_manager.backup_training_patterns(donnees_augmentees)
        backup_manager.backup_metrics(metrics)
        
        # Sauvegarde des métriques dans l'historique
        training_logger.log_metrics(metrics)
        
        # Résumé final des backups après nettoyage
        final_backup_summary = backup_manager.get_backup_summary()
        
        # Résumé final
        print("\n" + "=" * 90)
        print("✅ ENTRAÎNEMENT VERSION 2.0 TERMINÉ AVEC SUCCÈS!")
        print("=" * 90)
        print(f"📊 Connaissances utilisées: {metrics.total_knowledge}")
        print(f"📊 Tags d'entraînement: {metrics.valid_tags}")
        print(f"📊 Vocabulaire: {metrics.vocabulary_size} mots")
        print(f"📊 Patterns total: {metrics.total_patterns}")
        print(f"📊 Facteur d'augmentation: {metrics.data_augmentation_factor:.2f}x")
        print(f"📊 Précision finale: {metrics.model_accuracy:.4f}")
        print(f"📊 Durée totale: {metrics.duration:.2f} secondes")
        print(f"📊 Epochs complétés: {metrics.epochs_completed}")
        
        print("\n📁 Fichiers mis à jour:")
        print("   ✅ chatbot_model.keras (modèle Keras entraîné)")
        print("   ✅ words.pkl (vocabulaire à jour)")
        print("   ✅ classes.pkl (classes à jour)")
        print("   ✅ training_patterns.pkl (patterns de fallback)")
        
        print("\n🗃️ Gestion des backups (max 3 versions):")
        for backup_type, count in final_backup_summary.items():
            print(f"   📦 {backup_type}: {count} versions conservées")
        
        print("\n💡 Le chatbot peut maintenant utiliser le modèle mis à jour!")
        print("🔄 Redémarrez l'application pour prendre en compte les changements")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Entraînement interrompu par l'utilisateur")
        return False
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur lors de l'entraînement: {e}")
        if hasattr(config, 'DEBUG') and config.DEBUG:
            import traceback
            traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
