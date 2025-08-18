#!/usr/bin/env python3
"""
Test approfondi du système de réponses naturelles
"""

from response_modes import create_response_system, ResponseMode

def test_response_comparison():
    """Compare les réponses entre les différents modes"""
    
    test_cases = [
        {
            "question": "Bonjour, comment allez-vous ?",
            "response": "Je vais très bien, merci de votre question !"
        },
        {
            "question": "Pourquoi le code ne fonctionne pas ?",
            "response": "Il faut vérifier la syntaxe et les indentations."
        },
        {
            "question": "Merci pour votre aide !",
            "response": "De rien, c'était avec plaisir."
        },
        {
            "question": "Peux-tu m'expliquer comment faire une boucle en Python ?",
            "response": "Utilisez 'for' pour itérer sur une séquence ou 'while' pour une condition."
        },
        {
            "question": "J'ai un problème avec mon serveur",
            "response": "Vérifiez les logs et la configuration réseau."
        }
    ]
    
    modes = [ResponseMode.MINIMAL, ResponseMode.BALANCED, ResponseMode.NATURAL]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {test_case['question']}")
        print(f"Réponse de base: {test_case['response']}")
        print('='*60)
        
        for mode in modes:
            print(f"\n--- MODE {mode.upper()} ---")
            system = create_response_system(mode)
            result = system.get_enhanced_response(
                test_case['response'], 
                test_case['question'], 
                0.85
            )
            print(f"✨ {result['response']}")
            print(f"   [Type: {result['question_type']}, Enhanced: {result['enhancement_applied']}]")

def test_conversation_context():
    """Test la continuité conversationnelle"""
    print(f"\n{'='*60}")
    print("TEST DE CONTINUITÉ CONVERSATIONNELLE")
    print('='*60)
    
    system = create_response_system(ResponseMode.NATURAL)
    
    conversation = [
        ("Qu'est-ce que Python ?", "Python est un langage de programmation"),
        ("Comment installer Python ?", "Téléchargez-le depuis python.org"),
        ("Et les bibliothèques Python ?", "Utilisez pip pour installer des packages"),
        ("Que faire en cas d'erreur ?", "Lisez le message d'erreur et vérifiez votre code")
    ]
    
    for question, response in conversation:
        result = system.get_enhanced_response(response, question, 0.9)
        print(f"\n🤔 {question}")
        print(f"🤖 {result['response']}")

if __name__ == "__main__":
    print("🚀 Test du système de réponses naturelles amélioré")
    test_response_comparison()
    test_conversation_context()
    print(f"\n{'='*60}")
    print("✅ Tests terminés !")
