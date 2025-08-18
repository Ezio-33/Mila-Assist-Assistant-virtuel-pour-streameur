"""
API sécurisée pour le chatbot avec authentification et gestion des requêtes
Compatible avec la base de données vectorielle et l'architecture existante
"""

import os
import time
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from database import ChatbotDatabase, init_database
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
        self.db = None
        self.api_keys = self._load_api_keys()
        self._setup_routes()
        self._init_database()
    
    def _init_database(self):
        """Initialise la base de données"""
        try:
            self.db = init_database(migrate_intents=True)
            logger.info("Base de données initialisée pour l'API")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la DB: {e}")
            raise
    
    def _load_api_keys(self):
        """Charge les clés API depuis les variables d'environnement ou génère une clé par défaut"""
        api_keys = {}
        
        # Clé par défaut pour le développement (À CHANGER EN PRODUCTION)
        default_key = os.getenv('DEFAULT_API_KEY', 'dev_key_123456789')
        api_keys[hashlib.sha256(default_key.encode()).hexdigest()] = {
            'name': 'default',
            'permissions': ['read', 'write'],
            'rate_limit': 100,  # requêtes par minute
            'created_at': datetime.now()
        }
        
        # Clés supplémentaires depuis les variables d'environnement
        for i in range(1, 6):  # Jusqu'à 5 clés supplémentaires
            key_name = f'API_KEY_{i}'
            key_value = os.getenv(key_name)
            if key_value:
                key_hash = hashlib.sha256(key_value.encode()).hexdigest()
                api_keys[key_hash] = {
                    'name': f'key_{i}',
                    'permissions': ['read', 'write'],
                    'rate_limit': 1000,
                    'created_at': datetime.now()
                }
        
        return api_keys
    
    def _validate_api_key(self, api_key):
        """Valide une clé API"""
        if not api_key:
            return False, "Clé API manquante"
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        if key_hash not in self.api_keys:
            return False, "Clé API invalide"
        
        return True, self.api_keys[key_hash]
    
    def require_api_key(self, permission='read'):
        """Décorateur pour vérifier la clé API"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
                
                is_valid, result = self._validate_api_key(api_key)
                if not is_valid:
                    return jsonify({'error': result, 'success': False}), 401
                
                # Vérifier les permissions
                if permission not in result['permissions']:
                    return jsonify({'error': 'Permission insuffisante', 'success': False}), 403
                
                # Ajouter les infos de la clé à la requête
                request.api_key_info = result
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def _setup_routes(self):
        """Configure les routes de l'API"""
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Point de santé de l'API"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '2.0.0'
            })
        
        @self.app.route('/api/chat', methods=['POST'])
        @self.require_api_key('read')
        def chat():
            """Endpoint principal pour les requêtes de chat"""
            try:
                start_time = time.time()
                
                data = request.get_json()
                if not data or 'message' not in data:
                    return jsonify({
                        'error': 'Message manquant',
                        'success': False
                    }), 400
                
                user_message = data['message'].strip()
                session_id = data.get('session_id', 'anonymous')
                threshold = data.get('threshold', 0.7)
                
                if not user_message:
                    return jsonify({
                        'error': 'Message vide',
                        'success': False
                    }), 400
                
                # Recherche dans la base de connaissances
                best_match = self.db.get_best_response(user_message, threshold=threshold)
                
                response_time = (time.time() - start_time) * 1000  # en ms
                
                if best_match:
                    # Log de la conversation (optionnel)
                    self._log_conversation(session_id, user_message, best_match['response'], 
                                         best_match['id'], best_match['similarity'], response_time)
                    
                    return jsonify({
                        'success': True,
                        'response': best_match['response'],
                        'confidence': best_match['similarity'],
                        'tag': best_match['tag'],
                        'response_time_ms': response_time,
                        'source': 'database'
                    })
                else:
                    # Réponse par défaut
                    default_response = "Désolé, je ne comprends pas votre question. Pouvez-vous la reformuler ?"
                    
                    self._log_conversation(session_id, user_message, default_response, 
                                         None, 0.0, response_time)
                    
                    return jsonify({
                        'success': True,
                        'response': default_response,
                        'confidence': 0.0,
                        'tag': 'unknown',
                        'response_time_ms': response_time,
                        'source': 'fallback'
                    })
            
            except Exception as e:
                logger.error(f"Erreur dans /api/chat: {e}")
                return jsonify({
                    'error': 'Erreur interne du serveur',
                    'success': False
                }), 500
        
        @self.app.route('/api/feedback', methods=['POST'])
        @self.require_api_key('write')
        def feedback():
            """Endpoint pour recevoir les feedbacks utilisateurs"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'Données manquantes', 'success': False}), 400
                
                question = data.get('question', '').strip()
                expected_response = data.get('expected_response', '').strip()
                current_response = data.get('current_response', '').strip()
                
                if not question or not expected_response:
                    return jsonify({
                        'error': 'Question et réponse attendue requises',
                        'success': False
                    }), 400
                
                # Sauvegarder le feedback
                success = self.db.save_feedback(question, expected_response, current_response)
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': 'Feedback enregistré avec succès'
                    })
                else:
                    return jsonify({
                        'error': 'Erreur lors de la sauvegarde',
                        'success': False
                    }), 500
            
            except Exception as e:
                logger.error(f"Erreur dans /api/feedback: {e}")
                return jsonify({
                    'error': 'Erreur interne du serveur',
                    'success': False
                }), 500
        
        @self.app.route('/api/knowledge', methods=['POST'])
        @self.require_api_key('write')
        def add_knowledge():
            """Endpoint pour ajouter de nouvelles connaissances"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'Données manquantes', 'success': False}), 400
                
                tag = data.get('tag', '').strip()
                question = data.get('question', '').strip()
                response = data.get('response', '').strip()
                metadata = data.get('metadata', {})
                
                if not all([tag, question, response]):
                    return jsonify({
                        'error': 'Tag, question et réponse requis',
                        'success': False
                    }), 400
                
                # Ajouter à la base de connaissances
                success = self.db.add_knowledge(tag, question, response, metadata)
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': 'Connaissance ajoutée avec succès'
                    })
                else:
                    return jsonify({
                        'error': 'Erreur lors de l\'ajout',
                        'success': False
                    }), 500
            
            except Exception as e:
                logger.error(f"Erreur dans /api/knowledge: {e}")
                return jsonify({
                    'error': 'Erreur interne du serveur',
                    'success': False
                }), 500
        
        @self.app.route('/api/search', methods=['POST'])
        @self.require_api_key('read')
        def search():
            """Endpoint pour rechercher dans la base de connaissances"""
            try:
                data = request.get_json()
                if not data or 'query' not in data:
                    return jsonify({'error': 'Requête manquante', 'success': False}), 400
                
                query = data['query'].strip()
                top_k = data.get('top_k', 5)
                threshold = data.get('threshold', 0.5)
                
                if not query:
                    return jsonify({'error': 'Requête vide', 'success': False}), 400
                
                # Rechercher des questions similaires
                results = self.db.search_similar_questions(query, top_k=top_k, threshold=threshold)
                
                return jsonify({
                    'success': True,
                    'results': results,
                    'count': len(results)
                })
            
            except Exception as e:
                logger.error(f"Erreur dans /api/search: {e}")
                return jsonify({
                    'error': 'Erreur interne du serveur',
                    'success': False
                }), 500
        
        @self.app.route('/api/stats', methods=['GET'])
        @self.require_api_key('read')
        def stats():
            """Endpoint pour obtenir les statistiques de la base"""
            try:
                stats_data = self.db.get_stats()
                return jsonify({
                    'success': True,
                    'stats': stats_data
                })
            
            except Exception as e:
                logger.error(f"Erreur dans /api/stats: {e}")
                return jsonify({
                    'error': 'Erreur interne du serveur',
                    'success': False
                }), 500
        
        @self.app.route('/api/process-feedbacks', methods=['POST'])
        @self.require_api_key('write')
        def process_feedbacks():
            """Endpoint pour traiter les feedbacks en attente"""
            try:
                success = self.db.process_pending_feedbacks()
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': 'Feedbacks traités avec succès'
                    })
                else:
                    return jsonify({
                        'error': 'Erreur lors du traitement',
                        'success': False
                    }), 500
            
            except Exception as e:
                logger.error(f"Erreur dans /api/process-feedbacks: {e}")
                return jsonify({
                    'error': 'Erreur interne du serveur',
                    'success': False
                }), 500
        
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({
                'error': 'Endpoint non trouvé',
                'success': False
            }), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({
                'error': 'Erreur interne du serveur',
                'success': False
            }), 500
    
    def _log_conversation(self, session_id, user_input, bot_response, matched_kb_id, confidence, response_time):
        """Log une conversation (optionnel)"""
        try:
            from database import ConversationLog
            session = self.db.Session()
            
            log_entry = ConversationLog(
                session_id=session_id,
                user_input=user_input,
                bot_response=bot_response,
                matched_kb_id=matched_kb_id,
                confidence_score=confidence,
                response_time_ms=response_time
            )
            
            session.add(log_entry)
            session.commit()
            session.close()
        except Exception as e:
            logger.error(f"Erreur lors du logging de conversation: {e}")
    
    def run(self, host='localhost', port=5001, debug=False):
        """Lance le serveur API"""
        logger.info(f"Démarrage de l'API sur {host}:{port}")
        logger.info("Clés API configurées:")
        for key_hash, info in self.api_keys.items():
            logger.info(f"  - {info['name']}: {info['permissions']}")
        
        self.app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    # Configuration du serveur
    HOST = os.getenv('API_HOST', 'localhost')
    PORT = int(os.getenv('API_PORT', 5001))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Création et lancement de l'API
    api = ChatbotAPI()
    api.run(host=HOST, port=PORT, debug=DEBUG)
