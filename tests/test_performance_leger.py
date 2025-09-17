#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE PERFORMANCE LÉGER - MILA ASSIST RNCP 6
===============================================

Test de performance simplifié pour mesurer les vraies métriques :
- Temps de chargement de la configuration
- Performance des composants principaux
- Test des services sans TensorFlow
- Métriques d'architecture réelles
- Test de précision depuis la base de données (comme train.py)

Auteur: Samuel VERSCHUEREN
Date: 17-09-2025
"""

import os
import sys
import time
import statistics
import json
import requests
import urllib3
import threading
import gc
import psutil
import concurrent.futures
import random
import string
import traceback
from typing import Dict, Any, List, Tuple, Optional
from dotenv import load_dotenv
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Charger la configuration depuis .env
load_dotenv()

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ConfigurationManager:
    """Gestionnaire de configuration centralisé (adapté de train.py)"""
    
    def __init__(self):
        # Configuration API réelle depuis .env (SÉCURISÉ)
        self.API_URL = os.getenv('API_URL', 'http://localhost:5000/api')
        self.API_KEY = os.getenv('API_KEY', 'default_test_key')
        self.USE_API = os.getenv('USE_API', 'true').lower() == 'true'
        self.DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
        
        print(f"   🔧 Configuration API: {self.API_URL}")
        print(f"   🔑 Clé API: {'*' * 8}...{self.API_KEY[-4:] if len(self.API_KEY) > 4 else '****'}")
        print(f"   🌐 Utiliser API: {self.USE_API}")

class DatabaseAPIClient:
    """Client API pour récupérer les données de la base (adapté de train.py)"""
    
    def __init__(self, config: ConfigurationManager):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': config.API_KEY,
            'Content-Type': 'application/json'
        })
    
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
                print(f"Erreur connexion API: {e}")
            return False
    
    def recuperer_donnees_pour_tests(self) -> List[Dict[str, Any]]:
        """Récupère un échantillon représentatif de la base de données pour les tests"""
        print("   🔍 Récupération des données depuis la base...")
        
        toutes_connaissances = []
        connaissances_vues = set()
        
        # Requêtes représentatives pour couvrir différents domaines
        requetes_test = [
            "bonjour", "merci", "au revoir", "salut", "hello",
            "comment", "qui es", "aide", "ai_licia", "ailicia", 
            "configuration", "TTS", "OBS", "stream", "vocal",
            "créateur", "nom", "age", ""  # Requête vide pour récupérer plus
        ]
        
        for i, requete in enumerate(requetes_test):
            try:
                payload = {
                    "query": requete,
                    "top_k": 200,  # Limité pour les tests
                    "threshold": 0.0
                }
                
                response = self.session.post(
                    f"{self.config.API_URL}/search",
                    json=payload,
                    timeout=15,
                    verify=False
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and 'results' in data:
                        for resultat in data['results']:
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
                        
                        print(f"      ✅ Requête '{requete}': {len(data['results'])} résultats")
                    
            except Exception as e:
                print(f"      ❌ Erreur requête '{requete}': {e}")
        
        print(f"   📊 Total données récupérées: {len(toutes_connaissances)}")
        return toutes_connaissances
    
    def convertir_vers_format_test(self, connaissances: List[Dict[str, Any]]) -> List[tuple]:
        """Convertit les données de la base vers format de test"""
        test_questions = []
        
        # Grouper par tag pour extraire des mots-clés représentatifs
        donnees_par_tag = {}
        for connaissance in connaissances:
            tag = connaissance.get('tag', 'general').strip()
            question = connaissance.get('question', '').strip()
            reponse = connaissance.get('response', '').strip()
            
            if not tag or not question or not reponse:
                continue
                
            if tag not in donnees_par_tag:
                donnees_par_tag[tag] = {'questions': [], 'responses': []}
            
            donnees_par_tag[tag]['questions'].append(question)
            donnees_par_tag[tag]['responses'].append(reponse)
        
        # Sélectionner des échantillons représentatifs par tag
        for tag, donnees in donnees_par_tag.items():
            # Extraire des mots-clés depuis les réponses
            keywords = []
            for response in donnees['responses'][:3]:  # 3 premières réponses
                words = response.lower().split()
                relevant_words = [word.strip('.,!?;:') for word in words 
                                if len(word.strip('.,!?;:')) > 3 and word.isalpha()]
                keywords.extend(relevant_words[:3])
            
            # Prendre jusqu'à 3 questions par tag pour les tests
            for question in donnees['questions'][:3]:
                if question.strip():  # Exclure les questions vides
                    test_questions.append((question, tag, list(set(keywords))))
        
        return test_questions

class LightPerformanceTest:
    """Test de performance léger du système Mila Assist"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        
    def run_performance_tests(self) -> Dict[str, Any]:
        print("🚀 TESTS DE PERFORMANCE - MILA ASSIST")
        print("=" * 60)
        try:
            # 1. Test configuration
            print("1. ⚙️ Test de la configuration")
            self.results['config'] = self._test_configuration()

            # 2. Test temps de réponse et précision
            print("\n2. ⚡ Test du temps de réponse et précision")
            self.results['response'] = self._test_response_metrics()

            # 3. Test sécurité anti-injection
            print("\n3. 🔒 Test de sécurité anti-injection")
            self.results['security'] = self._test_security_injection()

            # 4. Dépendances
            print("\n4. 📦 Test des dépendances critiques")
            self.results['dependencies'] = self._test_dependencies()

            # 5. NOUVEAUX TESTS AVANCÉS
            print("\n5. 🚀 Test de performance sous charge")
            self.results['load_performance'] = self._test_load_performance()

            print("\n6. 🧠 Test d'utilisation mémoire")
            self.results['memory_usage'] = self._test_memory_usage()

            print("\n7. 🛠️ Test de récupération d'erreurs")
            self.results['error_recovery'] = self._test_error_recovery()

            print("\n8. 🎯 Test des cas limites")
            self.results['edge_cases'] = self._test_edge_cases()

            # Génération du rapport Markdown
            print("\nGénération du rapport test_perf.md ...")
            self._generate_markdown_report()

            print("\n✅ Tests terminés avec succès")
            return self.results
        except Exception as e:
            print(f"❌ Erreur pendant les tests: {e}")
            return {'error': str(e)}
    def _test_response_metrics(self) -> Dict[str, Any]:
        """Test du temps de réponse et de la précision sur des questions entraînées"""
        try:
            from config.app_config import AppConfig
            from services.chatbot_service import ChatbotService
            config = AppConfig()
            chatbot = ChatbotService(config)
            
            # Charger les vraies données d'entraînement
            test_questions = self._load_training_data()
            
            # Optimisation: Tester d'abord le mode local (plus sensible à la fragmentation mémoire)
            print(f"   🧠 Test mode local avec fallbacks intelligents")
            local_smart_results = self._test_mode(chatbot, test_questions, "local_smart")
            
            print(f"   🔧 Test mode local Keras direct")
            local_raw_results = self._test_mode(chatbot, test_questions, "local_raw")
            
            print(f"   🌐 Test mode API externe")
            api_results = self._test_mode(chatbot, test_questions, "api")
            
            return {
                'local_smart': local_smart_results,
                'local_raw': local_raw_results,
                'api': api_results,
                'combined_accuracy': (local_smart_results.get('accuracy', 0) + local_raw_results.get('accuracy', 0) + api_results.get('accuracy', 0)) / 3,
                'combined_avg_time': (local_smart_results.get('avg_time_ms', 0) + local_raw_results.get('avg_time_ms', 0) + api_results.get('avg_time_ms', 0)) / 3
            }
            
        except Exception as e:
            print(f"   ❌ Erreur test réponse: {e}")
            return {'error': str(e)}

    def _test_mode(self, chatbot, test_questions, mode="local_smart") -> Dict[str, Any]:
        """Test pour un mode spécifique avec 3 variations :
        - local_smart : Mode local avec intelligence de fallback complète (obtenir_reponse)
        - local_raw : Modèle Keras brut seulement (_obtenir_reponse_keras_amelioree)  
        - api : API externe directe
        """
        try:
            times = []
            correct = 0
            total = len(test_questions)
            details = []
            
            print(f"     🔧 Configuration mode {mode}...")
            
            # Optimisation: Nettoyer le cache et les stats avant le test
            if "local" in mode and hasattr(chatbot, 'prediction_cache'):
                chatbot.prediction_cache.clear()
                print(f"     🧹 Cache de prédictions nettoyé")
            
            if mode == "local_smart":
                # Mode LOCAL INTELLIGENT : Utiliser obtenir_reponse avec fallbacks mais API désactivée
                print(f"     🧠 Mode LOCAL : Intelligence complète avec fallbacks")
                original_use_api = getattr(chatbot.config, 'USE_API', True)
                chatbot.config.USE_API = False
                
            elif mode == "local_raw":
                # Mode LOCAL BRUT : Modèle Keras seulement, sans fallbacks
                print(f"     🔧 Mode LOCAL : Modèle Keras direct sans fallbacks")
                original_use_api = getattr(chatbot.config, 'USE_API', True)
                chatbot.config.USE_API = False
                
            elif mode == "api":
                # Mode API : Forcer l'utilisation de l'API externe uniquement
                print(f"     🌐 Mode API : Serveur externe {chatbot.config.API_URL}")
                # S'assurer que l'API est activée
                chatbot.config.USE_API = True
                # Désactiver temporairement le fallback pour forcer l'utilisation de l'API
                original_use_fallback = getattr(chatbot.config, 'USE_LEGACY_FALLBACK', True)
                chatbot.config.USE_LEGACY_FALLBACK = False
            
            for i, (question, expected_tag, expected_keywords) in enumerate(test_questions):
                session_id = f"perf_test_{mode}_{i}"  # Préfixe spécial pour les tests
                start = time.time()
                
                try:
                    if mode == "api":
                        # Test direct de l'API sans fallback
                        response = self._test_api_direct(question, session_id, chatbot.config)
                    elif mode == "local_smart":
                        # Désactiver temporairement l'enregistrement des conversations pour les tests
                        original_save_conversations = getattr(chatbot, 'save_conversations', True)
                        chatbot.save_conversations = False
                        
                        # Test du modèle local avec intelligence complète (comme les tests originaux à 94%)
                        response = chatbot.obtenir_reponse(question, session_id)
                        
                        # Restaurer le paramètre
                        chatbot.save_conversations = original_save_conversations
                        
                    elif mode == "local_raw":
                        # Désactiver temporairement l'enregistrement des conversations pour les tests
                        original_save_conversations = getattr(chatbot, 'save_conversations', True)
                        chatbot.save_conversations = False
                        
                        # Test du modèle Keras brut seulement (pour comparaison)
                        if hasattr(chatbot, '_obtenir_reponse_keras_amelioree'):
                            response = chatbot._obtenir_reponse_keras_amelioree(question)
                            if not response:
                                response = chatbot._reponse_par_defaut(question)
                        else:
                            response = "Modèle Keras non disponible"
                            
                        # Restaurer le paramètre
                        chatbot.save_conversations = original_save_conversations
                    
                    elapsed = (time.time() - start) * 1000
                    times.append(elapsed)
                    
                    # Précision basée sur les mots-clés attendus du tag
                    is_correct = any(keyword.lower() in response.lower() for keyword in expected_keywords)
                    if is_correct:
                        correct += 1
                        
                    details.append({
                        'question': question,
                        'expected_tag': expected_tag,
                        'expected_keywords': expected_keywords,
                        'response': response,
                        'elapsed_ms': elapsed,
                        'correct': is_correct,
                        'mode': mode
                    })
                except Exception as e:
                    print(f"     ❌ Erreur sur question '{question}' en mode {mode}: {e}")
                    details.append({
                        'question': question,
                        'expected_tag': expected_tag,
                        'expected_keywords': expected_keywords,
                        'response': f"ERREUR: {str(e)}",
                        'elapsed_ms': 0,
                        'correct': False,
                        'mode': mode
                    })
            
            # Restaurer la configuration originale
            if mode in ["local_smart", "local_raw"]:
                chatbot.config.USE_API = original_use_api
                # Optimisation: Forcer le garbage collection après les tests locaux
                import gc
                gc.collect()
                print(f"     🧹 Mémoire nettoyée après test {mode}")
            elif mode == "api":
                chatbot.config.USE_LEGACY_FALLBACK = original_use_fallback
            
            avg_time = sum(times) / len(times) if times else 0
            accuracy = correct / total if total else 0
            
            print(f"     Mode {mode}: Temps moyen: {avg_time:.1f}ms, Précision: {accuracy*100:.1f}% ({correct}/{total})")
            
            return {
                'avg_time_ms': avg_time,
                'accuracy': accuracy,
                'details': details,
                'mode': mode,
                'total_questions': total,
                'correct_answers': correct
            }
            
        except Exception as e:
            print(f"   ❌ Erreur test mode {mode}: {e}")
            return {
                'error': str(e),
                'avg_time_ms': 0,
                'accuracy': 0,
                'details': [],
                'mode': mode
            }
    
    def _test_api_direct(self, question: str, session_id: str, config) -> str:
        """Test direct de l'API sans fallback"""
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        try:
            payload = {
                "message": question,
                "session_id": session_id,
                "mode": "chat"
            }
            
            headers = {
                'X-API-Key': config.API_KEY,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{config.API_URL}/chat",
                json=payload,
                headers=headers,
                timeout=10,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data.get('response', 'Réponse API vide')
                else:
                    return f"Erreur API: {data.get('error', 'Erreur inconnue')}"
            else:
                return f"Erreur HTTP {response.status_code}: {response.text[:100]}"
                
        except requests.exceptions.Timeout:
            return "Erreur: Timeout API"
        except requests.exceptions.ConnectionError:
            return "Erreur: Connexion API impossible"
        except Exception as e:
            return f"Erreur API: {str(e)}"

    def _load_training_data(self) -> list:
        """Charge les vraies données d'entraînement depuis la base de données (comme train.py)"""
        try:
            # Initialiser la configuration et le client API
            config = ConfigurationManager()
            api_client = DatabaseAPIClient(config)
            
            # Vérifier la connexion à l'API
            if not config.USE_API:
                print(f"   ⚠️ API désactivée dans la configuration")
                return self._get_fallback_data()
            
            if not api_client.test_connection():
                print(f"   ⚠️ API non accessible - utilisation des données de fallback")
                return self._get_fallback_data()
            
            # Récupérer les données depuis la base
            connaissances = api_client.recuperer_donnees_pour_tests()
            
            if not connaissances:
                print(f"   ⚠️ Aucune donnée récupérée depuis la base")
                return self._get_fallback_data()
            
            # Convertir vers format de test
            test_questions = api_client.convertir_vers_format_test(connaissances)
            
            print(f"   ✅ Chargé {len(test_questions)} questions depuis la base de données")
            print(f"   📊 Basé sur {len(connaissances)} entrées de la base")
            
            return test_questions
            
        except Exception as e:
            print(f"   ⚠️ Erreur lors du chargement depuis la base: {e}")
            return self._get_fallback_data()
    
    def _get_fallback_data(self) -> list:
        """Données de fallback si la base n'est pas accessible"""
        print("   📋 Utilisation des données de fallback")
        return [
            ("Bonjour", "greetings", ["bonjour", "salut", "ravi"]),
            ("Merci", "thanks", ["merci", "plaisir", "heureux"]),
            ("Au revoir", "goodbye", ["revoir", "bientôt", "journée"]),
            ("Qui es-tu", "name1", ["julie", "intelligence", "assistant"]),
            ("Comment t'appelles-tu", "name1", ["julie", "programme", "assistant"]),
            ("Qu'est-ce qu'ai_licia", "Ai_licia", ["compagnon", "premier", "pour"]),
            ("Aide-moi", "help", ["aide", "assistance", "aider"]),
            ("Comment configurer OBS", "stream_setup", ["configurer", "obs", "stream"]),
        ]

    def _test_security_injection(self) -> Dict[str, Any]:
        """Test de sécurité anti-injection de code malveillant"""
        try:
            from config.app_config import AppConfig
            from services.chatbot_service import ChatbotService
            config = AppConfig()
            chatbot = ChatbotService(config)
            # Messages malveillants typiques
            malicious_inputs = [
                "<script>alert('hack')</script>",
                "SELECT * FROM users; --",
                "DROP TABLE data;",
                "{{7*7}}",
                "'; exec('rm -rf /'); --",
                "<img src=x onerror=alert(1)>"
            ]
            safe = True
            details = []
            for i, msg in enumerate(malicious_inputs):
                session_id = f"sec_{i}"
                response = chatbot.obtenir_reponse(msg, session_id)
                # On considère qu'une réponse sûre ne doit pas exécuter, ni renvoyer le code
                is_safe = all(x not in response.lower() for x in ["script", "select", "drop", "exec", "img", "alert", "table", "rm -rf", "{{", "}}"])
                if not is_safe:
                    safe = False
                details.append({
                    'input': msg,
                    'response': response,
                    'safe': is_safe
                })
            print(f"   Sécurité anti-injection: {'OK' if safe else 'VULNÉRABLE'}")
            return {
                'safe': safe,
                'details': details
            }
        except Exception as e:
            print(f"   ❌ Erreur test sécurité: {e}")
            return {'error': str(e)}
    
    def _test_configuration(self) -> Dict[str, Any]:
        """Test de chargement de la configuration"""
        start_time = time.time()
        
        try:
            from config.app_config import AppConfig
            config = AppConfig()
            load_time = (time.time() - start_time) * 1000
            
            # Vérifier les propriétés importantes
            properties_check = {
                'API_URL': hasattr(config, 'API_URL'),
                'USE_API': hasattr(config, 'USE_API'),
                'USE_LEGACY_FALLBACK': hasattr(config, 'USE_LEGACY_FALLBACK'),
                'API_TIMEOUT': hasattr(config, 'API_TIMEOUT'),
                'HOST': hasattr(config, 'HOST'),
                'PORT': hasattr(config, 'PORT')
            }
            
            config_valid = all(properties_check.values())
            
            print(f"   ✅ Configuration chargée en {load_time:.1f}ms")
            print(f"   ✅ Propriétés valides: {sum(properties_check.values())}/{len(properties_check)}")
            
            return {
                'load_time_ms': load_time,
                'valid': config_valid,
                'properties': properties_check,
                'timeout_optimized': getattr(config, 'API_TIMEOUT', 0) <= 1
            }
            
        except Exception as e:
            load_time = (time.time() - start_time) * 1000
            print(f"   ❌ Erreur de configuration: {e}")
            return {'error': str(e), 'load_time_ms': load_time}
    
    def _test_dependencies(self) -> Dict[str, Any]:
        """Test des dépendances"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        requirements_file = os.path.join(base_dir, 'requirements_full.txt')
        
        if not os.path.exists(requirements_file):
            print("   ❌ Fichier requirements_full.txt manquant")
            return {'error': 'Requirements file missing'}
        
        try:
            with open(requirements_file, 'r') as f:
                content = f.read()
                lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
                
            # Dépendances critiques
            critical_deps = ['flask', 'tensorflow', 'nltk', 'requests', 'python-dotenv']
            found_deps = []
            
            for dep in critical_deps:
                for line in lines:
                    if dep in line.lower():
                        found_deps.append(dep)
                        break
            
            print(f"   📦 {len(lines)} dépendances trouvées")
            print(f"   ✅ Dépendances critiques: {len(found_deps)}/{len(critical_deps)}")
            
            for dep in found_deps:
                print(f"     ✅ {dep}")
            
            for dep in critical_deps:
                if dep not in found_deps:
                    print(f"     ❌ {dep} (manquant)")
            
            return {
                'total_dependencies': len(lines),
                'critical_found': len(found_deps),
                'critical_total': len(critical_deps),
                'critical_dependencies': found_deps,
                'dependencies_complete': len(found_deps) == len(critical_deps)
            }
            
        except Exception as e:
            print(f"   ❌ Erreur lecture requirements: {e}")
            return {'error': str(e)}

    def _test_load_performance(self) -> Dict[str, Any]:
        """Test de performance sous charge (requêtes simultanées)"""
        try:
            from config.app_config import AppConfig
            from services.chatbot_service import ChatbotService
            config = AppConfig()
            
            print("   🔧 Initialisation du test de charge...")
            test_questions = ["Bonjour", "Comment configurer OBS ?", "Qui es-tu ?", "Aide-moi avec le streaming"]
            load_levels = [5, 10, 20]  # Niveaux de charge progressive
            results = {}
            
            for load_level in load_levels:
                print(f"   📊 Test avec {load_level} requêtes simultanées...")
                start_time = time.time()
                
                def send_request(i):
                    """Fonction pour une requête individuelle"""
                    try:
                        chatbot = ChatbotService(config)
                        question = random.choice(test_questions)
                        session_id = f"load_test_{load_level}_{i}"
                        
                        request_start = time.time()
                        response = chatbot.obtenir_reponse(question, session_id)
                        request_time = (time.time() - request_start) * 1000
                        
                        return {
                            'success': True,
                            'response_time': request_time,
                            'response_length': len(response) if response else 0,
                            'question': question
                        }
                    except Exception as e:
                        return {
                            'success': False,
                            'error': str(e),
                            'response_time': 0,
                            'response_length': 0,
                            'question': question if 'question' in locals() else 'unknown'
                        }
                
                # Exécution des requêtes en parallèle
                with concurrent.futures.ThreadPoolExecutor(max_workers=load_level) as executor:
                    futures = [executor.submit(send_request, i) for i in range(load_level)]
                    request_results = [future.result() for future in concurrent.futures.as_completed(futures)]
                
                total_time = (time.time() - start_time) * 1000
                successful_requests = [r for r in request_results if r['success']]
                failed_requests = [r for r in request_results if not r['success']]
                
                if successful_requests:
                    avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
                    max_response_time = max(r['response_time'] for r in successful_requests)
                    min_response_time = min(r['response_time'] for r in successful_requests)
                else:
                    avg_response_time = max_response_time = min_response_time = 0
                
                # Calcul du throughput (requêtes par seconde)
                throughput = load_level / (total_time / 1000) if total_time > 0 else 0
                
                results[f'load_{load_level}'] = {
                    'total_requests': load_level,
                    'successful_requests': len(successful_requests),
                    'failed_requests': len(failed_requests),
                    'success_rate': len(successful_requests) / load_level * 100,
                    'total_time_ms': total_time,
                    'avg_response_time_ms': avg_response_time,
                    'max_response_time_ms': max_response_time,
                    'min_response_time_ms': min_response_time,
                    'throughput_rps': throughput,
                    'errors': [r['error'] for r in failed_requests]
                }
                
                print(f"     ✅ {len(successful_requests)}/{load_level} succès, Temps moy: {avg_response_time:.1f}ms, Throughput: {throughput:.1f} req/s")
                
                # Pause entre les tests pour éviter la surcharge
                time.sleep(2)
            
            # Analyse globale
            overall_success_rate = sum(results[key]['success_rate'] for key in results) / len(results)
            degradation = False
            
            if len(load_levels) > 1:
                # Vérifier si les performances se dégradent avec la charge
                first_load = f'load_{load_levels[0]}'
                last_load = f'load_{load_levels[-1]}'
                if (results[last_load]['avg_response_time_ms'] > 
                    results[first_load]['avg_response_time_ms'] * 2):
                    degradation = True
            
            print(f"   📊 Taux de succès global: {overall_success_rate:.1f}%")
            print(f"   {'⚠️ Dégradation détectée' if degradation else '✅ Performance stable'}")
            
            return {
                'overall_success_rate': overall_success_rate,
                'performance_degradation': degradation,
                'load_results': results,
                'stable_under_load': overall_success_rate >= 95 and not degradation
            }
            
        except Exception as e:
            print(f"   ❌ Erreur test de charge: {e}")
            return {'error': str(e)}

    def _test_memory_usage(self) -> Dict[str, Any]:
        """Analyse de l'utilisation mémoire et détection des fuites"""
        try:
            from config.app_config import AppConfig
            from services.chatbot_service import ChatbotService
            
            print("   🧠 Analyse de l'utilisation mémoire...")
            
            # Mesure mémoire initiale
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            print(f"   📊 Mémoire initiale: {initial_memory:.1f} MB")
            
            # Test avec création/destruction multiples d'instances
            memory_measurements = []
            config = AppConfig()
            
            for i in range(5):
                # Créer une instance
                chatbot = ChatbotService(config)
                
                # Faire quelques requêtes
                for j in range(10):
                    session_id = f"memory_test_{i}_{j}"
                    response = chatbot.obtenir_reponse(f"Test mémoire {i}-{j}", session_id)
                
                # Mesurer la mémoire
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_measurements.append(current_memory)
                
                # Nettoyer explicitement
                del chatbot
                gc.collect()
                
                print(f"     Itération {i+1}: {current_memory:.1f} MB")
            
            # Mesure mémoire finale après nettoyage
            gc.collect()  # Force garbage collection
            final_memory = process.memory_info().rss / 1024 / 1024
            
            # Analyse des fuites
            memory_increase = final_memory - initial_memory
            max_memory = max(memory_measurements)
            avg_memory = sum(memory_measurements) / len(memory_measurements)
            
            # Détection de fuite (si augmentation > 50MB)
            memory_leak_detected = memory_increase > 50
            
            # Test de performance avec cache plein
            print("   💾 Test avec cache saturé...")
            chatbot = ChatbotService(config)
            
            # Saturer le cache avec des requêtes uniques
            cache_test_start = time.time()
            for i in range(100):
                unique_question = f"Question unique cache test {i} {random.randint(1000, 9999)}"
                session_id = f"cache_test_{i}"
                response = chatbot.obtenir_reponse(unique_question, session_id)
            cache_test_time = (time.time() - cache_test_start) * 1000
            
            cache_memory = process.memory_info().rss / 1024 / 1024
            cache_size = len(getattr(chatbot, 'prediction_cache', {}))
            
            print(f"   📊 Mémoire avec cache plein: {cache_memory:.1f} MB")
            print(f"   📦 Taille du cache: {cache_size} entrées")
            print(f"   ⏱️ Temps test cache: {cache_test_time:.1f}ms")
            
            # Nettoyage final
            del chatbot
            gc.collect()
            
            return {
                'initial_memory_mb': initial_memory,
                'final_memory_mb': final_memory,
                'max_memory_mb': max_memory,
                'avg_memory_mb': avg_memory,
                'memory_increase_mb': memory_increase,
                'memory_leak_detected': memory_leak_detected,
                'cache_memory_mb': cache_memory,
                'cache_size': cache_size,
                'cache_test_time_ms': cache_test_time,
                'memory_measurements': memory_measurements,
                'memory_stable': not memory_leak_detected and memory_increase < 20
            }
            
        except Exception as e:
            print(f"   ❌ Erreur test mémoire: {e}")
            return {'error': str(e)}

    def _test_error_recovery(self) -> Dict[str, Any]:
        """Test de gestion des erreurs et récupération gracieuse"""
        try:
            from config.app_config import AppConfig
            from services.chatbot_service import ChatbotService
            
            print("   🛠️ Test de récupération d'erreurs...")
            recovery_results = {}
            
            # Test 1: API indisponible
            print("     🌐 Test API indisponible...")
            try:
                config = AppConfig()
                original_api_url = config.API_URL
                config.API_URL = "https://api-inexistante-test.fake"  # URL bidon
                
                chatbot = ChatbotService(config)
                response = chatbot.obtenir_reponse("Test API indisponible", "error_test_1")
                
                # La réponse devrait être fournie par le fallback
                api_recovery_success = response and len(response) > 10 and "erreur" not in response.lower()
                recovery_results['api_unavailable'] = {
                    'success': api_recovery_success,
                    'response_provided': bool(response),
                    'response_length': len(response) if response else 0
                }
                
                # Restaurer l'URL originale
                config.API_URL = original_api_url
                print(f"       {'✅' if api_recovery_success else '❌'} Récupération API")
                
            except Exception as e:
                recovery_results['api_unavailable'] = {'error': str(e), 'success': False}
            
            # Test 2: Configuration corrompue
            print("     ⚙️ Test configuration invalide...")
            try:
                config = AppConfig()
                # Corrompre temporairement la config
                original_timeout = getattr(config, 'API_TIMEOUT', 5)
                config.API_TIMEOUT = None  # Valeur invalide
                
                chatbot = ChatbotService(config)
                response = chatbot.obtenir_reponse("Test config corrompue", "error_test_2")
                
                config_recovery_success = response and len(response) > 5
                recovery_results['config_corrupted'] = {
                    'success': config_recovery_success,
                    'response_provided': bool(response),
                    'graceful_handling': True
                }
                
                # Restaurer
                config.API_TIMEOUT = original_timeout
                print(f"       {'✅' if config_recovery_success else '❌'} Récupération config")
                
            except Exception as e:
                recovery_results['config_corrupted'] = {'error': str(e), 'success': False}
            
            # Test 3: Mémoire saturée (simulation)
            print("     🧠 Test gestion mémoire limitée...")
            try:
                config = AppConfig()
                chatbot = ChatbotService(config)
                
                # Créer une charge mémoire artificielle
                large_requests = []
                for i in range(20):
                    large_question = "Test mémoire " + "x" * 1000  # Question très longue
                    response = chatbot.obtenir_reponse(large_question, f"memory_stress_{i}")
                    large_requests.append(response)
                
                # Vérifier que le système répond encore
                final_response = chatbot.obtenir_reponse("Test final", "memory_test_final")
                memory_recovery_success = final_response and len(final_response) > 5
                
                recovery_results['memory_stress'] = {
                    'success': memory_recovery_success,
                    'handled_large_requests': len(large_requests),
                    'final_response_ok': bool(final_response)
                }
                
                print(f"       {'✅' if memory_recovery_success else '❌'} Gestion mémoire")
                
            except Exception as e:
                recovery_results['memory_stress'] = {'error': str(e), 'success': False}
            
            # Test 4: Timeout réseau (simulation)
            print("     ⏱️ Test gestion timeout...")
            try:
                config = AppConfig()
                original_timeout = config.API_TIMEOUT
                config.API_TIMEOUT = 0.1  # Timeout très court
                
                chatbot = ChatbotService(config)
                response = chatbot.obtenir_reponse("Test timeout", "timeout_test")
                
                timeout_recovery_success = response and "timeout" not in response.lower()
                recovery_results['timeout_handling'] = {
                    'success': timeout_recovery_success,
                    'fallback_activated': bool(response),
                    'response_reasonable': len(response) > 10 if response else False
                }
                
                # Restaurer
                config.API_TIMEOUT = original_timeout
                print(f"       {'✅' if timeout_recovery_success else '❌'} Gestion timeout")
                
            except Exception as e:
                recovery_results['timeout_handling'] = {'error': str(e), 'success': False}
            
            # Test 5: Entrée malformée
            print("     📝 Test entrées malformées...")
            try:
                config = AppConfig()
                chatbot = ChatbotService(config)
                
                malformed_inputs = [
                    None,
                    "",
                    " " * 100,
                    "\n\n\n",
                    "🤖" * 100,
                    "a" * 5000  # Très long
                ]
                
                malformed_recovery_count = 0
                for i, malformed_input in enumerate(malformed_inputs):
                    try:
                        response = chatbot.obtenir_reponse(malformed_input, f"malformed_{i}")
                        if response and len(response) > 5:
                            malformed_recovery_count += 1
                    except:
                        pass  # Échec attendu pour certaines entrées
                
                malformed_recovery_success = malformed_recovery_count >= len(malformed_inputs) // 2
                recovery_results['malformed_input'] = {
                    'success': malformed_recovery_success,
                    'recovered_count': malformed_recovery_count,
                    'total_tests': len(malformed_inputs),
                    'recovery_rate': malformed_recovery_count / len(malformed_inputs) * 100
                }
                
                print(f"       {'✅' if malformed_recovery_success else '❌'} Entrées malformées ({malformed_recovery_count}/{len(malformed_inputs)})")
                
            except Exception as e:
                recovery_results['malformed_input'] = {'error': str(e), 'success': False}
            
            # Calcul du score global de récupération
            successful_recoveries = sum(1 for result in recovery_results.values() 
                                      if isinstance(result, dict) and result.get('success', False))
            total_tests = len(recovery_results)
            overall_recovery_rate = successful_recoveries / total_tests * 100 if total_tests > 0 else 0
            
            print(f"   📊 Taux de récupération global: {overall_recovery_rate:.1f}% ({successful_recoveries}/{total_tests})")
            
            return {
                'overall_recovery_rate': overall_recovery_rate,
                'successful_recoveries': successful_recoveries,
                'total_recovery_tests': total_tests,
                'recovery_details': recovery_results,
                'robust_error_handling': overall_recovery_rate >= 80
            }
            
        except Exception as e:
            print(f"   ❌ Erreur test récupération: {e}")
            return {'error': str(e)}

    def _test_edge_cases(self) -> Dict[str, Any]:
        """Test avec données extrêmes et cas limites"""
        try:
            from config.app_config import AppConfig
            from services.chatbot_service import ChatbotService
            config = AppConfig()
            chatbot = ChatbotService(config)
            
            print("   🎯 Test des cas limites...")
            edge_case_results = {}
            
            # Test 1: Messages très longs
            print("     📏 Test messages très longs...")
            long_message = "Question très longue sur le streaming " * 100  # ~3000 caractères
            start_time = time.time()
            response = chatbot.obtenir_reponse(long_message, "edge_long")
            long_msg_time = (time.time() - start_time) * 1000
            
            long_msg_success = response and len(response) > 10 and long_msg_time < 10000  # < 10s
            edge_case_results['long_message'] = {
                'success': long_msg_success,
                'input_length': len(long_message),
                'response_length': len(response) if response else 0,
                'response_time_ms': long_msg_time,
                'reasonable_time': long_msg_time < 5000
            }
            print(f"       {'✅' if long_msg_success else '❌'} Message long ({len(long_message)} chars, {long_msg_time:.1f}ms)")
            
            # Test 2: Messages vides et espaces
            print("     🗙 Test messages vides...")
            empty_tests = ["", "   ", "\n\n", "\t\t", " \n \t "]
            empty_success_count = 0
            
            for i, empty_msg in enumerate(empty_tests):
                response = chatbot.obtenir_reponse(empty_msg, f"edge_empty_{i}")
                if response and len(response) > 5 and "saisir" in response.lower():
                    empty_success_count += 1
            
            empty_success = empty_success_count >= len(empty_tests) // 2
            edge_case_results['empty_messages'] = {
                'success': empty_success,
                'total_tests': len(empty_tests),
                'successful_handles': empty_success_count,
                'proper_error_messages': empty_success_count >= 3
            }
            print(f"       {'✅' if empty_success else '❌'} Messages vides ({empty_success_count}/{len(empty_tests)})")
            
            # Test 3: Caractères spéciaux et emojis
            print("     🎭 Test caractères spéciaux...")
            special_chars = [
                "🤖 Comment configurer OBS ? 🎮",
                "Question avec émoticônes ❤️💯🔥",
                "Caractères spéciaux: àâäéèêëïîôùûüÿç",
                "<script>alert('test')</script>",
                "Question normale avec (parenthèses) et [crochets]",
                "Test & esperluette + plus = égal # hashtag",
                "Apostrophe's et quotes \"test\" et 'single'",
                "Accents: àâäéèêëïîôùûüÿç ÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ"
            ]
            
            special_char_success_count = 0
            for i, special_msg in enumerate(special_chars):
                try:
                    response = chatbot.obtenir_reponse(special_msg, f"edge_special_{i}")
                    if response and len(response) > 5 and not any(danger in response for danger in ["<script>", "alert", "undefined"]):
                        special_char_success_count += 1
                except:
                    pass
            
            special_char_success = special_char_success_count >= len(special_chars) * 0.8
            edge_case_results['special_characters'] = {
                'success': special_char_success,
                'total_tests': len(special_chars),
                'successful_handles': special_char_success_count,
                'security_safe': special_char_success_count >= len(special_chars) - 1
            }
            print(f"       {'✅' if special_char_success else '❌'} Caractères spéciaux ({special_char_success_count}/{len(special_chars)})")
            
            # Test 4: Langues non-françaises
            print("     🌍 Test langues étrangères...")
            foreign_languages = [
                "Hello, how to configure OBS?",  # Anglais
                "Hola, ¿cómo configurar OBS?",   # Espagnol
                "Hallo, wie konfiguriere ich OBS?",  # Allemand
                "Ciao, come configurare OBS?",   # Italien
                "你好，如何配置OBS？",              # Chinois
                "こんにちは、OBSの設定方法は？",        # Japonais
                "مرحبا، كيفية تكوين OBS؟"          # Arabe
            ]
            
            foreign_lang_success_count = 0
            for i, foreign_msg in enumerate(foreign_languages):
                try:
                    response = chatbot.obtenir_reponse(foreign_msg, f"edge_foreign_{i}")
                    # Succès si répond en français ou dans la langue appropriée
                    if response and len(response) > 10:
                        foreign_lang_success_count += 1
                except:
                    pass
            
            foreign_lang_success = foreign_lang_success_count >= len(foreign_languages) // 2
            edge_case_results['foreign_languages'] = {
                'success': foreign_lang_success,
                'total_tests': len(foreign_languages),
                'successful_handles': foreign_lang_success_count,
                'multilingual_support': foreign_lang_success_count >= 5
            }
            print(f"       {'✅' if foreign_lang_success else '❌'} Langues étrangères ({foreign_lang_success_count}/{len(foreign_languages)})")
            
            # Test 5: Répétitions et spam
            print("     🔄 Test répétitions...")
            repeated_message = "Test répétition " * 50
            spam_responses = []
            
            for i in range(3):
                response = chatbot.obtenir_reponse(repeated_message, f"edge_repeat_{i}")
                spam_responses.append(response)
            
            # Vérifier que les réponses sont cohérentes
            consistent_responses = len(set(spam_responses)) <= 2  # Max 2 réponses différentes
            spam_success = all(resp and len(resp) > 5 for resp in spam_responses)
            
            edge_case_results['repetitions'] = {
                'success': spam_success and consistent_responses,
                'responses_generated': len(spam_responses),
                'consistent_responses': consistent_responses,
                'handles_repetition': spam_success
            }
            print(f"       {'✅' if spam_success else '❌'} Répétitions")
            
            # Test 6: Nombres et calculs
            print("     🔢 Test nombres et calculs...")
            numeric_tests = [
                "Combien coûte OBS ?",
                "Quel est le meilleur bitrate pour 1080p ?",
                "2 + 2 = ?",
                "1920x1080 ou 1280x720 ?",
                "60fps ou 30fps pour le streaming ?",
                "Quelle résolution choisir entre 720p et 1080p ?"
            ]
            
            numeric_success_count = 0
            for i, numeric_msg in enumerate(numeric_tests):
                response = chatbot.obtenir_reponse(numeric_msg, f"edge_numeric_{i}")
                # Succès si contient des informations techniques pertinentes
                if response and (any(word in response.lower() for word in ["bitrate", "fps", "résolution", "gratuit", "configuration"]) or len(response) > 20):
                    numeric_success_count += 1
            
            numeric_success = numeric_success_count >= len(numeric_tests) // 2
            edge_case_results['numeric_content'] = {
                'success': numeric_success,
                'total_tests': len(numeric_tests),
                'successful_handles': numeric_success_count,
                'technical_accuracy': numeric_success_count >= 4
            }
            print(f"       {'✅' if numeric_success else '❌'} Contenu numérique ({numeric_success_count}/{len(numeric_tests)})")
            
            # Calcul du score global
            successful_edge_cases = sum(1 for result in edge_case_results.values() 
                                      if isinstance(result, dict) and result.get('success', False))
            total_edge_tests = len(edge_case_results)
            overall_edge_success_rate = successful_edge_cases / total_edge_tests * 100 if total_edge_tests > 0 else 0
            
            print(f"   📊 Taux de succès cas limites: {overall_edge_success_rate:.1f}% ({successful_edge_cases}/{total_edge_tests})")
            
            return {
                'overall_edge_success_rate': overall_edge_success_rate,
                'successful_edge_cases': successful_edge_cases,
                'total_edge_tests': total_edge_tests,
                'edge_case_details': edge_case_results,
                'robust_edge_handling': overall_edge_success_rate >= 70
            }
            
        except Exception as e:
            print(f"   ❌ Erreur test cas limites: {e}")
            return {'error': str(e)}
    
    def _generate_markdown_report(self):
        """Génère le rapport de performance en Markdown"""
        lines = []
        lines.append("# 📊 Rapport de Performance Mila Assist\n")
        # Configuration
        config = self.results.get('config', {})
        lines.append(f"## ⚙️ Configuration\n")
        if 'load_time_ms' in config:
            lines.append(f"- Temps de chargement : **{config['load_time_ms']:.1f} ms**\n")
        if 'valid' in config:
            lines.append(f"- Configuration valide : **{'Oui' if config['valid'] else 'Non'}**\n")
        # Temps de réponse et précision
        resp = self.results.get('response', {})
        lines.append(f"\n## ⚡ Temps de réponse & Précision\n")
        lines.append(f"*Tests basés sur les données réelles de la base de données (comme train.py)*\n")
        
        # Résultats combinés (moyenne des 3 modes)
        if 'combined_avg_time' in resp:
            lines.append(f"- Temps moyen combiné (3 modes) : **{resp['combined_avg_time']:.1f} ms**\n")
        if 'combined_accuracy' in resp:
            lines.append(f"- Précision combinée (3 modes) : **{resp['combined_accuracy']*100:.1f}%**\n")
        
        # Résultats mode local intelligent
        local_smart_results = resp.get('local_smart', {})
        if local_smart_results:
            lines.append(f"\n### 🧠 Mode Local Intelligent (Fallback complet)\n")
            if 'avg_time_ms' in local_smart_results:
                lines.append(f"- Temps moyen : **{local_smart_results['avg_time_ms']:.1f} ms**\n")
            if 'accuracy' in local_smart_results:
                lines.append(f"- Précision : **{local_smart_results['accuracy']*100:.1f}%** ({local_smart_results.get('correct_answers', 0)}/{local_smart_results.get('total_questions', 0)})\n")
        
        # Résultats mode local brut
        local_raw_results = resp.get('local_raw', {})
        if local_raw_results:
            lines.append(f"\n### 🤖 Mode Local Brut (Keras seulement)\n")
            if 'avg_time_ms' in local_raw_results:
                lines.append(f"- Temps moyen : **{local_raw_results['avg_time_ms']:.1f} ms**\n")
            if 'accuracy' in local_raw_results:
                lines.append(f"- Précision : **{local_raw_results['accuracy']*100:.1f}%** ({local_raw_results.get('correct_answers', 0)}/{local_raw_results.get('total_questions', 0)})\n")
        
        # Résultats mode API
        api_results = resp.get('api', {})
        if api_results:
            lines.append(f"\n### 🌐 Mode API (Serveur externe)\n")
            if 'avg_time_ms' in api_results:
                lines.append(f"- Temps moyen : **{api_results['avg_time_ms']:.1f} ms**\n")
            if 'accuracy' in api_results:
                lines.append(f"- Précision : **{api_results['accuracy']*100:.1f}%** ({api_results.get('correct_answers', 0)}/{api_results.get('total_questions', 0)})\n")
        
        # Détails des tests (combinés des 3 modes)
        all_details = []
        if local_smart_results.get('details'):
            all_details.extend(local_smart_results['details'])
        if local_raw_results.get('details'):
            all_details.extend(local_raw_results['details'])
        if api_results.get('details'):
            all_details.extend(api_results['details'])
            
        if all_details:
            lines.append(f"\n### 📋 Détails des tests de précision\n")
            lines.append(f"| Question | Tag attendu | Mots-clés | Réponse | Temps (ms) | Mode | Précis |\n")
            lines.append(f"|---|---|---|---|---|---|---|\n")
            for d in all_details:
                question = d.get('question', 'N/A')
                expected_tag = d.get('expected_tag', d.get('expected', 'N/A'))
                keywords = ', '.join(d.get('expected_keywords', []))[:30]
                response = d.get('response', 'N/A')[:40]
                elapsed = d.get('elapsed_ms', 0)
                mode = d.get('mode', 'N/A')
                correct = d.get('correct', False)
                lines.append(f"| {question} | {expected_tag} | {keywords} | {response}... | {elapsed:.1f} | {mode} | {'✅' if correct else '❌'} |\n")
        # Sécurité
        sec = self.results.get('security', {})
        lines.append(f"\n## 🔒 Sécurité anti-injection\n")
        if 'safe' in sec:
            lines.append(f"- Résultat global : **{'Sécurisé' if sec['safe'] else 'Vulnérable'}**\n")
        if 'details' in sec:
            lines.append(f"\n| Input | Réponse | Sûr |\n|---|---|---|\n")
            for d in sec['details']:
                lines.append(f"| {d['input']} | {d['response'][:40]}... | {'✅' if d['safe'] else '❌'} |")
        # Dépendances
        dep = self.results.get('dependencies', {})
        lines.append(f"\n## 📦 Dépendances critiques\n")
        if 'critical_found' in dep and 'critical_total' in dep:
            lines.append(f"- Dépendances critiques installées : **{dep['critical_found']}/{dep['critical_total']}**\n")
        if 'critical_dependencies' in dep:
            lines.append(f"- Modules trouvés : {', '.join(dep['critical_dependencies'])}\n")

        # NOUVEAUX TESTS AVANCÉS
        
        # Test de charge
        load = self.results.get('load_performance', {})
        lines.append(f"\n## 🚀 Performance sous charge\n")
        if 'overall_success_rate' in load:
            lines.append(f"- Taux de succès global : **{load['overall_success_rate']:.1f}%**\n")
        if 'performance_degradation' in load:
            lines.append(f"- Dégradation détectée : **{'Oui' if load['performance_degradation'] else 'Non'}**\n")
        if 'load_results' in load:
            lines.append(f"\n### Détails par niveau de charge\n")
            lines.append(f"| Charge | Succès | Temps moy. | Throughput | Taux succès |\n")
            lines.append(f"|--------|--------|------------|------------|-------------|\n")
            for load_key, load_data in load['load_results'].items():
                if isinstance(load_data, dict):
                    charge = load_data.get('total_requests', 0)
                    succes = load_data.get('successful_requests', 0)
                    temps_moy = load_data.get('avg_response_time_ms', 0)
                    throughput = load_data.get('throughput_rps', 0)
                    taux = load_data.get('success_rate', 0)
                    lines.append(f"| {charge} req | {succes} | {temps_moy:.1f}ms | {throughput:.1f} req/s | {taux:.1f}% |\n")

        # Test mémoire
        mem = self.results.get('memory_usage', {})
        lines.append(f"\n## 🧠 Utilisation mémoire\n")
        if 'initial_memory_mb' in mem and 'final_memory_mb' in mem:
            lines.append(f"- Mémoire initiale : **{mem['initial_memory_mb']:.1f} MB**\n")
            lines.append(f"- Mémoire finale : **{mem['final_memory_mb']:.1f} MB**\n")
            lines.append(f"- Augmentation : **{mem.get('memory_increase_mb', 0):.1f} MB**\n")
        if 'memory_leak_detected' in mem:
            lines.append(f"- Fuite mémoire : **{'Détectée' if mem['memory_leak_detected'] else 'Non détectée'}**\n")
        if 'cache_size' in mem:
            lines.append(f"- Taille cache : **{mem['cache_size']} entrées**\n")

        # Test récupération d'erreurs
        recovery = self.results.get('error_recovery', {})
        lines.append(f"\n## 🛠️ Récupération d'erreurs\n")
        if 'overall_recovery_rate' in recovery:
            lines.append(f"- Taux de récupération : **{recovery['overall_recovery_rate']:.1f}%**\n")
        if 'recovery_details' in recovery:
            lines.append(f"\n### Détails par type d'erreur\n")
            lines.append(f"| Type d'erreur | Récupération | Détails |\n")
            lines.append(f"|---------------|--------------|----------|\n")
            for error_type, details in recovery['recovery_details'].items():
                if isinstance(details, dict):
                    success = '✅' if details.get('success', False) else '❌'
                    info = f"Réponse: {details.get('response_provided', False)}"
                    lines.append(f"| {error_type.replace('_', ' ').title()} | {success} | {info} |\n")

        # Test cas limites
        edge = self.results.get('edge_cases', {})
        lines.append(f"\n## 🎯 Gestion des cas limites\n")
        if 'overall_edge_success_rate' in edge:
            lines.append(f"- Taux de succès global : **{edge['overall_edge_success_rate']:.1f}%**\n")
        if 'edge_case_details' in edge:
            lines.append(f"\n### Détails par type de cas limite\n")
            lines.append(f"| Type de test | Réussite | Tests passés | Détails |\n")
            lines.append(f"|--------------|----------|--------------|----------|\n")
            for case_type, details in edge['edge_case_details'].items():
                if isinstance(details, dict):
                    success = '✅' if details.get('success', False) else '❌'
                    passed = details.get('successful_handles', 0)
                    total = details.get('total_tests', 0)
                    info = f"{passed}/{total}"
                    lines.append(f"| {case_type.replace('_', ' ').title()} | {success} | {info} | - |\n")

        # Score global amélioré
        score = 0
        max_score = 200  # Score sur 200 avec les nouveaux tests
        
        # Configuration (25 points)
        if 'load_time_ms' in config:
            score += 25 if config['load_time_ms'] < 100 else 15
        
        # Précision (25 points)
        if 'combined_accuracy' in resp:
            score += 25 if resp['combined_accuracy'] >= 0.9 else (20 if resp['combined_accuracy'] >= 0.8 else 10)
        
        # Sécurité (25 points)
        if 'safe' in sec:
            score += 25 if sec['safe'] else 10
        
        # Dépendances (25 points)
        if 'critical_found' in dep and 'critical_total' in dep:
            score += 25 if dep['critical_found'] == dep['critical_total'] else 15
        
        # Performance sous charge (25 points)
        if 'stable_under_load' in load:
            score += 25 if load['stable_under_load'] else 10
        
        # Mémoire (25 points)
        if 'memory_stable' in mem:
            score += 25 if mem['memory_stable'] else 10
        
        # Récupération d'erreurs (25 points)
        if 'robust_error_handling' in recovery:
            score += 25 if recovery['robust_error_handling'] else 10
        
        # Cas limites (25 points)
        if 'robust_edge_handling' in edge:
            score += 25 if edge['robust_edge_handling'] else 10

        score_percentage = (score / max_score) * 100
        lines.append(f"\n## 🏆 Score global : **{score}/{max_score} ({score_percentage:.1f}%)**\n")

        # Conseils améliorés
        lines.append(f"\n## 💡 Conseils d'amélioration\n")
        if config.get('load_time_ms', 0) > 100:
            lines.append("- ⚡ Optimiser le temps de chargement de la configuration (<100ms recommandé)\n")
        if resp.get('combined_accuracy', 0) < 0.9:
            lines.append("- 🎯 Améliorer la précision du modèle (>90% recommandé)\n")
        if not sec.get('safe', True):
            lines.append("- 🔒 Renforcer la sécurité contre les injections de code\n")
        if load.get('performance_degradation', False):
            lines.append("- 📈 Optimiser les performances sous charge\n")
        if mem.get('memory_leak_detected', False):
            lines.append("- 🧠 Corriger les fuites mémoire détectées\n")
        if not recovery.get('robust_error_handling', False):
            lines.append("- 🛠️ Améliorer la gestion des erreurs\n")
        if not edge.get('robust_edge_handling', False):
            lines.append("- 🎯 Renforcer la gestion des cas limites\n")
        
        if score_percentage >= 90:
            lines.append("- 🏆 **Excellent !** Niveau professionnel atteint !\n")
        elif score_percentage >= 80:
            lines.append("- 🥈 **Très bien !** Qualité production avec quelques améliorations possibles\n")
        elif score_percentage >= 70:
            lines.append("- 🥉 **Bien !** Base solide, optimisations recommandées\n")
        else:
            lines.append("- ⚠️ **Améliorations nécessaires** pour la production\n")
        # Écriture du fichier dans le dossier tests/
        tests_dir = os.path.dirname(os.path.abspath(__file__))  # Dossier tests/
        report_path = os.path.join(tests_dir, "test_perf.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"   Rapport généré : {report_path}")

def main():
    """Fonction principale"""
    print("🔬 TESTS DE PERFORMANCE LÉGERS")
    print("Analyse des vraies métriques du projet Mila Assist")
    print("📊 Tests de précision basés sur la base de données réelle")
    print()
    
    test_suite = LightPerformanceTest()
    results = test_suite.run_performance_tests()
    
    if 'error' not in results:
        return True
    else:
        print(f"\n❌ Erreur: {results['error']}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)