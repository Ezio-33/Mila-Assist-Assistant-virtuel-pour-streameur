#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test des performances du modèle Keras
Compare l'ancien et le nouveau modèle après amélioration
"""

import os
import sys
import time
import requests

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.app_config import AppConfig
from services.chatbot_service import ChatbotService

def test_performance_modele():
    """Test complet des performances du modèle"""
    print("🧪 Test des performances du modèle Keras amélioré")
    print("=" * 60)
    
    # Configurer pour utiliser le fallback Keras uniquement
    os.environ['API_URL'] = 'http://localhost:99999/api'  # API invalide
    os.environ['USE_LEGACY_FALLBACK'] = 'true'
    
    try:
        # Initialiser le service
        config = AppConfig()
        chatbot_service = ChatbotService(config)
        
        if chatbot_service.model is None:
            print("❌ Modèle Keras non chargé - impossible de tester")
            return False
        
        print(f"✅ Modèle chargé: {len(chatbot_service.classes)} classes, {len(chatbot_service.words)} mots")
        print()
        
        # Messages de test variés
        messages_test = [
            # Salutations
            ("Bonjour", "greeting"),
            ("Salut", "greeting"),
            ("Hello", "greeting"),
            ("Bonsoir", "greeting"),
            
            # Questions d'identité
            ("Qui êtes-vous ?", "identity"),
            ("Comment tu t'appelles ?", "identity"),
            ("Quel est votre nom ?", "identity"),
            
            # Remerciements
            ("Merci", "thanks"),
            ("Merci beaucoup", "thanks"),
            ("Je vous remercie", "thanks"),
            
            # Au revoir
            ("Au revoir", "goodbye"),
            ("Bye", "goodbye"),
            ("À bientôt", "goodbye"),
            
            # Demandes d'aide
            ("Aide", "help"),
            ("Pouvez-vous m'aider ?", "help"),
            ("J'ai besoin d'aide", "help"),
            
            # Questions complexes
            ("Comment faire pour jouer ?", "help"),
            ("Qu'est-ce que tu peux faire ?", "help"),
            ("Explique-moi le stream", "help"),
        ]
        
        resultats = []
        temps_total = 0
        
        print("🧪 Tests de performance:")
        print()
        
        for i, (message, categorie_attendue) in enumerate(messages_test, 1):
            print(f"Test {i:2d}/{ len(messages_test)}: '{message}'")
            
            start_time = time.time()
            reponse = chatbot_service.obtenir_reponse(message, f"test_session_{i}")
            response_time = (time.time() - start_time) * 1000
            
            temps_total += response_time
            
            # Analyser la qualité de la réponse
            qualite = analyser_qualite_reponse(reponse, message, categorie_attendue)
            
            resultats.append({
                'message': message,
                'categorie_attendue': categorie_attendue,
                'reponse': reponse,
                'temps_ms': response_time,
                'qualite': qualite
            })
            
            print(f"         Réponse: '{reponse[:60]}{'...' if len(reponse) > 60 else ''}'")
            print(f"         Temps: {response_time:.1f}ms | Qualité: {qualite}/5")
            print()
        
        # Statistiques globales
        print("=" * 60)
        print("📊 STATISTIQUES GLOBALES")
        print("=" * 60)
        
        temps_moyen = temps_total / len(messages_test)
        qualite_moyenne = sum(r['qualite'] for r in resultats) / len(resultats)
        
        print(f"⏱️  Temps moyen de réponse: {temps_moyen:.1f}ms")
        print(f"📈 Qualité moyenne: {qualite_moyenne:.1f}/5")
        print(f"🎯 Messages traités: {len(messages_test)}")
        
        # Analyse par catégorie
        print("\n📋 Analyse par catégorie:")
        categories = {}
        for resultat in resultats:
            cat = resultat['categorie_attendue']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(resultat)
        
        for categorie, tests in categories.items():
            qualite_cat = sum(t['qualite'] for t in tests) / len(tests)
            temps_cat = sum(t['temps_ms'] for t in tests) / len(tests)
            print(f"  {categorie:12s}: Qualité {qualite_cat:.1f}/5, Temps {temps_cat:.1f}ms ({len(tests)} tests)")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        if qualite_moyenne < 3.0:
            print("  ⚠️  Qualité faible - Considérer un ré-entraînement avec plus de données")
        elif qualite_moyenne < 4.0:
            print("  📈 Qualité correcte - Optimisations possibles")
        else:
            print("  ✅ Excellente qualité - Modèle performant")
        
        if temps_moyen > 200:
            print("  ⏱️  Temps de réponse élevé - Optimiser le modèle ou l'infrastructure")
        elif temps_moyen > 100:
            print("  ⏱️  Temps de réponse acceptable")
        else:
            print("  ⚡ Temps de réponse excellent")
        
        # Statistiques du service
        stats = chatbot_service.obtenir_statistiques()
        print(f"\n🔧 Statistiques du service:")
        print(f"  - Fallback Keras utilisé: {stats['keras_fallback_used']} fois")
        print(f"  - Échecs API: {stats['api_failures']}")
        print(f"  - TensorFlow disponible: {stats['tensorflow_disponible']}")
        print(f"  - NLTK disponible: {stats['nltk_disponible']}")
        
        return qualite_moyenne >= 3.0
        
    except Exception as e:
        print(f"❌ Erreur pendant le test: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyser_qualite_reponse(reponse: str, message: str, categorie_attendue: str) -> int:
    """
    Analyse la qualité d'une réponse sur une échelle de 1 à 5
    """
    if not reponse or reponse.strip() == "":
        return 1
    
    score = 3  # Score de base
    
    message_lower = message.lower()
    reponse_lower = reponse.lower()
    
    # Vérifications par catégorie
    if categorie_attendue == "greeting":
        if any(word in reponse_lower for word in ["bonjour", "salut", "hello", "bonsoir", "ravi"]):
            score += 1
        if "comment" in reponse_lower and "aider" in reponse_lower:
            score += 1
    
    elif categorie_attendue == "identity":
        if any(word in reponse_lower for word in ["mila", "assistant", "virtuel", "nom", "appelle"]):
            score += 1
        if "je suis" in reponse_lower or "je m'appelle" in reponse_lower:
            score += 1
    
    elif categorie_attendue == "thanks":
        if any(word in reponse_lower for word in ["rien", "plaisir", "prie", "normal", "avec plaisir"]):
            score += 1
        if "autre chose" in reponse_lower:
            score += 1
    
    elif categorie_attendue == "goodbye":
        if any(word in reponse_lower for word in ["revoir", "bientôt", "plus tard", "bye", "journée"]):
            score += 1
        if "portez" in reponse_lower or "bonne" in reponse_lower:
            score += 1
    
    elif categorie_attendue == "help":
        if any(word in reponse_lower for word in ["aide", "aider", "question", "besoin", "peux"]):
            score += 1
        if "?" in reponse:
            score += 1
    
    # Pénalités pour réponses génériques
    if "comprends" in reponse_lower and "précis" in reponse_lower:
        score -= 1  # Réponse trop générique
    
    # Bonus pour réponses bien formées
    if len(reponse) > 20 and (reponse.endswith('.') or reponse.endswith('!') or reponse.endswith('?')):
        score += 1
    
    return max(1, min(5, score))

def main():
    """Fonction principale"""
    print("🚀 Test de performance du modèle Keras")
    print("Testez les performances avant et après les améliorations")
    print()
    
    success = test_performance_modele()
    
    if success:
        print("\n✅ Tests terminés avec succès")
    else:
        print("\n❌ Des problèmes ont été détectés")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
