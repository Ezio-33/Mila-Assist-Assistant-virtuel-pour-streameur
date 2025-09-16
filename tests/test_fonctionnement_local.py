#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DU FONCTIONNEMENT LOCAL - MILA ASSIST RNCP 6
================================================

Suite de tests complète pour valider le fonctionnement en mode local
Conforme aux exigences RNCP 6 - Concepteur Développeur d'Applications

Tests couverts:
- Configuration et initialisation
- Fallback Keras quand API indisponible
- Prédictions du modèle local
- Gestion des sessions
- Performance et métriques
- Intégration complète

Auteur: Concepteur Développeur d'Applications RNCP 6
Date: 2025-01-15
"""

import os
import sys
import time
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.app_config import AppConfig, ConfigurationError
    from services.chatbot_service import ChatbotService
    from services.session_service import SessionService
    from services.api_client import ApiClient
    from app import create_app
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("💡 Assurez-vous d'être dans le bon répertoire et que tous les modules sont disponibles")
    sys.exit(1)

class TestConfiguration(unittest.TestCase):
    """Tests de la configuration"""
    
    def setUp(self):
        """Préparation des tests"""
        self.original_env = os.environ.copy()
    
    def tearDown(self):
        """Nettoyage après tests"""
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_configuration_par_defaut(self):
        """Test de la configuration par défaut"""
        # Configuration minimale
        os.environ.update({
            'API_URL': 'https://test.example.com/api',
            'API_KEY': 'test_key_1234567890'
        })
        
        config = AppConfig()
        self.assertEqual(config.API_URL, 'https://test.example.com/api')
        self.assertEqual(config.API_KEY, 'test_key_1234567890')
        self.assertTrue(config.USE_API)
        self.assertTrue(config.USE_LEGACY_FALLBACK)
        self.assertEqual(config.RESPONSE_MODE, 'balanced')
    
    def test_validation_configuration(self):
        """Test de la validation de configuration"""
        # Configuration invalide - pas d'API_KEY
        os.environ.update({
            'API_URL': 'https://test.example.com/api'
        })
        
        with self.assertRaises(ConfigurationError):
            AppConfig()
    
    def test_mode_fallback_uniquement(self):
        """Test de la configuration en mode fallback uniquement"""
        os.environ.update({
            'API_URL': 'https://test.example.com/api',
            'API_KEY': 'test_key_1234567890',
            'USE_API': 'false',
            'USE_LEGACY_FALLBACK': 'true'
        })
        
        config = AppConfig()
        self.assertFalse(config.USE_API)
        self.assertTrue(config.USE_LEGACY_FALLBACK)

class TestFallbackKeras(unittest.TestCase):
    """Tests du système de fallback Keras"""
    
    def setUp(self):
        """Préparation des tests"""
        # Configuration pour mode local
        os.environ.update({
            'API_URL': 'http://localhost:99999/api',  # API invalide pour forcer fallback
            'API_KEY': 'test_key_1234567890',
            'USE_LEGACY_FALLBACK': 'true',
            'DEBUG': 'true'
        })
        
        self.config = AppConfig()
        
        # Mock des fichiers du modèle si ils n'existent pas
        self.temp_dir = tempfile.mkdtemp()
        self.config.BASE_DIR = self.temp_dir
        self.config.MODEL_PATH = os.path.join(self.temp_dir, "chatbot_model.keras")
        self.config.WORDS_PATH = os.path.join(self.temp_dir, "words.pkl")
        self.config.CLASSES_PATH = os.path.join(self.temp_dir, "classes.pkl")
        
        # Créer des fichiers mock si nécessaire
        self._create_mock_model_files()
    
    def tearDown(self):
        """Nettoyage après tests"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _create_mock_model_files(self):
        """Créer des fichiers de modèle mock pour les tests"""
        import pickle
        
        # Mock words.pkl
        mock_words = ['bonjour', 'salut', 'comment', 'allez', 'vous', 'aide', 'merci']
        with open(self.config.WORDS_PATH, 'wb') as f:
            pickle.dump(mock_words, f)
        
        # Mock classes.pkl
        mock_classes = ['greeting', 'help', 'thanks']
        with open(self.config.CLASSES_PATH, 'wb') as f:
            pickle.dump(mock_classes, f)
        
        # Note: Le modèle Keras sera mocké dans les tests
    
    @patch('services.chatbot_service.TENSORFLOW_AVAILABLE', True)
    @patch('services.chatbot_service.load_model')
    def test_chargement_modele_keras(self, mock_load_model):
        """Test du chargement du modèle Keras"""
        # Mock du modèle TensorFlow
        mock_model = MagicMock()
        mock_model.predict.return_value = [[0.8, 0.1, 0.1]]  # Prédiction mock
        mock_load_model.return_value = mock_model
        
        service = ChatbotService(self.config)
        
        # Vérifications
        self.assertIsNotNone(service.model)
        self.assertIsNotNone(service.words)
        self.assertIsNotNone(service.classes)
        self.assertEqual(len(service.words), 7)  # Nos mots mock
        self.assertEqual(len(service.classes), 3)  # Nos classes mock
    
    @patch('services.chatbot_service.TENSORFLOW_AVAILABLE', True)
    @patch('services.chatbot_service.load_model')
    def test_prediction_keras(self, mock_load_model):
        """Test des prédictions avec le modèle Keras"""
        # Mock du modèle avec prédiction forte pour 'greeting'
        mock_model = MagicMock()
        mock_model.predict.return_value = [[0.9, 0.05, 0.05]]
        mock_load_model.return_value = mock_model
        
        service = ChatbotService(self.config)
        
        # Test d'une prédiction
        message = "bonjour comment allez vous"
        reponse = service._obtenir_reponse_keras_amelioree(message)
        
        self.assertIsNotNone(reponse)
        self.assertIsInstance(reponse, str)
        self.assertGreater(len(reponse), 0)
    
    @patch('services.chatbot_service.TENSORFLOW_AVAILABLE', True)
    @patch('services.chatbot_service.load_model')
    def test_fallback_api_vers_keras(self, mock_load_model):
        """Test du fallback API vers Keras"""
        # Mock du modèle
        mock_model = MagicMock()
        mock_model.predict.return_value = [[0.8, 0.1, 0.1]]
        mock_load_model.return_value = mock_model
        
        service = ChatbotService(self.config)
        
        # Test avec API indisponible (ce qui est le cas avec notre config)
        session_id = "test_session_123"
        message = "bonjour"
        
        reponse = service.obtenir_reponse(message, session_id)
        
        # Vérifications
        self.assertIsNotNone(reponse)
        self.assertIsInstance(reponse, str)
        self.assertGreater(len(reponse), 0)
        
        # Vérifier que le fallback a été utilisé
        stats = service.obtenir_statistiques()
        self.assertGreater(stats['keras_fallback_used'], 0)
    
    def test_fallback_sans_modele(self):
        """Test du comportement quand le modèle n'est pas disponible"""
        # Supprimer les fichiers du modèle
        for path in [self.config.MODEL_PATH, self.config.WORDS_PATH, self.config.CLASSES_PATH]:
            if os.path.exists(path):
                os.remove(path)
        
        service = ChatbotService(self.config)
        
        # Le service doit se rabattre sur des réponses par défaut
        session_id = "test_session_456"
        message = "test"
        
        reponse = service.obtenir_reponse(message, session_id)
        
        # Doit retourner une réponse par défaut
        self.assertIsNotNone(reponse)
        self.assertIn("base de connaissances", reponse.lower())

