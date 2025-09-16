#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MILA ASSIST - APPLICATION PRINCIPALE AVEC CHARGEMENT ASYNCHRONE
==============================================================

VERSION RNCP 6 CDA

Améliorations VERSION ASYNCHRONE:
- Chargement asynchrone du modèle Keras sans bloquer l'interface
- Route /model_status pour suivre l'état du chargement
- Démarrage instantané de l'application
- Interface utilisateur non bloquante
- Basculement transparent vers le fallback local
- Reformulation désactivée (réponses directes seulement)

Fonctionnalités:
- Chatbot avec fallback API → Keras intelligent et asynchrone
- Interface web responsive et accessible
- Gestion des sessions utilisateur
- Système de feedback et amélioration continue
- Monitoring temps réel des performances et du chargement

Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import os
import sys
import signal
import time
import threading
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

from flask import Flask, render_template, request, jsonify, g
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

# Import des couches métier avec gestion d'erreur
try:
    from services.chatbot_service import ChatbotService
    from services.session_service import SessionService
    from services.feedback_service import FeedbackService
    from config.app_config import AppConfig, ConfigurationError
except ImportError as e:
    print(f"❌ Erreur d'import des modules: {e}")
    print("💡 Vérifiez que tous les fichiers sont présents et que les dépendances sont installées")
    sys.exit(1)

# Configuration du logging
def setup_logging(debug: bool = False, log_file: str = None):
    """Configuration du système de logging"""
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Format de log professionnel
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configuration du logger racine
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Handler fichier si spécifié
    if log_file:
        try:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            logging.warning(f"Impossible de créer le fichier de log {log_file}: {e}")
    
    # Réduire le bruit des libraries externes
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)

