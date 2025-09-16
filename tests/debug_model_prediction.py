#!/usr/bin/env python3
"""
Debug du modèle Keras pour comprendre les mauvaises prédictions
"""

import os
import sys
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer
import re

# Configuration
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

# Charger les artefacts
def charger_modele_et_artefacts():
    model_path = os.path.join(base_dir, "chatbot_model.keras")
    words_path = os.path.join(base_dir, "words.pkl")
    classes_path = os.path.join(base_dir, "classes.pkl")
    patterns_path = os.path.join(base_dir, "training_patterns.pkl")
    
    model = load_model(model_path)
    
    with open(words_path, 'rb') as f:
        words = pickle.load(f)
    
    with open(classes_path, 'rb') as f:
        classes = pickle.load(f)
    
    with open(patterns_path, 'rb') as f:
        patterns = pickle.load(f)
    
    return model, words, classes, patterns

def nettoyer_phrase(phrase):
    """Nettoyer et tokeniser une phrase"""
    lemmatizer = WordNetLemmatizer()
    
    # Normalisation de base
    phrase = phrase.lower().strip()
    
    # Suppression de la ponctuation et caractères spéciaux
    phrase = re.sub(r'[^\w\s\']', ' ', phrase)
    
    # Tokenisation
    mots = nltk.word_tokenize(phrase, language='french')
    
    # Lemmatisation et filtrage
    mots_nettoyes = []
    for mot in mots:
        if len(mot) > 1:  # Éviter les mots trop courts
            mot_lemma = lemmatizer.lemmatize(mot.lower())
            mots_nettoyes.append(mot_lemma)
    
    return mots_nettoyes

def creer_bag_of_words(mots_phrase, words):
    """Créer un bag of words"""
    bag = np.zeros(len(words), dtype=np.float32)
    
    for mot in mots_phrase:
        for i, word in enumerate(words):
            if word == mot:
                bag[i] = 1.0
                break
    
    return bag

def predire_avec_details(model, words, classes, phrase):
    """Prédire avec des détails sur les scores"""
    print(f"\n🔍 Analyse de: '{phrase}'")
    print("-" * 60)
    
    # Nettoyer la phrase
    mots_phrase = nettoyer_phrase(phrase)
    print(f"Mots extraits: {mots_phrase}")
    
    # Créer le bag of words
    bag = creer_bag_of_words(mots_phrase, words)
    mots_trouves = [words[i] for i in range(len(words)) if bag[i] == 1]
    print(f"Mots trouvés dans le vocabulaire: {mots_trouves}")
    
    # Prédiction
    res = model.predict(np.array([bag]), verbose=0)[0]
    
    # Trier les résultats par score
    resultats = [(i, score, classes[i]) for i, score in enumerate(res)]
    resultats = sorted(resultats, key=lambda x: x[1], reverse=True)
    
    print(f"\nTop 10 des prédictions:")
    for i, (idx, score, classe) in enumerate(resultats[:10]):
        print(f"{i+1:2d}. {classe:15s} - Score: {score:.4f}")
    
    print(f"\nClasse prédite: {resultats[0][2]} (score: {resultats[0][1]:.4f})")
    
    return resultats[0][2], resultats[0][1]

def main():
    print("🔍 DEBUG DU MODÈLE KERAS")
    print("=" * 60)
    
    # Charger le modèle
    model, words, classes, patterns = charger_modele_et_artefacts()
    
    print(f"Modèle chargé: {len(words)} mots, {len(classes)} classes")
    
    # Questions de test problématiques
    questions_test = [
        "Est ce qu'on peut utiliser alicia en meme temps sur plusieurs pc",
        "Comment configurer TTS sur OBS ?",
        "Qu'est-ce que ai_licia ?",
        "Comment faire un test",
        "Bonjour comment ça va",
        "Merci pour ton aide"
    ]
    
    for question in questions_test:
        classe_predite, score = predire_avec_details(model, words, classes, question)
        
        # Vérifier si on a des patterns pour cette classe
        if classe_predite in patterns:
            reponses_possibles = patterns[classe_predite]["responses"]
            print(f"Réponses possibles: {reponses_possibles[:2]}")
        else:
            print("❌ Aucune réponse trouvée dans les patterns")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    main()