class TestGestionSessions(unittest.TestCase):
    """Tests de la gestion des sessions"""
    
    def setUp(self):
        """Préparation des tests"""
        self.session_service = SessionService()
    
    def test_creation_session(self):
        """Test de création de session"""
        session_id = self.session_service.create_session()
        
        self.assertIsNotNone(session_id)
        self.assertIsInstance(session_id, str)
        self.assertTrue(session_id.startswith('session_'))
        self.assertTrue(self.session_service.is_valid_session(session_id))
    
    def test_validation_session(self):
        """Test de validation de session"""
        # Session valide
        session_id = self.session_service.create_session()
        self.assertTrue(self.session_service.is_valid_session(session_id))
        
        # Session invalide
        self.assertFalse(self.session_service.is_valid_session("invalid_session"))
        self.assertFalse(self.session_service.is_valid_session(""))
        self.assertFalse(self.session_service.is_valid_session(None))
    
    def test_mise_a_jour_activite(self):
        """Test de mise à jour de l'activité de session"""
        session_id = self.session_service.create_session()
        
        # Simuler de l'activité
        self.session_service.update_session_activity(session_id, 150.0)
        self.session_service.update_session_activity(session_id, 200.0)
        
        # Vérifier les statistiques
        session = self.session_service.get_session(session_id)
        self.assertIsNotNone(session)
        self.assertEqual(session['message_count'], 2)
        self.assertAlmostEqual(session['average_response_time'], 175.0, places=1)
    
    def test_nettoyage_sessions_expirees(self):
        """Test du nettoyage des sessions expirées"""
        # Créer une session
        session_id = self.session_service.create_session()
        initial_count = self.session_service.get_active_sessions_count()
        
        # Simuler l'expiration en modifiant directement l'heure
        session = self.session_service._sessions[session_id]
        session['last_activity'] = datetime.now() - self.session_service._session_timeout * 2
        
        # Nettoyer
        self.session_service.cleanup_expired_sessions()
        
        # Vérifier que la session a été supprimée
        self.assertLess(self.session_service.get_active_sessions_count(), initial_count)
        self.assertFalse(self.session_service.is_valid_session(session_id))

