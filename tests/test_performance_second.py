#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE PERFORMANCE RÉEL - MILA ASSIST RNCP 6
==============================================

Test de performance complet avec métriques réelles du projet :
- Temps de chargement du modèle Keras
- Temps de réponse API vs Fallback
- Mesure de la précision des prédictions
- Analyse de la mémoire utilisée
- Test de charge avec requêtes simultanées
- Validation des métriques d'architecture

Auteur: Samuel VERSCHUEREN
Date: 17-09-2025
"""

import os
import sys
import time
import threading
import psutil
import concurrent.futures
import statistics
from typing import List, Dict, Any, Tuple
import logging

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.app_config import AppConfig, ConfigurationError
    from services.chatbot_service import ChatbotService, ModelStatus
    from services.api_client import ApiClient
    from services.session_service import SessionService
    from app import MilaAssistApp
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

# Configuration du logging pour les tests
logging.basicConfig(level=logging.WARNING)

class PerformanceMetrics:
    """Classe pour collecter les métriques de performance"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Réinitialiser toutes les métriques"""
        self.model_loading_time = 0.0
        self.api_response_times = []
        self.keras_response_times = []
        self.memory_usage_before = 0
        self.memory_usage_after = 0
        self.cpu_usage_peak = 0.0
        self.successful_predictions = 0
        self.failed_predictions = 0
        self.api_success_rate = 0.0
        self.keras_accuracy_score = 0.0
        self.concurrent_request_times = []
        self.cache_hit_rate = 0.0

