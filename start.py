#!/usr/bin/env python3
"""
Script de démarrage pour Mila Assist v2.0
Assistant virtuel pour streameur - Permet de lancer différents modes de fonctionnement
"""

import os
import sys
import argparse
import subprocess
import threading
import time
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_api_server():
    """Démarre le serveur API"""
    logger.info("Démarrage du serveur API...")
    try:
        from api import ChatbotAPI
        api = ChatbotAPI()
        api.run(host='localhost', port=5001, debug=False)
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'API: {e}")

def start_web_app():
    """Démarre l'application web"""
    logger.info("Démarrage de l'application web...")
    try:
        import app_v2
        app_v2.app.run(host='localhost', port=5000, debug=False)
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'app web: {e}")

def start_legacy_app():
    """Démarre l'application legacy (désactivé - fichier archivé)"""
    logger.warning("Mode legacy désactivé : app.py a été archivé")
    logger.info("Utilisez le mode 'web' pour lancer app_v2.py")

def start_full_system():
    """Démarre le système complet (API + Web)"""
    logger.info("Démarrage du système complet...")
    
    # Démarrage de l'API en arrière-plan
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()
    
    # Attendre que l'API démarre
    time.sleep(3)
    
    # Démarrage de l'application web
    start_web_app()

def run_tests():
    """Exécute les tests de migration (désactivé - fichier archivé)"""
    logger.warning("Mode test désactivé : migrate_and_test.py a été archivé")
    logger.info("Les fichiers de migration ont été déplacés vers a_supprimer/")
    return False

def install_dependencies():
    """Installe les dépendances"""
    logger.info("Installation des dépendances...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                              cwd=os.path.dirname(__file__))
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Erreur lors de l'installation: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Mila Assist - Assistant virtuel pour streameur")
    parser.add_argument("mode", choices=["api", "web", "full", "install"], 
                       help="Mode de démarrage")
    parser.add_argument("--host", default="localhost", help="Adresse d'écoute")
    parser.add_argument("--port", type=int, default=5000, help="Port d'écoute")
    parser.add_argument("--debug", action="store_true", help="Mode debug")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Mila Assist - Mode: {args.mode}")
    
    try:
        if args.mode == "install":
            success = install_dependencies()
            if success:
                logger.info("✅ Installation terminée avec succès")
            else:
                logger.error("❌ Erreur lors de l'installation")
            return
        
        elif args.mode == "api":
            start_api_server()
        
        elif args.mode == "web":
            start_web_app()
        
        elif args.mode == "full":
            start_full_system()
        
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