class TestPerformance(unittest.TestCase):
    """Tests de performance"""
    
    def setUp(self):
        """Préparation des tests"""
        os.environ.update({
            'API_URL': 'http://localhost:99999/api',
            'API_KEY': 'test_key_1234567890',
            'USE_LEGACY_FALLBACK': 'true',
            'DEBUG': 'false'  # Désactiver le debug pour des tests de performance
        })
        
        self.config = AppConfig()
    
    @patch('services.chatbot_service.TENSORFLOW_AVAILABLE', True)
    @patch('services.chatbot_service.load_model')
    def test_temps_reponse_local(self, mock_load_model):
        """Test du temps de réponse en mode local"""
        # Mock d'un modèle rapide
        mock_model = MagicMock()
        mock_model.predict.return_value = [[0.8, 0.1, 0.1]]
        mock_load_model.return_value = mock_model
        
        # Créer des fichiers mock temporaires
        temp_dir = tempfile.mkdtemp()
        try:
            self.config.BASE_DIR = temp_dir
            self.config.MODEL_PATH = os.path.join(temp_dir, "chatbot_model.keras")
            self.config.WORDS_PATH = os.path.join(temp_dir, "words.pkl")
            self.config.CLASSES_PATH = os.path.join(temp_dir, "classes.pkl")
            
            # Créer les fichiers mock
            import pickle
            with open(self.config.WORDS_PATH, 'wb') as f:
                pickle.dump(['test', 'bonjour', 'aide'], f)
            with open(self.config.CLASSES_PATH, 'wb') as f:
                pickle.dump(['greeting', 'help'], f)
            
            service = ChatbotService(self.config)
            
            # Test de performance
            session_id = "perf_test_session"
            message = "bonjour test"
            
            start_time = time.time()
            reponse = service.obtenir_reponse(message, session_id)
            response_time = (time.time() - start_time) * 1000
            
            # Vérifications
            self.assertIsNotNone(reponse)
            self.assertLess(response_time, 2000)  # Moins de 2 secondes
            
            print(f"⏱️ Temps de réponse local: {response_time:.2f}ms")
            
        finally:
            shutil.rmtree(temp_dir)
    
    def test_cache_predictions(self):
        """Test du cache des prédictions"""
        # Ce test nécessiterait un mock plus complexe du service
        # Pour l'instant, on vérifie juste que les méthodes existent
        
        service = ChatbotService(self.config)
        
        # Vérifier que les méthodes de cache existent
        self.assertTrue(hasattr(service, '_generer_cache_key'))
        self.assertTrue(hasattr(service, '_mettre_en_cache_prediction'))
        self.assertTrue(hasattr(service, 'vider_cache_predictions'))

