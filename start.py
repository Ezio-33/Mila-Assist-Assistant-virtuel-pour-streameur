#!/usr/bin/env python3

"""
Script de démarrage principal pour Mila Assist v2.0 - VERSION RNCP 6
========================================================================

VERSION ASYNCHRONE:
- Démarrage instantané de l'interface utilisateur (< 1 seconde)
- Chargement du modèle Keras en arrière-plan sans bloquer
- Interface utilisable immédiatement même pendant le chargement
- Basculement transparent vers le fallback local quand prêt
- Monitoring en temps réel du statut de chargement

Modes de lancement:
- web: Interface web avec chargement asynchrone
- full: Mode complet (identique à web avec nouvelle architecture)
- install: Installation des dépendances

Note importante:
L'application démarre instantanément et l'utilisateur peut commencer 
à l'utiliser immédiatement. Le modèle Keras se charge silencieusement
en arrière-plan pour offrir un fallback robuste en cas de coupure API.
Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import os
import sys
import argparse
import subprocess
import requests
import threading
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_async_compatibility():
    """Vérifier la compatibilité avec le mode asynchrone"""
    try:
        # Vérifier que TensorFlow est disponible (pour le fallback)
        import tensorflow as tf
        tf_version = tf.__version__
        logger.info(f"✅ TensorFlow {tf_version} disponible pour le fallback asynchrone")
        return True, tf_version
    except ImportError:
        logger.warning("⚠️ TensorFlow non disponible - fallback Keras désactivé")
        return False, None

def monitor_model_loading(host='localhost', port=5000, max_wait=30):
    """Monitorer le chargement du modèle en temps réel"""
    print("\n🔍 Monitoring du chargement asynchrone du modèle...")
    print("-" * 50)
    
    base_url = f"http://{host}:{port}"
    start_time = time.time()
    
    for attempt in range(max_wait):
        try:
            response = requests.get(f"{base_url}/model_status", timeout=2)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status', 'unknown')
                message = data.get('message', 'Pas de message')
                loading_time = data.get('loading_time', 0)
                
                elapsed = time.time() - start_time
                
                if status == 'loading':
                    print(f"🔄 [{elapsed:4.1f}s] {message}")
                elif status == 'ready':
                    print(f"✅ [{elapsed:4.1f}s] Modèle prêt ! Temps de chargement: {loading_time:.2f}s")
                    print("🎉 Fallback Keras maintenant disponible")
                    break
                elif status == 'error':
                    print(f"❌ [{elapsed:4.1f}s] Erreur: {message}")
                    break
                elif status == 'disabled':
                    print(f"🚫 [{elapsed:4.1f}s] Fallback Keras désactivé")
                    break
                else:
                    print(f"❓ [{elapsed:4.1f}s] Statut inconnu: {status}")
            
        except requests.exceptions.RequestException:
            if attempt == 0:
                print("⏳ En attente du démarrage de l'application...")
        
        time.sleep(1)
    
    print("-" * 50)

def start_web_app_async(host: str = 'localhost', port: int = 5000, debug: bool = False, monitor: bool = True):
    """
    Démarre l'application web avec chargement asynchrone
    """
    tf_available, tf_version = check_async_compatibility()
    
    print("=" * 70)
    print("🚀 MILA ASSIST - DÉMARRAGE ASYNCHRONE")
    print("=" * 70)
    print("⚡ Interface utilisable IMMÉDIATEMENT")
    print("🧠 Modèle Keras se charge en arrière-plan")
    print("🔄 Basculement transparent vers fallback local")
    print("=" * 70)
    
    if tf_available:
        print(f"✅ TensorFlow {tf_version} détecté - Fallback Keras disponible")
    else:
        print("⚠️ TensorFlow non disponible - API uniquement")
    
    print(f"🌐 Démarrage sur http://{host}:{port}")
    print("=" * 70)
    
    logger.info(f"Démarrage asynchrone de l'application web sur {host}:{port} (debug={debug})...")
    
    try:
        # Import et démarrage de l'application
        from app import create_app
        
        app_instance = create_app()
        
        # Démarrer le monitoring en arrière-plan si demandé
        if monitor and tf_available:
            monitor_thread = threading.Thread(
                target=monitor_model_loading,
                args=(host, port),
                daemon=True
            )
            monitor_thread.start()
        
        print("🎯 Application prête ! Ouvrez votre navigateur sur l'URL ci-dessus")
        print("💡 Le modèle Keras se charge silencieusement en arrière-plan")
        print()
        
        # Lancement de l'application
        app_instance.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        logger.error(f"Erreur lors du démarrage asynchrone: {e}")
        sys.exit(1)

def test_async_functionality():
    """Test rapide du fonctionnement asynchrone"""
    print("🧪 TEST DU FONCTIONNEMENT ASYNCHRONE")
    print("=" * 50)
    
    try:
        # Test des imports
        from app import create_app
        from services.chatbot_service import ChatbotService, ModelStatus
        from config.app_config import AppConfig
        
        print("✅ Imports OK")
        
        # Test de création d'app
        os.environ.update({
            'API_URL': 'http://localhost:99999/api',  # API invalide pour test
            'API_KEY': 'test_key_1234567890',
            'USE_LEGACY_FALLBACK': 'true'
        })
        
        start_time = time.time()
        config = AppConfig()
        service = ChatbotService(config)
        creation_time = time.time() - start_time
        
        print(f"✅ Service créé en {creation_time*1000:.1f}ms")
        print(f"🔄 Statut initial: {service.model_status.value}")
        
        # Test de réponse pendant chargement
        if service.model_status == ModelStatus.LOADING:
            start_response = time.time()
            reponse = service.obtenir_reponse("test", "test_session")
            response_time = time.time() - start_response
            
            print(f"✅ Réponse obtenue en {response_time*1000:.1f}ms pendant chargement")
            print(f"💬 Réponse: {reponse[:60]}{'...' if len(reponse) > 60 else ''}")
        
        print("🎉 Test asynchrone réussi !")
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        return False
    
    return True

def run_full_async_tests():
    """Exécuter la suite complète de tests asynchrones"""
    print("🔬 SUITE COMPLÈTE DE TESTS ASYNCHRONES")
    print("=" * 60)
    
    try:
        # Import et exécution des tests
        from tests.test_async_loading import run_async_tests
        return run_async_tests()
    except ImportError:
        print("❌ Module de tests asynchrones non trouvé")
        print("💡 Créez tests/test_async_loading.py pour les tests complets")
        return False

def install_dependencies(minimal: bool = False):
    """
    Installe les dépendances (mode minimal si nécessaire)
    """
    logger.info("Installation des dépendances (%s)...", "minimal" if minimal else "complet")
    
    print("📦 INSTALLATION DES DÉPENDANCES")
    print("=" * 40)
    
    try:
        req_file = "requirements-min.txt" if minimal else "requirements_full.txt"
        
        if not os.path.exists(req_file):
            req_file = "requirements.txt"  # Fallback
        
        print(f"📋 Utilisation de {req_file}")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", req_file],
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode == 0:
            print("✅ Installation réussie")
            
            # Test post-installation
            try:
                import tensorflow
                print(f"✅ TensorFlow {tensorflow.__version__} installé")
            except ImportError:
                print("⚠️ TensorFlow non installé - fallback Keras indisponible")
            
            return True
        else:
            print("❌ Erreur durant l'installation")
            return False
            
    except Exception as e:
        logger.error(f"Erreur lors de l'installation: {e}")
        return False

def show_async_info():
    """Afficher les informations sur le mode asynchrone"""
    print("ℹ️  INFORMATIONS SUR LE MODE ASYNCHRONE")
    print("=" * 50)
    print("🎯 AVANTAGES:")
    print("  ⚡ Démarrage instantané (< 1 seconde)")
    print("  🔄 Pas d'attente pour l'utilisateur")
    print("  🧠 Chargement silencieux du modèle")
    print("  🔄 Basculement transparent API ↔ Local")
    print("  💡 Interface toujours réactive")
    print()
    print("🔧 FONCTIONNEMENT:")
    print("  1. L'application démarre immédiatement")
    print("  2. L'utilisateur peut utiliser le chatbot")
    print("  3. Le modèle Keras se charge en arrière-plan")
    print("  4. Basculement automatique quand prêt")
    print("  5. Fallback robuste en cas de coupure")
    print()
    print("📊 MONITORING:")
    print("  • /model_status : Statut du chargement")
    print("  • /stats : Statistiques complètes")
    print("  • Interface : Indicateur discret")
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description="Mila Assist - Assistant virtuel avec chargement asynchrone")
    parser.add_argument("mode", choices=["web", "full", "install", "test-async", "info"], 
                       help="Mode de démarrage")
    parser.add_argument("--host", default="localhost", help="Adresse d'écoute")
    parser.add_argument("--port", type=int, default=5000, help="Port d'écoute")
    parser.add_argument("--debug", action="store_true", help="Mode debug")
    parser.add_argument("--no-monitor", action="store_true", help="Désactiver le monitoring du chargement")
    
    # Paramètres de configuration dynamiques
    parser.add_argument("--api-url", dest="api_url", help="URL de l'API")
    parser.add_argument("--api-key", dest="api_key", help="Clé API")
    parser.add_argument("--use-api", dest="use_api", action="store_true", help="Forcer l'utilisation de l'API")
    parser.add_argument("--no-api", dest="no_api", action="store_true", help="Désactiver l'API")
    parser.add_argument("--offline", dest="offline", action="store_true", help="Mode hors-ligne complet")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Mila Assist - Mode: {args.mode} (Asynchrone)")

    # Appliquer les overrides de configuration
    if args.offline:
        os.environ["USE_API"] = "false"
        os.environ["USE_DB"] = "false"
        logger.info("Mode hors-ligne activé: USE_API=false, USE_DB=false")
    else:
        if args.use_api:
            os.environ["USE_API"] = "true"
        if args.no_api:
            os.environ["USE_API"] = "false"

    if args.api_url:
        os.environ["API_URL"] = args.api_url
        logger.info(f"API_URL override: {args.api_url}")
    if args.api_key:
        os.environ["API_KEY"] = args.api_key
    
    try:
        if args.mode == "install":
            # Installation avec détection automatique
            minimal = os.getenv("MIN_REQ", "0") in {"1", "true", "yes", "on"}
            success = install_dependencies(minimal=minimal)
            if success:
                logger.info("✅ Installation terminée - Prêt pour le mode asynchrone")
            else:
                logger.error("❌ Erreur lors de l'installation")
            return
        
        elif args.mode == "info":
            show_async_info()
            return
        
        elif args.mode == "test-async":
            print("🧪 Test rapide du fonctionnement asynchrone...")
            if test_async_functionality():
                print("\n🎉 Tests de base réussis")
                
                # Proposer les tests complets
                response = input("\n❓ Exécuter la suite complète de tests ? (y/N): ")
                if response.lower() in ['y', 'yes', 'oui']:
                    run_full_async_tests()
            return
        
        elif args.mode in ["web", "full"]:
            # Les deux modes utilisent maintenant la même architecture asynchrone
            start_web_app_async(
                host=args.host, 
                port=args.port, 
                debug=args.debug,
                monitor=not args.no_monitor
            )
        
        else:
            logger.error(f"Mode non reconnu: {args.mode}")
            return
        
    except KeyboardInterrupt:
        logger.info("Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()