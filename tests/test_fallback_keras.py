#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du fallback Keras - Vérifie que l'application bascule correctement
sur le modèle local quand l'API n'est pas disponible
"""

import os
import sys
import time
import requests
import subprocess

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.app_config import AppConfig
from services.chatbot_service import ChatbotService

def test_api_indisponible():
    """Test avec API indisponible - force le fallback Keras"""
    print("🧪 Test du fallback Keras avec API indisponible")
    
    # Configurer pour utiliser une URL d'API invalide
    os.environ['API_URL'] = 'http://localhost:99999/api'  # Port inexistant
    os.environ['USE_LEGACY_FALLBACK'] = 'true'
    
    try:
        # Initialiser la configuration et le service
        config = AppConfig()
        chatbot_service = ChatbotService(config)
        
        print(f"✅ Service initialisé")
        print(f"🧠 Modèle Keras chargé: {chatbot_service.model is not None}")
        print(f"📝 Words chargé: {chatbot_service.words is not None}")
        print(f"🏷️ Classes chargées: {chatbot_service.classes is not None}")
        
        if chatbot_service.model is None:
            print("❌ Modèle Keras non chargé - test impossible")
            return False
        
        # Test de plusieurs messages
        messages_test = [
            "Bonjour",
            "Comment allez-vous ?",
            "Qui êtes-vous ?",
            "Merci",
            "Au revoir"
        ]
        
        print("\n🧪 Tests de messages avec fallback Keras:")
        session_id = "test_fallback_session"
        
        for message in messages_test:
            print(f"\n📨 Message: '{message}'")
            start_time = time.time()
            
            reponse = chatbot_service.obtenir_reponse(message, session_id)
            
            response_time = (time.time() - start_time) * 1000
            print(f"💬 Réponse: '{reponse}'")
            print(f"⏱️ Temps: {response_time:.2f}ms")
        
        # Afficher les statistiques
        stats = chatbot_service.obtenir_statistiques()
        print(f"\n📊 Statistiques finales:")
        print(f"  - Messages traités: {stats['messages_traites']}")
        print(f"  - Succès API: {stats['api_success']}")
        print(f"  - Échecs API: {stats['api_failures']}")
        print(f"  - Fallback Keras utilisé: {stats['keras_fallback_used']}")
        print(f"  - Modèle local chargé: {stats['modele_local_charge']}")
        print(f"  - Fallback actif: {stats['fallback_keras_actif']}")
        
        # Vérifier que le fallback Keras a été utilisé
        if stats['keras_fallback_used'] > 0:
            print("✅ Test réussi - Le fallback Keras fonctionne !")
            return True
        else:
            print("❌ Test échoué - Le fallback Keras n'a pas été utilisé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur pendant le test: {e}")
        return False

def test_api_disponible():
    """Test avec API disponible - doit utiliser l'API"""
    print("\n🧪 Test avec API disponible")
    
    # Restaurer l'URL d'API normale
    os.environ['API_URL'] = 'https://ezi0.synology.me:10443/api'
    
    try:
        config = AppConfig()
        chatbot_service = ChatbotService(config)
        
        # Test rapide de connexion API
        api_connectee = chatbot_service.test_api_connection()
        print(f"🌐 API connectée: {api_connectee}")
        
        if api_connectee:
            # Test d'un message
            reponse = chatbot_service.obtenir_reponse("Bonjour", "test_api_session")
            print(f"💬 Réponse API: '{reponse}'")
            
            stats = chatbot_service.obtenir_statistiques()
            print(f"📊 Succès API: {stats['api_success']}")
            print(f"📊 Fallback Keras: {stats['keras_fallback_used']}")
            
            if stats['api_success'] > 0:
                print("✅ API fonctionne correctement")
                return True
        else:
            print("⚠️ API non disponible - normal si pas sur le réseau local")
            return True  # Pas d'erreur si API pas dispo
            
    except Exception as e:
        print(f"❌ Erreur test API: {e}")
        return False

def main():
    """Test principal"""
    print("🚀 Test du système de fallback Keras")
    print("=" * 50)
    
    # Test 1: Fallback Keras avec API indisponible
    test1_ok = test_api_indisponible()
    
    # Test 2: API disponible (si possible)
    test2_ok = test_api_disponible()
    
    print("\n" + "=" * 50)
    print("📊 Résultats des tests:")
    print(f"  - Fallback Keras: {'✅ OK' if test1_ok else '❌ ÉCHEC'}")
    print(f"  - API disponible: {'✅ OK' if test2_ok else '❌ ÉCHEC'}")
    
    if test1_ok:
        print("\n🎉 Le fallback Keras fonctionne correctement !")
        print("💡 L'application basculera automatiquement sur le modèle local")
        print("   si l'API NAS n'est pas accessible.")
    else:
        print("\n⚠️ Le fallback Keras ne fonctionne pas comme attendu.")
    
    return test1_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