class TestIntegrationComplete(unittest.TestCase):
    """Tests d'intégration complète"""
    
    def setUp(self):
        """Préparation des tests d'intégration"""
        os.environ.update({
            'API_URL': 'http://localhost:99999/api',  # API invalide
            'API_KEY': 'test_key_1234567890',
            'USE_LEGACY_FALLBACK': 'true',
            'DEBUG': 'true'
        })
    
    @patch('services.chatbot_service.TENSORFLOW_AVAILABLE', True)
    @patch('services.chatbot_service.load_model')
    def test_integration_app_complete(self, mock_load_model):
        """Test d'intégration de l'application complète"""
        # Mock du modèle
        mock_model = MagicMock()
        mock_model.predict.return_value = [[0.8, 0.1, 0.1]]
        mock_load_model.return_value = mock_model
        
        # Créer des fichiers temporaires
        temp_dir = tempfile.mkdtemp()
        try:
            # Patch des chemins de fichiers
            with patch.object(AppConfig, 'BASE_DIR', temp_dir):
                # Créer les fichiers mock
                import pickle
                words_path = os.path.join(temp_dir, "words.pkl")
                classes_path = os.path.join(temp_dir, "classes.pkl")
                
                with open(words_path, 'wb') as f:
                    pickle.dump(['bonjour', 'aide', 'merci'], f)
                with open(classes_path, 'wb') as f:
                    pickle.dump(['greeting', 'help', 'thanks'], f)
                
                # Créer l'application
                app_instance = create_app()
                
                # Vérifications
                self.assertIsNotNone(app_instance)
                self.assertIsNotNone(app_instance.app)
                self.assertIsNotNone(app_instance.services)
                
                # Vérifier que les services sont initialisés
                self.assertIn('chatbot', app_instance.services)
                self.assertIn('session', app_instance.services)
                self.assertIn('feedback', app_instance.services)
                
                # Test de création de session
                session_service = app_instance.services['session']
                session_id = session_service.create_session()
                self.assertTrue(session_service.is_valid_session(session_id))
                
                # Test de réponse chatbot
                chatbot_service = app_instance.services['chatbot']
                reponse = chatbot_service.obtenir_reponse("bonjour", session_id)
                self.assertIsNotNone(reponse)
                self.assertIsInstance(reponse, str)
                
                print("✅ Test d'intégration complète réussi")
                
        finally:
            shutil.rmtree(temp_dir)

def run_diagnostic_complet():
    """Exécuter un diagnostic complet du système"""
    print("🔍 DIAGNOSTIC COMPLET DU SYSTÈME LOCAL")
    print("=" * 50)
    
    # 1. Test de la configuration
    print("\n📋 Test de configuration...")
    try:
        os.environ.update({
            'API_URL': 'http://localhost:99999/api',
            'API_KEY': 'test_key_diagnostic_1234567890',
            'USE_LEGACY_FALLBACK': 'true'
        })
        config = AppConfig()
        print("✅ Configuration valide")
        print(f"   - API URL: {config.API_URL}")
        print(f"   - Fallback Keras: {config.USE_LEGACY_FALLBACK}")
        print(f"   - Mode réponse: {config.RESPONSE_MODE}")
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False
    
    # 2. Test des fichiers du modèle
    print("\n🧠 Test des fichiers du modèle...")
    model_status = config.validate_model_files()
    for file_type, exists in model_status.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {file_type}: {'Présent' if exists else 'Manquant'}")
    
    if not all(model_status.values()):
        print("⚠️ Certains fichiers du modèle sont manquants")
        print("💡 Exécutez train.py pour créer/mettre à jour le modèle")
    
    # 3. Test des imports
    print("\n📦 Test des dépendances...")
    try:
        import tensorflow
        print("✅ TensorFlow disponible")
    except ImportError:
        print("❌ TensorFlow non disponible")
    
    try:
        import nltk
        print("✅ NLTK disponible")
    except ImportError:
        print("❌ NLTK non disponible")
    
    # 4. Test d'un service simple
    print("\n🔧 Test des services...")
    try:
        session_service = SessionService()
        session_id = session_service.create_session()
        print(f"✅ Service de session fonctionnel (ID: {session_id[:20]}...)")
    except Exception as e:
        print(f"❌ Erreur service de session: {e}")
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 50)
    
    if all(model_status.values()):
        print("🎉 Système prêt pour fonctionnement local complet")
        print("💡 L'application peut utiliser le fallback Keras")
    else:
        print("⚠️ Système partiellement fonctionnel")
        print("💡 Entraînez le modèle pour un fonctionnement optimal")
    
    return True

def main():
    """Fonction principale des tests"""
    print("🧪 SUITE DE TESTS - MILA ASSIST RNCP 6")
    print("=" * 50)
    
    # Exécuter le diagnostic
    diagnostic_ok = run_diagnostic_complet()
    
    if not diagnostic_ok:
        print("❌ Diagnostic échoué - arrêt des tests")
        return
    
    # Exécuter les tests unitaires
    print("\n🔬 EXÉCUTION DES TESTS UNITAIRES")
    print("=" * 50)
    
    # Découvrir et exécuter tous les tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 Tous les tests ont réussi !")
        print("✅ Le système fonctionne correctement en mode local")
    else:
        print("⚠️ Certains tests ont échoué")
        print("💡 Vérifiez les logs ci-dessus pour plus de détails")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)