#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLIENT API POUR MILA ASSIST - VERSION RNCP 6
=====================================================

Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import requests
import logging
import time
import json
from typing import Optional, Dict, List, Any, Tuple
from datetime import datetime, timedelta
import urllib3
from functools import wraps

# Désactiver les avertissements SSL pour le NAS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Exception personnalisée pour les erreurs API"""
    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Décorateur pour retry automatique en cas d'échec"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.RequestException, APIError) as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        logger.error(f"Échec définitif après {max_retries} tentatives: {e}")
                        break
                    
                    logger.warning(f"Tentative {attempt + 1}/{max_retries} échouée: {e}")
                    if attempt < max_retries - 1:
                        logger.info(f"Nouvelle tentative dans {current_delay:.1f}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                
            raise last_exception
        return wrapper
    return decorator

class PerformanceMonitor:
    """Moniteur de performance pour les requêtes API"""
    
    def __init__(self):
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_response_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'last_request_time': None,
            'endpoints_stats': {}
        }
    
    def record_request(self, endpoint: str, response_time: float, success: bool):
        """Enregistrer les métriques d'une requête"""
        self.metrics['total_requests'] += 1
        self.metrics['total_response_time'] += response_time
        self.metrics['last_request_time'] = datetime.now()
        
        if success:
            self.metrics['successful_requests'] += 1
        else:
            self.metrics['failed_requests'] += 1
        
        # Statistiques par endpoint
        if endpoint not in self.metrics['endpoints_stats']:
            self.metrics['endpoints_stats'][endpoint] = {
                'requests': 0,
                'successes': 0,
                'failures': 0,
                'total_time': 0.0
            }
        
        stats = self.metrics['endpoints_stats'][endpoint]
        stats['requests'] += 1
        stats['total_time'] += response_time
        
        if success:
            stats['successes'] += 1
        else:
            stats['failures'] += 1
    
    def record_cache_hit(self):
        """Enregistrer un cache hit"""
        self.metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Enregistrer un cache miss"""
        self.metrics['cache_misses'] += 1
    
    def get_average_response_time(self) -> float:
        """Obtenir le temps de réponse moyen"""
        if self.metrics['total_requests'] > 0:
            return self.metrics['total_response_time'] / self.metrics['total_requests']
        return 0.0
    
    def get_success_rate(self) -> float:
        """Obtenir le taux de succès"""
        if self.metrics['total_requests'] > 0:
            return (self.metrics['successful_requests'] / self.metrics['total_requests']) * 100
        return 0.0
    
    def get_cache_hit_rate(self) -> float:
        """Obtenir le taux de cache hit"""
        total_cache_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
        if total_cache_requests > 0:
            return (self.metrics['cache_hits'] / total_cache_requests) * 100
        return 0.0

class ResponseCache:
    """Cache intelligent pour les réponses API"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 300):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache = {}
        self.access_times = {}
    
    def _generate_key(self, endpoint: str, params: Dict = None) -> str:
        """Générer une clé de cache"""
        import hashlib
        key_data = f"{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_expired(self, timestamp: datetime) -> bool:
        """Vérifier si une entrée a expiré"""
        return datetime.now() - timestamp > timedelta(seconds=self.ttl_seconds)
    
    def _cleanup_expired(self):
        """Nettoyer les entrées expirées"""
        now = datetime.now()
        expired_keys = [
            key for key, timestamp in self.access_times.items()
            if self._is_expired(timestamp)
        ]
        
        for key in expired_keys:
            self.cache.pop(key, None)
            self.access_times.pop(key, None)
    
    def _evict_oldest(self):
        """Éviction de la plus ancienne entrée"""
        if self.access_times:
            oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            self.cache.pop(oldest_key, None)
            self.access_times.pop(oldest_key, None)
    
    def get(self, endpoint: str, params: Dict = None) -> Optional[Any]:
        """Récupérer une valeur du cache"""
        key = self._generate_key(endpoint, params)
        
        if key in self.cache:
            timestamp = self.access_times[key]
            if not self._is_expired(timestamp):
                # Mettre à jour le timestamp d'accès
                self.access_times[key] = datetime.now()
                return self.cache[key]
            else:
                # Supprimer l'entrée expirée
                self.cache.pop(key, None)
                self.access_times.pop(key, None)
        
        return None
    
    def set(self, endpoint: str, value: Any, params: Dict = None):
        """Stocker une valeur dans le cache"""
        # Nettoyer d'abord les entrées expirées
        self._cleanup_expired()
        
        # Éviction si nécessaire
        while len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        key = self._generate_key(endpoint, params)
        self.cache[key] = value
        self.access_times[key] = datetime.now()
    
    def clear(self):
        """Vider le cache"""
        self.cache.clear()
        self.access_times.clear()

