#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONFIGURATION CENTRALISÉE POUR MILA ASSIST - VERSION RNCP 6
===================================================================

Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import os
import secrets
import logging
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from pathlib import Path

# Charger le fichier .env si présent
load_dotenv()

logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Exception levée en cas d'erreur de configuration"""
    pass

class AppConfig:
    """Configuration centralisée et sécurisée de l'application"""
    
    # Valeurs par défaut sécurisées
    DEFAULT_VALUES = {
        'HOST': 'localhost',
        'PORT': 5000,
        'DEBUG': False,
        'USE_API': True,
        'USE_DB': False,  # Par défaut, utiliser uniquement l'API
        'USE_LEGACY_FALLBACK': True,
        'API_TIMEOUT': 1,  # Timeout ultra-court (1s) pour bascule instantanée
        'MYSQL_PORT': 3306
    }
    
    # Configuration de sécurité
    SECURITY_CONFIG = {
        'MIN_SECRET_KEY_LENGTH': 32,
        'REQUIRED_API_KEY_LENGTH': 16,
        'MAX_API_TIMEOUT': 60,
        'ALLOWED_HOSTS': ['localhost', '127.0.0.1', '0.0.0.0']
    }
    
    def __init__(self):
        """Initialisation avec validation complète"""
        # Configuration de base
        self.BASE_DIR = self._get_base_directory()
        self.ENV_TYPE = self._detect_environment_type()
        
        # Sécurité et authentification
        self.SECRET_KEY = self._load_secret_key()
        self.API_KEY = self._load_api_key()
        
        # Configuration API externe
        self.USE_API = self._load_boolean('USE_API', self.DEFAULT_VALUES['USE_API'])
        self.API_URL = self._load_api_url()
        self.API_TIMEOUT = self._load_integer('API_TIMEOUT', self.DEFAULT_VALUES['API_TIMEOUT'], 1, 60)
        
        # Configuration serveur
        self.HOST = self._load_host()
        self.PORT = self._load_port()
        self.DEBUG = self._load_boolean('DEBUG', self.DEFAULT_VALUES['DEBUG'])
        
        # Configuration base de données MySQL (via API)
        self.USE_DB = self._load_boolean('USE_DB', self.DEFAULT_VALUES['USE_DB'])
        self.MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
        self.MYSQL_PORT = self._load_integer('MYSQL_PORT', self.DEFAULT_VALUES['MYSQL_PORT'], 1, 65535)
        self.MYSQL_USER = os.getenv('MYSQL_USER', 'chatbot_user')
        self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
        self.MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'mila_assist_db')
        
        # Configuration chatbot (reformulation désactivée)
        self.USE_LEGACY_FALLBACK = self._load_boolean('USE_LEGACY_FALLBACK', self.DEFAULT_VALUES['USE_LEGACY_FALLBACK'])
        
        # Mode réponse pour évolution future (LLM en conteneur)
        self.RESPONSE_MODE = "simple"  # Prêt pour "reformulation" avec LLM
        
        # Chemins des fichiers du modèle
        self._initialize_model_paths()
        
        # Validation finale de la configuration
        self._validate_configuration()
        
        # Log de la configuration (sans les secrets)
        self._log_configuration_summary()
    
    def _get_base_directory(self) -> str:
        """Obtenir le répertoire de base de l'application"""
        return str(Path(__file__).parent.parent.absolute())
    
    def _detect_environment_type(self) -> str:
        """Détecter le type d'environnement (dev/test/prod)"""
        env = os.getenv('ENVIRONMENT', '').lower()
        if env in ['production', 'prod']:
            return 'production'
        elif env in ['test', 'testing']:
            return 'test'
        else:
            return 'development'
    
    def _load_boolean(self, key: str, default: bool) -> bool:
        """Charger une valeur booléenne avec validation"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def _load_integer(self, key: str, default: int, min_val: int = None, max_val: int = None) -> int:
        """Charger une valeur entière avec validation"""
        try:
            value = int(os.getenv(key, str(default)))
            if min_val is not None and value < min_val:
                raise ConfigurationError(f"{key} doit être >= {min_val}, reçu: {value}")
            if max_val is not None and value > max_val:
                raise ConfigurationError(f"{key} doit être <= {max_val}, reçu: {value}")
            return value
        except ValueError:
            raise ConfigurationError(f"Valeur invalide pour {key}: {os.getenv(key)}")
    
    def _load_secret_key(self) -> str:
        """Charger ou générer la clé secrète avec validation de sécurité"""
        secret_key = os.getenv('SECRET_KEY')
        
        if not secret_key:
            # Générer une clé secrète sécurisée
            secret_key = secrets.token_hex(32)
            logger.warning("🔐 Clé secrète générée automatiquement - configurez SECRET_KEY dans .env pour la production")
        
        if len(secret_key) < self.SECURITY_CONFIG['MIN_SECRET_KEY_LENGTH']:
            raise ConfigurationError(
                f"SECRET_KEY trop courte (minimum {self.SECURITY_CONFIG['MIN_SECRET_KEY_LENGTH']} caractères)"
            )
        
        return secret_key
    
    def _load_api_key(self) -> str:
        """Charger la clé API avec validation"""
        api_key = os.getenv('API_KEY') or os.getenv('DEFAULT_API_KEY', '')
        
        if not api_key:
            raise ConfigurationError("API_KEY ou DEFAULT_API_KEY est requis")
        
        if len(api_key) < self.SECURITY_CONFIG['REQUIRED_API_KEY_LENGTH']:
            raise ConfigurationError(
                f"API_KEY trop courte (minimum {self.SECURITY_CONFIG['REQUIRED_API_KEY_LENGTH']} caractères)"
            )
        
        return api_key
    
    def _load_api_url(self) -> str:
        """Charger et valider l'URL de l'API"""
        api_url = os.getenv('API_URL', '').strip()
        
        if not api_url:
            raise ConfigurationError("API_URL est requis dans la configuration")
        
        # Validation de base de l'URL
        if not api_url.startswith(('http://', 'https://')):
            raise ConfigurationError("API_URL doit commencer par http:// ou https://")
        
        # Supprimer le slash final s'il existe
        return api_url.rstrip('/')
    
    def _load_host(self) -> str:
        """Charger et valider l'adresse d'écoute"""
        host = os.getenv('HOST', self.DEFAULT_VALUES['HOST'])
        
        # Validation de sécurité pour la production
        if self.ENV_TYPE == 'production' and host not in self.SECURITY_CONFIG['ALLOWED_HOSTS']:
            logger.warning(f"⚠️ Host '{host}' en production - vérifiez la sécurité")
        
        return host
    
    def _load_port(self) -> int:
        """Charger et valider le port d'écoute"""
        port = self._load_integer('PORT', self.DEFAULT_VALUES['PORT'], 1, 65535)
        
        # Avertissement pour les ports privilégiés en production
        if self.ENV_TYPE == 'production' and port < 1024:
            logger.warning(f"⚠️ Port privilégié {port} en production")
        
        return port
    
    def _initialize_model_paths(self):
        """Initialiser les chemins des fichiers du modèle"""
        self.MODEL_PATH = os.path.join(self.BASE_DIR, "chatbot_model.keras")
        self.WORDS_PATH = os.path.join(self.BASE_DIR, "words.pkl")
        self.CLASSES_PATH = os.path.join(self.BASE_DIR, "classes.pkl")
        self.TRAINING_PATTERNS_PATH = os.path.join(self.BASE_DIR, "training_patterns.pkl")
        
        # Vérifier l'existence des fichiers si le fallback est activé
        if self.USE_LEGACY_FALLBACK:
            missing_files = []
            for path, name in [
                (self.MODEL_PATH, "chatbot_model.keras"),
                (self.WORDS_PATH, "words.pkl"),
                (self.CLASSES_PATH, "classes.pkl")
            ]:
                if not os.path.exists(path):
                    missing_files.append(name)
            
            if missing_files:
                logger.warning(
                    f"⚠️ Fichiers manquants pour le fallback Keras: {', '.join(missing_files)}"
                )
                logger.warning("💡 Exécutez train.py pour créer/mettre à jour le modèle")
    
    def _validate_configuration(self):
        """Validation finale de la cohérence de la configuration"""
        errors = []
        warnings = []
        
        # Validation de la cohérence USE_API / USE_DB
        if not self.USE_API and not self.USE_LEGACY_FALLBACK:
            errors.append("Impossible de désactiver à la fois USE_API et USE_LEGACY_FALLBACK")
        
        # Validation de la base de données
        if self.USE_DB and not self.MYSQL_PASSWORD:
            warnings.append("USE_DB=true mais MYSQL_PASSWORD vide")
        
        # Validation de l'environnement de production
        if self.ENV_TYPE == 'production':
            if self.DEBUG:
                warnings.append("DEBUG=true en production - risque de sécurité")
            
            if 'localhost' in self.API_URL or '127.0.0.1' in self.API_URL:
                warnings.append("API_URL utilise localhost en production")
        
        # Lever les erreurs critiques
        if errors:
            raise ConfigurationError(f"Erreurs de configuration: {'; '.join(errors)}")
        
        # Logger les avertissements
        for warning in warnings:
            logger.warning(f"⚠️ {warning}")
    
    def _log_configuration_summary(self):
        """Logger un résumé de la configuration (sans les secrets)"""
        if logger.isEnabledFor(logging.INFO):
            logger.info("🔧 Configuration Mila Assist chargée:")
            logger.info(f"   - Environnement: {self.ENV_TYPE}")
            logger.info(f"   - API URL: {self.API_URL}")
            logger.info(f"   - Utiliser API: {self.USE_API}")
            logger.info(f"   - Fallback Keras: {self.USE_LEGACY_FALLBACK}")
            logger.info(f"   - Mode réponse: {self.RESPONSE_MODE}")
            logger.info(f"   - Serveur: {self.HOST}:{self.PORT}")
            logger.info(f"   - Debug: {self.DEBUG}")
    
    def get_api_headers(self) -> Dict[str, str]:
        """Obtenir les en-têtes pour les requêtes API"""
        return {
            'Content-Type': 'application/json',
            'X-API-Key': self.API_KEY,
            'User-Agent': f'MilaAssist/2.0 ({self.ENV_TYPE})'
        }
    
    def is_production(self) -> bool:
        """Vérifier si on est en mode production"""
        return self.ENV_TYPE == 'production'
    
    def is_development(self) -> bool:
        """Vérifier si on est en mode développement"""
        return self.ENV_TYPE == 'development'
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé de la configuration (sans les secrets)"""
        return {
            # Configuration générale
            'environment': self.ENV_TYPE,
            'debug': self.DEBUG,
            'base_dir': self.BASE_DIR,
            
            # Configuration API
            'use_api': self.USE_API,
            'api_url': self.API_URL,
            'api_timeout': self.API_TIMEOUT,
            
            # Configuration serveur
            'host': self.HOST,
            'port': self.PORT,
            
            # Configuration chatbot
            'response_mode': self.RESPONSE_MODE,
            'use_legacy_fallback': self.USE_LEGACY_FALLBACK,
            
            # Configuration base de données
            'use_db': self.USE_DB,
            'mysql_host': self.MYSQL_HOST,
            'mysql_port': self.MYSQL_PORT,
            'mysql_database': self.MYSQL_DATABASE,
            
            # Fichiers du modèle
            'model_exists': os.path.exists(self.MODEL_PATH),
            'words_exists': os.path.exists(self.WORDS_PATH),
            'classes_exists': os.path.exists(self.CLASSES_PATH),
            'training_patterns_exists': os.path.exists(self.TRAINING_PATTERNS_PATH),
            
            # Informations de validation
            'config_valid': True,  # Si on arrive ici, la config est valide
            'security_level': 'high' if self.is_production() else 'standard'
        }
    
    def validate_model_files(self) -> Dict[str, bool]:
        """Valider l'existence des fichiers du modèle"""
        return {
            'model': os.path.exists(self.MODEL_PATH),
            'words': os.path.exists(self.WORDS_PATH),
            'classes': os.path.exists(self.CLASSES_PATH),
            'training_patterns': os.path.exists(self.TRAINING_PATTERNS_PATH)
        }
    
    def get_model_files_status(self) -> str:
        """Obtenir le statut des fichiers du modèle"""
        status = self.validate_model_files()
        
        if all(status.values()):
            return "✅ Tous les fichiers du modèle sont présents"
        elif status['model'] and status['words'] and status['classes']:
            return "⚠️ Fichiers de base présents, training_patterns.pkl manquant"
        else:
            missing = [name for name, exists in status.items() if not exists]
            return f"❌ Fichiers manquants: {', '.join(missing)}"
    
    def get_database_config(self) -> Optional[Dict[str, Any]]:
        """Obtenir la configuration de base de données (si activée)"""
        if not self.USE_DB:
            return None
        
        return {
            'host': self.MYSQL_HOST,
            'port': self.MYSQL_PORT,
            'user': self.MYSQL_USER,
            'password': '***masked***',  # Ne pas exposer le mot de passe
            'database': self.MYSQL_DATABASE,
            'charset': 'utf8mb4'
        }
    
    def get_security_info(self) -> Dict[str, Any]:
        """Obtenir les informations de sécurité (pour monitoring)"""
        return {
            'environment': self.ENV_TYPE,
            'debug_enabled': self.DEBUG,
            'api_key_length': len(self.API_KEY),
            'secret_key_length': len(self.SECRET_KEY),
            'api_url_secure': self.API_URL.startswith('https://'),
            'host_secure': self.HOST in self.SECURITY_CONFIG['ALLOWED_HOSTS'],
            'port_privileged': self.PORT < 1024
        }

# Instance globale pour compatibilité avec l'ancien code
def create_config() -> AppConfig:
    """Factory pour créer une instance de configuration"""
    try:
        return AppConfig()
    except ConfigurationError as e:
        logger.error(f"❌ Erreur de configuration: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Erreur inattendue lors de la configuration: {e}")
        raise ConfigurationError(f"Erreur inattendue: {e}")

# Pour compatibilité avec l'existant
def get_config() -> AppConfig:
    """Obtenir la configuration (singleton pattern)"""
    if not hasattr(get_config, '_instance'):
        get_config._instance = create_config()
    return get_config._instance