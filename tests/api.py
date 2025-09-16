#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API.PY SIMPLIFIÉ - COMPATIBILITÉ AVEC CHARGEMENT ASYNCHRONE
==========================================================

Version simplifiée d'api.py qui utilise la logique principale de app.py
Maintient la compatibilité avec les anciens scripts de lancement

Améliorations VERSION ASYNCHRONE:
- Utilise la classe MilaAssistApp de app.py
- Chargement asynchrone du modèle Keras
- Interface utilisable immédiatement
- Pas de duplication de code

Auteur: Concepteur Développeur d'Applications RNCP 6  
Date: 2025-01-15
"""

import os
import sys
import logging
from datetime import datetime

# Import de la classe principale depuis app.py
try:
    from app import MilaAssistApp, create_app
except ImportError as e:
    print(f"❌ Erreur d'import depuis app.py: {e}")
    print("💡 Assurez-vous que app.py est présent dans le même répertoire")
    sys.exit(1)

logger = logging.getLogger(__name__)

def create_app_legacy():
    """Factory legacy pour compatibilité - utilise la nouvelle architecture asynchrone"""
    try:
        logger.info("🔄 Utilisation de l'architecture asynchrone via app.py")
        return create_app()
    except Exception as e:
        logger.error(f"❌ Erreur création app legacy: {e}")
        raise

def main():
    """Point d'entrée principal pour api.py - Version asynchrone"""
    print("🚀 MILA ASSIST API - Redirection vers architecture asynchrone")
    print("⚡ Chargement instantané avec modèle Keras en arrière-plan")
    print("-" * 60)
    
    try:
        # Créer l'application avec la nouvelle architecture
        app_instance = create_app_legacy()
        
        # Configuration depuis les variables d'environnement
        HOST = os.getenv('HOST', 'localhost')
        PORT = int(os.getenv('PORT', 5000))
        DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
        
        logger.info("🔗 Lancement via api.py avec architecture asynchrone")
        app_instance.run(host=HOST, port=PORT, debug=DEBUG)
        
    except KeyboardInterrupt:
        logger.info("Application interrompue par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()