class ApiClient:
    """Client API amélioré pour communiquer avec l'API NAS"""
    
    def __init__(self, config):
        self.config = config
        self.base_url = config.API_URL.rstrip('/')
        self.headers = config.get_api_headers()
        self.timeout = config.API_TIMEOUT
        
        # Composants avancés
        self.performance_monitor = PerformanceMonitor()
        self.cache = ResponseCache(max_size=500, ttl_seconds=180)  # Cache 3 minutes
        
        # Configuration de la session
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Adapter pour les timeouts adaptatifs
        adapter = requests.adapters.HTTPAdapter(
            max_retries=requests.adapters.Retry(
                total=0,  # Pas de retry automatique
                backoff_factor=0,
                status_forcelist=[]
            )
        )
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)
        
        logger.info(f"🔗 Client API initialisé: {self.base_url}")
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Dict = None, 
        params: Dict = None,
        use_cache: bool = True,
        timeout: int = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """Effectuer une requête avec monitoring et cache"""
        
        start_time = time.time()
        endpoint_clean = endpoint.lstrip('/')
        
        # Vérifier le cache pour les requêtes GET
        if method.upper() == 'GET' and use_cache:
            cached_response = self.cache.get(endpoint_clean, params)
            if cached_response is not None:
                self.performance_monitor.record_cache_hit()
                logger.debug(f"💾 Cache hit pour {endpoint_clean}")
                return True, cached_response
            else:
                self.performance_monitor.record_cache_miss()
        
        try:
            url = f"{self.base_url}/{endpoint_clean}"
            request_timeout = timeout or self.timeout
            
            logger.debug(f"🌐 {method.upper()} {url}")
            
            if method.upper() == 'GET':
                response = self.session.get(
                    url, 
                    params=params, 
                    timeout=request_timeout,
                    verify=False
                )
            elif method.upper() == 'POST':
                response = self.session.post(
                    url, 
                    json=data, 
                    params=params,
                    timeout=request_timeout,
                    verify=False
                )
            elif method.upper() == 'PUT':
                response = self.session.put(
                    url, 
                    json=data, 
                    params=params,
                    timeout=request_timeout,
                    verify=False
                )
            else:
                raise APIError(f"Méthode HTTP non supportée: {method}")
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    
                    # Mettre en cache les réponses GET réussies
                    if method.upper() == 'GET' and use_cache:
                        self.cache.set(endpoint_clean, response_data, params)
                    
                    self.performance_monitor.record_request(endpoint_clean, response_time, True)
                    logger.debug(f"✅ {endpoint_clean} - {response_time*1000:.1f}ms")
                    
                    return True, response_data
                    
                except json.JSONDecodeError:
                    error_msg = f"Réponse JSON invalide de {endpoint_clean}"
                    logger.error(error_msg)
                    self.performance_monitor.record_request(endpoint_clean, response_time, False)
                    return False, {"error": error_msg, "raw_response": response.text[:200]}
            else:
                error_msg = f"Erreur HTTP {response.status_code}"
                logger.warning(f"⚠️ {endpoint_clean} - {error_msg}")
                self.performance_monitor.record_request(endpoint_clean, response_time, False)
                return False, {
                    "error": error_msg,
                    "status_code": response.status_code,
                    "response": response.text[:200]
                }
                
        except requests.exceptions.Timeout:
            error_msg = f"Timeout API après {request_timeout}s"
            logger.warning(f"⏱️ {endpoint_clean} - {error_msg}")
            self.performance_monitor.record_request(endpoint_clean, time.time() - start_time, False)
            return False, {"error": error_msg}
            
        except requests.exceptions.ConnectionError:
            error_msg = "Impossible de se connecter à l'API"
            logger.warning(f"🔌 {endpoint_clean} - {error_msg}")
            self.performance_monitor.record_request(endpoint_clean, time.time() - start_time, False)
            return False, {"error": error_msg}
            
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            logger.error(f"❌ {endpoint_clean} - {error_msg}")
            self.performance_monitor.record_request(endpoint_clean, time.time() - start_time, False)
            return False, {"error": error_msg}
    
    @retry_on_failure(max_retries=1, delay=0.1)  # Un seul retry ultra-rapide
    def test_connection(self) -> bool:
        """Test de connexion à l'API avec timeout ultra-court"""
        try:
            success, response = self._make_request('GET', '/health', use_cache=False, timeout=1)  # Timeout 1s
            return success and response.get('status') in ['healthy', 'ok']
        except Exception as e:
            logger.warning(f"Test de connexion échoué: {e}")
            return False
    
    # === GESTION DES CONVERSATIONS ===
    
    def obtenir_reponse_chatbot(self, question: str, session_id: str, seuil: float = 0.7) -> Optional[Dict]:
        """Obtenir une réponse du chatbot via l'API avec timeout court pour bascule rapide"""
        
        # Validation des paramètres
        if not question or not question.strip():
            logger.error("Question vide fournie à obtenir_reponse_chatbot")
            return None
        
        if len(question.strip()) > 500:
            logger.warning("Question trop longue, troncature à 500 caractères")
            question = question.strip()[:500]
        
        if not session_id:
            logger.error("session_id vide fournie à obtenir_reponse_chatbot")
            return None
        
        try:
            payload = {
                'message': question.strip(),
                'session_id': session_id,
                'threshold': max(0.0, min(1.0, seuil))  # Validation du seuil
            }
            
            # Timeout ultra-court pour bascule instantanée vers le mode local
            success, data = self._make_request('POST', '/chat', data=payload, use_cache=False, timeout=1)
            
            if success and data.get('success'):
                response_data = {
                    'reponse': data.get('response', ''),
                    'confiance': data.get('confidence', 0.0),
                    'id_connaissance': data.get('knowledge_id'),
                    'temps_reponse_ms': data.get('response_time_ms', 0.0),
                    'source': data.get('source', 'api')
                }
                
                logger.debug(f"✅ Réponse chatbot reçue (confiance: {response_data['confiance']:.2f})")
                return response_data
            else:
                logger.warning(f"API chat sans succès: {data}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur obtenir_reponse_chatbot: {e}")
            return None
    
    def enregistrer_conversation(
        self, 
        session_id: str, 
        question: str, 
        reponse: str,
        id_connaissance: Optional[int] = None, 
        score_confiance: Optional[float] = None,
        temps_reponse_ms: Optional[float] = None
    ) -> bool:
        """Enregistrer une conversation dans journal_conversation avec timeout court"""
        
        # Validation des paramètres requis
        if not all([session_id, question, reponse]):
            logger.error("Paramètres requis manquants pour enregistrer_conversation")
            return False
        
        try:
            payload = {
                'id_session': session_id,
                'question': question[:1000],  # Limiter la longueur
                'reponse': reponse[:2000],     # Limiter la longueur
                'id_connaissance': id_connaissance,
                'score_confiance': score_confiance,
                'temps_reponse_ms': temps_reponse_ms
            }
            
            # Timeout ultra-court pour ne pas bloquer
            success, data = self._make_request('POST', '/journal_conversation', data=payload, use_cache=False, timeout=1)
            
            if success and data.get('success'):
                logger.debug(f"📝 Conversation enregistrée: session {session_id[:12]}...")
                return True
            else:
                logger.warning(f"Échec enregistrement conversation: {data}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur enregistrement conversation: {e}")
            return False
    
    # === GESTION DES FEEDBACKS ===
    
    def soumettre_feedback(
        self, 
        question: str, 
        reponse_attendue: str, 
        reponse_donnee: Optional[str] = None,
        tag_suggere: Optional[str] = None,
        priorite: str = 'moyenne'
    ) -> bool:
        """Soumettre un feedback utilisateur avec validation"""
        
        # Validation des paramètres
        if not question or not reponse_attendue:
            logger.error("Question et réponse attendue requises pour soumettre_feedback")
            return False
        
        if priorite not in ['faible', 'moyenne', 'haute']:
            priorite = 'moyenne'
        
        try:
            payload = {
                'question': question[:500],
                'reponse_donnee': reponse_donnee[:1000] if reponse_donnee else None,
                'reponse_attendue': reponse_attendue[:1000],
                'tag_suggere': tag_suggere,
                'statut': 'nouveau',
                'priorite': priorite
            }
            
            success, data = self._make_request('POST', '/feedback', data=payload, use_cache=False)
            
            if success and data.get('success'):
                logger.debug(f"📝 Feedback envoyé: {question[:50]}...")
                return True
            else:
                logger.warning(f"Échec soumission feedback: {data}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur soumission feedback: {e}")
            return False
    
    # === RECHERCHE DANS LA BASE DE CONNAISSANCES ===
    
    def rechercher_connaissances(
        self, 
        requete: str, 
        limite: int = 5, 
        seuil: float = 0.5
    ) -> List[Dict]:
        """Rechercher dans la base_connaissances avec cache"""
        
        if not requete or not requete.strip():
            return []
        
        try:
            payload = {
                'query': requete.strip(),
                'top_k': max(1, min(100, limite)),  # Validation de la limite
                'threshold': max(0.0, min(1.0, seuil))  # Validation du seuil
            }
            
            success, data = self._make_request('POST', '/search', data=payload, use_cache=True)
            
            if success and data.get('success'):
                results = data.get('results', [])
                logger.debug(f"🔍 Recherche '{requete}': {len(results)} résultats")
                return results
            else:
                logger.warning(f"Échec recherche: {data}")
                return []
                
        except Exception as e:
            logger.error(f"Erreur recherche connaissances: {e}")
            return []
    
    # === STATISTIQUES ET MONITORING ===
    
    def obtenir_statistiques(self) -> Dict[str, Any]:
        """Obtenir les statistiques depuis l'API avec cache"""
        try:
            success, data = self._make_request('GET', '/stats', use_cache=True)
            
            if success and data.get('success'):
                return data.get('stats', {})
            else:
                logger.warning(f"Échec récupération stats: {data}")
                return {}
                
        except Exception as e:
            logger.error(f"Erreur récupération stats: {e}")
            return {}
    
    def obtenir_statistiques_francaises(self) -> Dict:
        """Obtenir les statistiques détaillées via l'endpoint français"""
        try:
            success, data = self._make_request('GET', '/fr/statistiques', use_cache=True)
            
            if success and data.get('success'):
                return data.get('statistiques', {})
            else:
                logger.warning(f"Échec récupération stats FR: {data}")
                return {}
                
        except Exception as e:
            logger.error(f"Erreur récupération stats FR: {e}")
            return {}
    
    # === GESTION DES CONNAISSANCES ===
    
    def ajouter_connaissance(
        self, 
        etiquette: str, 
        question: str, 
        reponse: str,
        donnees_supplementaires: Optional[str] = None
    ) -> bool:
        """Ajouter une nouvelle connaissance avec validation"""
        
        # Validation des paramètres
        if not all([etiquette, question, reponse]):
            logger.error("Étiquette, question et réponse requises pour ajouter_connaissance")
            return False
        
        try:
            # Préparer les métadonnées
            metadata = None
            if donnees_supplementaires:
                try:
                    metadata = json.loads(donnees_supplementaires)
                except json.JSONDecodeError:
                    metadata = {'data': donnees_supplementaires}
            
            payload = {
                'tag': etiquette[:50],  # Limitation de longueur
                'question': question[:500],
                'response': reponse[:2000],
                'metadata': metadata
            }
            
            success, data = self._make_request('POST', '/knowledge', data=payload, use_cache=False)
            
            if success and data.get('success'):
                logger.debug(f"📚 Connaissance ajoutée: {etiquette}")
                # Invalider le cache de recherche
                self.cache.clear()
                return True
            else:
                logger.warning(f"Échec ajout connaissance: {data}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur ajout connaissance: {e}")
            return False
    
    # === MONITORING ET PERFORMANCE ===
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Obtenir les métriques de performance du client"""
        metrics = self.performance_monitor.metrics.copy()
        
        # Ajouter des métriques calculées
        metrics['average_response_time'] = self.performance_monitor.get_average_response_time()
        metrics['success_rate'] = self.performance_monitor.get_success_rate()
        metrics['cache_hit_rate'] = self.performance_monitor.get_cache_hit_rate()
        metrics['cache_size'] = len(self.cache.cache)
        
        return metrics
    
    def reset_performance_metrics(self):
        """Réinitialiser les métriques de performance"""
        self.performance_monitor = PerformanceMonitor()
        logger.info("📊 Métriques de performance réinitialisées")
    
    def clear_cache(self):
        """Vider le cache de réponses"""
        self.cache.clear()
        logger.info("🗑️ Cache API vidé")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Obtenir le statut de santé complet du client API"""
        return {
            'api_connected': self.test_connection(),
            'performance_metrics': self.get_performance_metrics(),
            'cache_info': {
                'size': len(self.cache.cache),
                'max_size': self.cache.max_size,
                'hit_rate': self.performance_monitor.get_cache_hit_rate()
            },
            'configuration': {
                'base_url': self.base_url,
                'timeout': self.timeout,
                'headers_count': len(self.headers)
            },
            'last_check': datetime.now().isoformat()
        }
    
    def __del__(self):
        """Nettoyage lors de la destruction de l'objet"""
        try:
            if hasattr(self, 'session'):
                self.session.close()
        except:
            pass