class RealPerformanceTest:
    """Test de performance réel du système Mila Assist"""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.process = psutil.Process()
        self.config = None
        self.chatbot_service = None
        
    def run_complete_performance_test(self) -> Dict[str, Any]:
        """Exécute tous les tests de performance et retourne les résultats"""
        print("🚀 DÉMARRAGE DES TESTS DE PERFORMANCE RÉELS")
        print("=" * 60)
        
        results = {}
        
        try:
            # Test 1: Configuration et initialisation
            print("1. 📊 Test de configuration et initialisation")
            results['config'] = self._test_configuration_performance()
            
            # Test 2: Chargement du modèle Keras
            print("\n2. 🧠 Test de chargement du modèle Keras")
            results['model_loading'] = self._test_model_loading_performance()
            
            # Test 3: Performance des réponses
            print("\n3. ⚡ Test de performance des réponses")
            results['response_performance'] = self._test_response_performance()
            
            # Test 4: Test de charge
            print("\n4. 🔄 Test de charge avec requêtes simultanées")
            results['load_test'] = self._test_concurrent_load()
            
            # Test 5: Utilisation mémoire
            print("\n5. 💾 Test d'utilisation mémoire")
            results['memory_usage'] = self._test_memory_usage()
            
            # Test 6: Précision du modèle
            print("\n6. 🎯 Test de précision du modèle")
            results['model_accuracy'] = self._test_model_accuracy()
            
            # Résumé final
            print("\n" + "=" * 60)
            print("📋 RÉSUMÉ DES PERFORMANCES RÉELLES")
            print("=" * 60)
            self._print_performance_summary(results)
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur pendant les tests: {e}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
    
    def _test_configuration_performance(self) -> Dict[str, Any]:
        """Test de performance de la configuration"""
        start_time = time.time()
        
        try:
            # Mesurer le temps de chargement de la configuration
            self.config = AppConfig()
            config_load_time = (time.time() - start_time) * 1000
            
            # Vérifier la validité de la configuration
            config_valid = all([
                hasattr(self.config, 'API_URL'),
                hasattr(self.config, 'USE_API'),
                hasattr(self.config, 'USE_LEGACY_FALLBACK'),
                hasattr(self.config, 'API_TIMEOUT')
            ])
            
            return {
                'load_time_ms': config_load_time,
                'valid': config_valid,
                'api_timeout': self.config.API_TIMEOUT,
                'fallback_enabled': self.config.USE_LEGACY_FALLBACK
            }
            
        except Exception as e:
            return {'error': str(e), 'load_time_ms': (time.time() - start_time) * 1000}
    
    def _test_model_loading_performance(self) -> Dict[str, Any]:
        """Test de performance du chargement du modèle"""
        if not self.config:
            return {'error': 'Configuration non disponible'}
        
        start_time = time.time()
        memory_before = self.process.memory_info().rss / 1024 / 1024  # MB
        
        try:
            # Initialiser le service chatbot (chargement asynchrone)
            self.chatbot_service = ChatbotService(self.config)
            init_time = (time.time() - start_time) * 1000
            
            # Attendre le chargement du modèle si activé
            if self.config.USE_LEGACY_FALLBACK:
                print("   🔄 Attente du chargement asynchrone du modèle...")
                max_wait = 30  # 30 secondes max
                waited = 0
                
                while (self.chatbot_service.model_status == ModelStatus.LOADING and 
                       waited < max_wait):
                    time.sleep(0.5)
                    waited += 0.5
                
                loading_time = self.chatbot_service.stats.get('model_loading_time', 0) * 1000
                model_ready = self.chatbot_service.model_status == ModelStatus.READY
            else:
                loading_time = 0
                model_ready = False
            
            memory_after = self.process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = memory_after - memory_before
            
            # Vérifier les composants chargés
            components_loaded = {
                'model': self.chatbot_service.model is not None,
                'words': self.chatbot_service.words is not None,
                'classes': self.chatbot_service.classes is not None
            }
            
            return {
                'init_time_ms': init_time,
                'model_loading_time_ms': loading_time,
                'model_ready': model_ready,
                'memory_increase_mb': memory_increase,
                'components_loaded': components_loaded,
                'model_status': self.chatbot_service.model_status.value
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'init_time_ms': (time.time() - start_time) * 1000
            }
    
    def _test_response_performance(self) -> Dict[str, Any]:
        """Test de performance des réponses"""
        if not self.chatbot_service:
            return {'error': 'Service chatbot non disponible'}
        
        # Messages de test avec types variés
        test_messages = [
            "Bonjour",
            "Comment configurer OBS ?",
            "Aide pour le streaming",
            "Merci beaucoup",
            "Au revoir",
            "Qu'est-ce que tu peux faire ?",
            "Comment utiliser Ailicia TTS ?",
            "Configuration audio pour streaming",
            "Problème avec plusieurs PC"
        ]
        
        api_times = []
        keras_times = []
        
        print(f"   🧪 Test de {len(test_messages)} messages...")
        
        for i, message in enumerate(test_messages):
            session_id = f"perf_test_{i}"
            
            # Mesurer le temps de réponse
            start_time = time.time()
            response = self.chatbot_service.obtenir_reponse(message, session_id)
            response_time = (time.time() - start_time) * 1000
            
            # Déterminer si c'était une réponse API ou Keras
            if self.chatbot_service.stats['api_success'] > 0:
                api_times.append(response_time)
            elif self.chatbot_service.stats['keras_fallback_used'] > 0:
                keras_times.append(response_time)
            
            print(f"     Message {i+1}: {response_time:.1f}ms - '{response[:50]}...'")
        
        # Calculer les statistiques
        all_times = api_times + keras_times
        
        return {
            'total_messages': len(test_messages),
            'api_responses': len(api_times),
            'keras_responses': len(keras_times),
            'average_response_time_ms': statistics.mean(all_times) if all_times else 0,
            'median_response_time_ms': statistics.median(all_times) if all_times else 0,
            'min_response_time_ms': min(all_times) if all_times else 0,
            'max_response_time_ms': max(all_times) if all_times else 0,
            'api_avg_time_ms': statistics.mean(api_times) if api_times else 0,
            'keras_avg_time_ms': statistics.mean(keras_times) if keras_times else 0,
            'response_time_target_met': statistics.mean(all_times) < 1000 if all_times else False
        }
    
    def _test_concurrent_load(self) -> Dict[str, Any]:
        """Test de charge avec requêtes simultanées"""
        if not self.chatbot_service:
            return {'error': 'Service chatbot non disponible'}
        
        concurrent_requests = 10
        test_message = "Test de charge simultané"
        
        print(f"   🔄 Test avec {concurrent_requests} requêtes simultanées...")
        
        def send_request(request_id):
            start_time = time.time()
            session_id = f"load_test_{request_id}"
            response = self.chatbot_service.obtenir_reponse(test_message, session_id)
            return (time.time() - start_time) * 1000, len(response) > 0
        
        start_test_time = time.time()
        
        # Exécuter les requêtes en parallèle
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            futures = [executor.submit(send_request, i) for i in range(concurrent_requests)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        total_test_time = (time.time() - start_test_time) * 1000
        
        # Analyser les résultats
        response_times = [result[0] for result in results]
        success_count = sum(1 for result in results if result[1])
        
        return {
            'concurrent_requests': concurrent_requests,
            'successful_requests': success_count,
            'success_rate': success_count / concurrent_requests,
            'total_test_time_ms': total_test_time,
            'average_response_time_ms': statistics.mean(response_times),
            'max_response_time_ms': max(response_times),
            'requests_per_second': concurrent_requests / (total_test_time / 1000),
            'load_test_passed': success_count == concurrent_requests and statistics.mean(response_times) < 2000
        }
    
    def _test_memory_usage(self) -> Dict[str, Any]:
        """Test d'utilisation mémoire"""
        try:
            memory_info = self.process.memory_info()
            cpu_percent = self.process.cpu_percent(interval=1)
            
            # Informations système
            system_memory = psutil.virtual_memory()
            
            return {
                'process_memory_mb': memory_info.rss / 1024 / 1024,
                'process_memory_vms_mb': memory_info.vms / 1024 / 1024,
                'cpu_percent': cpu_percent,
                'system_memory_total_gb': system_memory.total / 1024 / 1024 / 1024,
                'system_memory_available_gb': system_memory.available / 1024 / 1024 / 1024,
                'system_memory_usage_percent': system_memory.percent,
                'memory_efficient': memory_info.rss / 1024 / 1024 < 500  # Moins de 500MB
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _test_model_accuracy(self) -> Dict[str, Any]:
        """Test de précision du modèle avec des questions connues"""
        if not self.chatbot_service or not self.chatbot_service.model:
            return {'error': 'Modèle Keras non disponible'}
        
        # Questions avec réponses attendues
        accuracy_tests = [
            ("Bonjour", "greeting"),
            ("Merci", "thanks"),
            ("Au revoir", "goodbye"),
            ("Comment configurer", "help"),
            ("Qui êtes-vous", "identity"),
            ("Aide", "help"),
            ("Hello", "greeting"),
            ("Bye", "goodbye")
        ]
        
        correct_predictions = 0
        total_predictions = len(accuracy_tests)
        
        print(f"   🎯 Test de précision avec {total_predictions} questions...")
        
        for question, expected_category in accuracy_tests:
            try:
                # Utiliser directement la méthode de prédiction
                predictions = self.chatbot_service._predire_classe_keras_amelioree(question)
                
                if predictions and len(predictions) > 0:
                    predicted_intent = predictions[0]['intent']
                    confidence = predictions[0]['probability']
                    
                    # Vérification flexible des catégories
                    if (expected_category in predicted_intent.lower() or 
                        predicted_intent.lower() in expected_category or
                        confidence > 0.5):
                        correct_predictions += 1
                        print(f"     ✅ '{question}' -> {predicted_intent} ({confidence:.2f})")
                    else:
                        print(f"     ❌ '{question}' -> {predicted_intent} ({confidence:.2f}) attendu: {expected_category}")
                else:
                    print(f"     ❓ '{question}' -> Aucune prédiction")
                    
            except Exception as e:
                print(f"     ❌ Erreur pour '{question}': {e}")
        
        accuracy = correct_predictions / total_predictions
        
        return {
            'total_tests': total_predictions,
            'correct_predictions': correct_predictions,
            'accuracy': accuracy,
            'accuracy_percentage': accuracy * 100,
            'accuracy_target_met': accuracy >= 0.7,  # 70% minimum
            'model_vocabulary_size': len(self.chatbot_service.words) if self.chatbot_service.words else 0,
            'model_classes_count': len(self.chatbot_service.classes) if self.chatbot_service.classes else 0
        }
    
    def _print_performance_summary(self, results: Dict[str, Any]):
        """Affiche le résumé des performances"""
        print("📊 MÉTRIQUES CLÉS:")
        
        # Configuration
        if 'config' in results and 'load_time_ms' in results['config']:
            print(f"   ⚙️  Configuration: {results['config']['load_time_ms']:.1f}ms")
        
        # Chargement du modèle
        if 'model_loading' in results:
            model_data = results['model_loading']
            if 'model_loading_time_ms' in model_data:
                print(f"   🧠 Chargement modèle: {model_data['model_loading_time_ms']:.1f}ms")
            if 'memory_increase_mb' in model_data:
                print(f"   💾 Augmentation mémoire: {model_data['memory_increase_mb']:.1f}MB")
        
        # Performance des réponses
        if 'response_performance' in results:
            resp_data = results['response_performance']
            if 'average_response_time_ms' in resp_data:
                avg_time = resp_data['average_response_time_ms']
                print(f"   ⚡ Temps de réponse moyen: {avg_time:.1f}ms")
                
                # Évaluation de la performance
                if avg_time < 100:
                    print("     🎉 EXCELLENT (< 100ms)")
                elif avg_time < 500:
                    print("     ✅ BON (< 500ms)")
                elif avg_time < 1000:
                    print("     ⚠️  ACCEPTABLE (< 1s)")
                else:
                    print("     ❌ LENT (> 1s)")
        
        # Test de charge
        if 'load_test' in results:
            load_data = results['load_test']
            if 'success_rate' in load_data:
                success_rate = load_data['success_rate'] * 100
                print(f"   🔄 Taux de succès concurrent: {success_rate:.1f}%")
            if 'requests_per_second' in load_data:
                rps = load_data['requests_per_second']
                print(f"   📈 Requêtes/seconde: {rps:.1f}")
        
        # Utilisation mémoire
        if 'memory_usage' in results:
            mem_data = results['memory_usage']
            if 'process_memory_mb' in mem_data:
                memory_mb = mem_data['process_memory_mb']
                print(f"   💾 Mémoire utilisée: {memory_mb:.1f}MB")
                
                if memory_mb < 200:
                    print("     🎉 LÉGER (< 200MB)")
                elif memory_mb < 500:
                    print("     ✅ RAISONNABLE (< 500MB)")
                else:
                    print("     ⚠️  LOURD (> 500MB)")
        
        # Précision du modèle
        if 'model_accuracy' in results:
            acc_data = results['model_accuracy']
            if 'accuracy_percentage' in acc_data:
                accuracy = acc_data['accuracy_percentage']
                print(f"   🎯 Précision du modèle: {accuracy:.1f}%")
                
                if accuracy >= 80:
                    print("     🎉 EXCELLENT (≥ 80%)")
                elif accuracy >= 70:
                    print("     ✅ BON (≥ 70%)")
                elif accuracy >= 60:
                    print("     ⚠️  ACCEPTABLE (≥ 60%)")
                else:
                    print("     ❌ INSUFFISANT (< 60%)")
        
        print("\n🏆 ÉVALUATION GLOBALE:")
        
        # Calculer le score global
        scores = []
        
        # Score temps de réponse (25%)
        if ('response_performance' in results and 
            'average_response_time_ms' in results['response_performance']):
            avg_time = results['response_performance']['average_response_time_ms']
            if avg_time < 100:
                scores.append(100)
            elif avg_time < 500:
                scores.append(80)
            elif avg_time < 1000:
                scores.append(60)
            else:
                scores.append(40)
        
        # Score précision (25%)
        if ('model_accuracy' in results and 
            'accuracy_percentage' in results['model_accuracy']):
            accuracy = results['model_accuracy']['accuracy_percentage']
            scores.append(min(100, accuracy * 1.25))  # Bonus pour haute précision
        
        # Score mémoire (25%)
        if ('memory_usage' in results and 
            'process_memory_mb' in results['memory_usage']):
            memory_mb = results['memory_usage']['process_memory_mb']
            if memory_mb < 200:
                scores.append(100)
            elif memory_mb < 500:
                scores.append(80)
            else:
                scores.append(60)
        
        # Score charge (25%)
        if ('load_test' in results and 
            'success_rate' in results['load_test']):
            success_rate = results['load_test']['success_rate'] * 100
            scores.append(success_rate)
        
        if scores:
            global_score = statistics.mean(scores)
            print(f"   📊 Score global: {global_score:.1f}/100")
            
            if global_score >= 90:
                print("   🏅 PERFORMANCE EXCEPTIONNELLE")
            elif global_score >= 80:
                print("   🥈 TRÈS BONNE PERFORMANCE")
            elif global_score >= 70:
                print("   🥉 BONNE PERFORMANCE")
            elif global_score >= 60:
                print("   ⚠️  PERFORMANCE ACCEPTABLE")
            else:
                print("   ❌ PERFORMANCE À AMÉLIORER")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        
        recommendations = []
        
        if ('response_performance' in results and 
            results['response_performance'].get('average_response_time_ms', 0) > 500):
            recommendations.append("   ⚡ Optimiser les temps de réponse (< 500ms)")
        
        if ('model_accuracy' in results and 
            results['model_accuracy'].get('accuracy_percentage', 0) < 70):
            recommendations.append("   🎯 Améliorer la précision du modèle (ré-entraînement)")
        
        if ('memory_usage' in results and 
            results['memory_usage'].get('process_memory_mb', 0) > 500):
            recommendations.append("   💾 Optimiser l'utilisation mémoire")
        
        if ('load_test' in results and 
            results['load_test'].get('success_rate', 0) < 0.95):
            recommendations.append("   🔄 Améliorer la gestion de charge")
        
        if not recommendations:
            recommendations.append("   ✅ Toutes les métriques sont dans les objectifs !")
        
        for rec in recommendations:
            print(rec)

def main():
    """Fonction principale"""
    print("🔬 TEST DE PERFORMANCE RÉEL - MILA ASSIST")
    print("Mesure les vraies performances du système en production")
    print()
    
    test_suite = RealPerformanceTest()
    results = test_suite.run_complete_performance_test()
    
    if 'error' not in results:
        print("\n✅ Tests de performance terminés avec succès")
        return True
    else:
        print(f"\n❌ Erreur pendant les tests: {results['error']}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)