class MilaAssistApp:
    """Application principale Mila Assist - VERSION SANS REFORMULATION"""
    
    def __init__(self):
        """Initialisation de l'application avec gestion d'erreur robuste"""
        self.app = None
        self.config = None
        self.services = {}
        self.running = False
        self.startup_time = datetime.now()
        
        try:
            self._initialize_application()
        except Exception as e:
            logging.error(f"❌ Erreur fatale lors de l'initialisation: {e}")
            if hasattr(self, 'config') and self.config and self.config.DEBUG:
                traceback.print_exc()
            raise
    
    def _initialize_application(self):
        """Initialisation complète de l'application"""
        logging.info("🚀 Initialisation de Mila Assist - Version RNCP 6 (Asynchrone, sans reformulation)")
        
        # 1. Chargement de la configuration
        self._load_configuration()
        
        # 2. Configuration du logging avancé
        log_file = os.path.join(self.config.BASE_DIR, 'logs', 'mila_assist.log') if self.config.is_production() else None
        setup_logging(self.config.DEBUG, log_file)
        
        # 3. Création de l'application Flask
        self._create_flask_app()
        
        # 4. Initialisation des services métier (INSTANTANÉ)
        self._initialize_services()
        
        # 5. Enregistrement des routes
        self._register_routes()
        
        # 6. Configuration des gestionnaires d'événements
        self._setup_event_handlers()
        
        logging.info("✅ Application initialisée avec succès (mode asynchrone, reformulation désactivée)")
        self._log_startup_summary()
    
    def _load_configuration(self):
        """Chargement et validation de la configuration"""
        try:
            self.config = AppConfig()
            logging.info("🔧 Configuration chargée et validée")
        except ConfigurationError as e:
            logging.error(f"❌ Erreur de configuration: {e}")
            raise
        except Exception as e:
            logging.error(f"❌ Erreur inattendue lors du chargement de la configuration: {e}")
            raise
    
    def _create_flask_app(self):
        """Création et configuration de l'application Flask"""
        self.app = Flask(__name__)
        
        # Configuration Flask
        self.app.config.update({
            'SECRET_KEY': self.config.SECRET_KEY,
            'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max
            'JSON_AS_ASCII': False,  # Support Unicode
            'JSONIFY_PRETTYPRINT_REGULAR': self.config.DEBUG
        })
        
        # Configuration de sécurité pour la production
        if self.config.is_production():
            self.app.config.update({
                'SESSION_COOKIE_SECURE': True,
                'SESSION_COOKIE_HTTPONLY': True,
                'SESSION_COOKIE_SAMESITE': 'Lax'
            })
        
        logging.info("🌐 Application Flask configurée")
    
    def _initialize_services(self):
        """Initialisation INSTANTANÉE des services métier avec chargement asynchrone"""
        try:
            # Service chatbot principal (DÉMARRAGE INSTANTANÉ avec chargement asynchrone)
            logging.info("⚡ Initialisation instantanée du service chatbot (sans reformulation)...")
            self.services['chatbot'] = ChatbotService(self.config)
            
            # Service de gestion des sessions
            self.services['session'] = SessionService()
            
            # Service de feedback utilisateur
            self.services['feedback'] = FeedbackService(self.config)
            
            logging.info("✅ Services métier initialisés instantanément")
            logging.info("🔄 Le modèle Keras se charge en arrière-plan si activé")
            logging.info("🚫 Reformulation désactivée - réponses directes uniquement")
            
        except Exception as e:
            logging.error(f"❌ Erreur lors de l'initialisation des services: {e}")
            raise
    
    def _setup_event_handlers(self):
        """Configuration des gestionnaires d'événements système"""
        def signal_handler(sig, frame):
            logging.info("🛑 Signal d'arrêt reçu, fermeture en cours...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Gestionnaire avant requête
        @self.app.before_request
        def before_request():
            g.request_start_time = time.time()
            g.request_id = f"{int(time.time()*1000)}{os.getpid()}"
        
        # Gestionnaire après requête
        @self.app.after_request
        def after_request(response):
            if hasattr(g, 'request_start_time'):
                response_time = (time.time() - g.request_start_time) * 1000
                response.headers['X-Response-Time'] = f"{response_time:.2f}ms"
                
                if response_time > 1000:  # Log les requêtes lentes
                    logging.warning(f"⏱️ Requête lente: {request.endpoint} - {response_time:.2f}ms")
            
            response.headers['X-Powered-By'] = 'Mila-Assist-RNCP6-NoReformat'
            return response
    
    def _register_routes(self):
        """Enregistrement des routes simplifiées (sans gestion des modes)"""
        
        @self.app.route("/")
        def home():
            """Page d'accueil du chatbot"""
            try:
                return render_template("index.html")
            except Exception as e:
                logging.error(f"Erreur page d'accueil: {e}")
                return "Erreur lors du chargement de la page", 500
        
        @self.app.route("/model_status", methods=["GET"])
        def model_status():
            """NOUVELLE ROUTE: Statut du modèle Keras pour l'interface"""
            try:
                status_info = self.services['chatbot'].get_model_status()
                return jsonify(status_info)
            except Exception as e:
                logging.error(f"Erreur récupération statut modèle: {e}")
                return jsonify({
                    "status": "error",
                    "message": "Erreur lors de la récupération du statut",
                    "error": str(e)
                }), 500
        
        @self.app.route("/get", methods=["POST"])
        def get_response():
            """Obtenir une réponse du chatbot avec validation complète - SANS REFORMULATION"""
            try:
                # Validation des données d'entrée
                message = request.form.get("msg", "").strip()
                session_id = request.form.get("session_id", "").strip()
                
                if not message:
                    return self._create_error_response("Message vide non autorisé", 400)
                
                if len(message) > 500:
                    return self._create_error_response("Message trop long (maximum 500 caractères)", 400)
                
                # Gestion de la session
                if not session_id or not self.services['session'].is_valid_session(session_id):
                    session_id = self.services['session'].create_session()
                    logging.info(f"Nouvelle session créée: {session_id[:12]}...")
                
                # Traitement de la requête (INSTANTANÉ même si le modèle charge)
                start_time = time.time()
                reponse = self.services['chatbot'].obtenir_reponse(message, session_id)
                response_time = (time.time() - start_time) * 1000
                
                # Vérification que la réponse n'est jamais None ou vide
                if not reponse or reponse.strip() == "":
                    logging.warning(f"⚠️ Réponse vide reçue du chatbot - fallback appliqué")
                    reponse = "Désolé, je n'ai pas pu traiter votre demande. Veuillez réessayer."
                
                # Mise à jour des statistiques de session
                self.services['session'].update_session_activity(session_id, response_time)
                
                # Log de performance
                if response_time > 2000:
                    logging.warning(f"⏱️ Réponse lente du chatbot: {response_time:.2f}ms")
                
                logging.info(f"✅ Réponse générée en {response_time:.2f}ms pour session {session_id[:12]}... (direct, sans reformulation)")
                
                return reponse
                
            except Exception as e:
                logging.error(f"Erreur dans get_response: {e}")
                return self._create_error_response("Erreur interne du chatbot", 500)
        
        @self.app.route("/feedback", methods=["POST"])
        def submit_feedback():
            """Soumettre un feedback utilisateur avec validation"""
            try:
                question = request.form.get("question", "").strip()
                reponse_attendue = request.form.get("expected", "").strip()
                reponse_actuelle = request.form.get("current_response", "").strip()
                
                # Validation
                if not question or not reponse_attendue:
                    return self._create_error_response("Question et réponse attendue requises", 400)
                
                if len(question) > 500:
                    return self._create_error_response("Question trop longue", 400)
                
                if len(reponse_attendue) > 1000:
                    return self._create_error_response("Réponse attendue trop longue", 400)
                
                # Traitement asynchrone du feedback
                def process_feedback():
                    try:
                        success = self.services['feedback'].soumettre_feedback(
                            question, reponse_attendue, reponse_actuelle
                        )
                        if success:
                            logging.info(f"📝 Feedback traité: {question[:50]}...")
                        else:
                            logging.warning("⚠️ Échec traitement feedback")
                    except Exception as e:
                        logging.error(f"Erreur traitement feedback asynchrone: {e}")
                
                # Lancer le traitement en arrière-plan
                thread = threading.Thread(target=process_feedback)
                thread.daemon = True
                thread.start()
                
                return "Feedback enregistré avec succès. Merci pour votre contribution !"
                
            except Exception as e:
                logging.error(f"Erreur dans submit_feedback: {e}")
                return self._create_error_response("Erreur lors du traitement du feedback", 500)
        
        # ROUTES DES MODES SUPPRIMÉES - La reformulation est désactivée
        # Plus besoin de /set_mode, /modes_info car pas de reformulation
        
        @self.app.route("/stats", methods=["GET"])
        def get_stats():
            """Obtenir les statistiques complètes du système"""
            try:
                # Statistiques des services
                chatbot_stats = self.services['chatbot'].obtenir_statistiques()
                session_stats = self.services['session'].get_session_stats()
                feedback_stats = self.services['feedback'].obtenir_statistiques_feedbacks()
                
                # Statistiques de l'application
                app_uptime = datetime.now() - self.startup_time
                
                return f"""
                <h2>📊 Statistiques Mila Assist - Version RNCP 6 Asynchrone (Sans Reformulation)</h2>
                
                <h3>🖥️ Application</h3>
                <p>Version: RNCP 6 Asynchrone - Sans Reformulation</p>
                <p>Uptime: {str(app_uptime).split('.')[0]}</p>
                <p>Environnement: {self.config.ENV_TYPE}</p>
                <p>Mode debug: {'Activé' if self.config.DEBUG else 'Désactivé'}</p>
                
                <h3>🤖 Chatbot (Mode Asynchrone - Réponses Directes)</h3>
                <p>Messages traités: {chatbot_stats.get('messages_traites', 0)}</p>
                <p>Temps de réponse moyen: {chatbot_stats.get('temps_reponse_moyen', 0):.2f}ms</p>
                <p>Mode actuel: {chatbot_stats.get('mode_actuel', 'N/A')}</p>
                <p>Reformulation active: {'✅' if chatbot_stats.get('reformulation_active', False) else '🚫 DÉSACTIVÉE'}</p>
                <p>Statut modèle: {chatbot_stats.get('model_status', 'N/A')}</p>
                <p>Temps chargement modèle: {chatbot_stats.get('model_loading_time', 0):.2f}s</p>
                <p>API connectée: {'✅' if chatbot_stats.get('api_connectee') else '❌'}</p>
                <p>Succès API: {chatbot_stats.get('api_success', 0)}</p>
                <p>Échecs API: {chatbot_stats.get('api_failures', 0)}</p>
                <p>Fallback Keras utilisé: {chatbot_stats.get('keras_fallback_used', 0)} fois</p>
                <p>Requêtes pendant chargement: {chatbot_stats.get('requests_during_loading', 0)}</p>
                <p>API utilisée pendant chargement: {chatbot_stats.get('taux_api_pendant_chargement', 0)}%</p>
                <p>Chargement asynchrone: {'✅ Activé' if chatbot_stats.get('chargement_asynchrone') else '❌'}</p>
                
                <h3>🔗 Sessions</h3>
                <p>Sessions actives: {self.services['session'].get_active_sessions_count()}</p>
                <p>Messages total: {session_stats.get('total_messages', 0)}</p>
                <p>Durée moyenne session: {session_stats.get('average_session_duration', 0):.1f}s</p>
                
                <h3>💬 Feedbacks</h3>
                <p>Total feedbacks: {feedback_stats.get('total_feedbacks', 0)}</p>
                <p>Mode: {feedback_stats.get('mode', 'N/A')}</p>
                
                <h3>🔧 Configuration</h3>
                <p>Base de données: {chatbot_stats.get('db_connectee', 'N/A')}</p>
                <p>TensorFlow: {'✅' if chatbot_stats.get('tensorflow_disponible') else '❌'}</p>
                <p>NLTK: {'✅' if chatbot_stats.get('nltk_disponible') else '❌'}</p>
                <p>Modèle local: {'✅' if chatbot_stats.get('modele_local_charge') else '❌'}</p>
                """
            except Exception as e:
                logging.error(f"Erreur dans get_stats: {e}")
                return "<p>Erreur lors de la récupération des statistiques</p>", 500
        
        @self.app.route("/health", methods=["GET"])
        def health_check():
            """Point de santé complet de l'application"""
            try:
                # Test des services
                api_connected = self.services['chatbot'].test_api_connection()
                model_status_info = self.services['chatbot'].get_model_status()
                
                # Calcul du statut global
                status = "healthy"
                if not api_connected and not model_status_info['is_ready']:
                    if model_status_info['status'] == 'loading':
                        status = "initializing"
                    else:
                        status = "degraded"
                elif not api_connected or not model_status_info['is_ready']:
                    status = "partial"
                
                return jsonify({
                    "status": status,
                    "timestamp": datetime.now().isoformat(),
                    "version": "2.0-RNCP6-Async-NoReformat",
                    "environment": self.config.ENV_TYPE,
                    "uptime_seconds": int((datetime.now() - self.startup_time).total_seconds()),
                    "services": {
                        "api_connected": api_connected,
                        "model_status": model_status_info['status'],
                        "model_ready": model_status_info['is_ready'],
                        "sessions_active": self.services['session'].get_active_sessions_count()
                    },
                    "configuration": {
                        "use_api": self.config.USE_API,
                        "use_fallback": self.config.USE_LEGACY_FALLBACK,
                        "response_mode": "direct",  # Plus de modes de reformulation
                        "reformulation_enabled": False,  # NOUVEAU: indique que c'est désactivé
                        "debug": self.config.DEBUG,
                        "async_loading": True
                    },
                    "model_info": model_status_info
                })
            except Exception as e:
                logging.error(f"Erreur health check: {e}")
                return jsonify({
                    "status": "error", 
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }), 500
        
        @self.app.route("/quit", methods=["POST"])
        def quit_app():
            """Fermer l'application proprement"""
            try:
                logging.info("🛑 Demande d'arrêt de l'application reçue")
                
                def shutdown_server():
                    time.sleep(1)  # Attendre que la réponse soit envoyée
                    self.shutdown()
                    os._exit(0)
                
                thread = threading.Thread(target=shutdown_server)
                thread.daemon = True
                thread.start()
                
                return "Application en cours de fermeture... Merci d'avoir utilisé Mila Assist !", 200
                
            except Exception as e:
                logging.error(f"Erreur lors de la fermeture: {e}")
                return "Erreur lors de la fermeture.", 500
        
        # Gestionnaires d'erreurs personnalisés
        @self.app.errorhandler(400)
        def bad_request(error):
            return self._create_error_response("Requête invalide", 400)
        
        @self.app.errorhandler(404)
        def not_found(error):
            return self._create_error_response("Page non trouvée", 404)
        
        @self.app.errorhandler(500)
        def internal_error(error):
            logging.error(f"Erreur 500: {error}")
            return self._create_error_response("Erreur interne du serveur", 500)
        
        logging.info("🛣️ Routes enregistrées avec succès (sans gestion des modes de reformulation)")
    
    def _create_error_response(self, message: str, status_code: int) -> tuple:
        """Créer une réponse d'erreur structurée"""
        if request.is_json or 'application/json' in request.headers.get('Accept', ''):
            return jsonify({
                "error": message,
                "status": status_code,
                "timestamp": datetime.now().isoformat()
            }), status_code
        else:
            return message, status_code
    
    def _log_startup_summary(self):
        """Logger le résumé du démarrage"""
        logging.info("=" * 70)
        logging.info("🎯 MILA ASSIST - DÉMARRAGE RÉUSSI (MODE ASYNCHRONE SANS REFORMULATION)")
        logging.info("=" * 70)
        logging.info(f"📍 Version: RNCP 6 - Concepteur Développeur d'Applications (Async No-Reformat)")
        logging.info(f"🌐 URL: http://{self.config.HOST}:{self.config.PORT}")
        logging.info(f"🔧 Environnement: {self.config.ENV_TYPE}")
        logging.info(f"🚫 Reformulation: DÉSACTIVÉE (réponses directes)")
        logging.info(f"🔗 API externe: {'✅ Activée' if self.config.USE_API else '❌ Désactivée'}")
        logging.info(f"🧮 Fallback Keras: {'✅ Chargement asynchrone' if self.config.USE_LEGACY_FALLBACK else '❌ Désactivé'}")
        logging.info(f"⚡ Démarrage instantané: Interface utilisable immédiatement")
        logging.info(f"🔄 Modèle local: Se charge en arrière-plan sans bloquer")
        logging.info("=" * 70)
    
    def shutdown(self):
        """Fermeture propre de l'application"""
        try:
            self.running = False
            logging.info("🔄 Fermeture des services...")
            
            # Fermer les services dans l'ordre inverse
            for service_name in reversed(list(self.services.keys())):
                service = self.services[service_name]
                if hasattr(service, 'fermer'):
                    try:
                        service.fermer()
                        logging.info(f"✅ Service {service_name} fermé")
                    except Exception as e:
                        logging.warning(f"⚠️ Erreur fermeture service {service_name}: {e}")
            
            # Nettoyer les sessions expirées
            try:
                if 'session' in self.services:
                    self.services['session'].cleanup_expired_sessions()
            except Exception as e:
                logging.warning(f"⚠️ Erreur nettoyage sessions: {e}")
            
            uptime = datetime.now() - self.startup_time
            logging.info(f"✅ Application fermée proprement après {uptime} (sans reformulation)")
            
        except Exception as e:
            logging.error(f"Erreur lors de la fermeture: {e}")
    
    def run(self, host: str = None, port: int = None, debug: bool = None):
        """Lancer l'application Flask avec configuration optimisée"""
        
        # Utiliser la configuration si les paramètres ne sont pas fournis
        host = host or self.config.HOST
        port = port or self.config.PORT
        debug = debug if debug is not None else self.config.DEBUG
        
        logging.info(f"🚀 Démarrage du serveur sur {host}:{port} (mode asynchrone, sans reformulation)")
        logging.info(f"🔧 Mode debug: {debug}")
        
        self.running = True
        
        try:
            # Configuration pour la production
            if self.config.is_production():
                logging.info("🛡️ Configuration de production activée")
                self.app.run(
                    host=host, 
                    port=port, 
                    debug=False,  # Toujours False en production
                    use_reloader=False,
                    threaded=True
                )
            else:
                # Configuration pour le développement
                self.app.run(
                    host=host, 
                    port=port, 
                    debug=debug, 
                    use_reloader=False,  # Éviter les conflits avec nos services
                    threaded=True
                )
                
        except KeyboardInterrupt:
            logging.info("🛑 Interruption clavier reçue")
            self.shutdown()
        except Exception as e:
            logging.error(f"❌ Erreur lors du démarrage du serveur: {e}")
            self.shutdown()
            raise

def create_app() -> MilaAssistApp:
    """Factory pour créer l'application - Pattern recommandé pour RNCP 6"""
    try:
        return MilaAssistApp()
    except Exception as e:
        logging.error(f"❌ Erreur fatale lors de la création de l'application: {e}")
        raise

def main():
    """Fonction principale pour le lancement direct"""
    try:
        # Banner de démarrage
        print("=" * 80)
        print("🚀 MILA ASSIST - ASSISTANT VIRTUEL POUR STREAMEUR")
        print("🎓 Version RNCP 6 - Concepteur Développeur d'Applications (Asynchrone)")
        print("⚡ Démarrage instantané avec chargement asynchrone du modèle")
        print("🚫 Reformulation désactivée - Réponses directes uniquement")
        print("=" * 80)
        
        app_instance = create_app()
        
        # Configuration depuis les variables d'environnement
        HOST = os.getenv('HOST', app_instance.config.HOST)
        PORT = int(os.getenv('PORT', app_instance.config.PORT))
        DEBUG = os.getenv('DEBUG', str(app_instance.config.DEBUG)).lower() == 'true'
        
        app_instance.run(host=HOST, port=PORT, debug=DEBUG)
        
    except KeyboardInterrupt:
        logging.info("Application interrompue par l'utilisateur")
    except ConfigurationError as e:
        logging.error(f"Erreur de configuration: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Erreur fatale: {e}")
        if '--debug' in sys.argv:
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()