# Version hybride d'app.py intégrant la base de données vectorielle
# Compatible avec l'ancien système comme fallback

import os
import random
import numpy as np
import pickle
import json
import nltk
import requests
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from datetime import datetime
from threading import Thread
import subprocess
import logging
from database import ChatbotDatabase, init_database

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation du lemmatiseur pour le traitement du langage naturel
lemmatizer = WordNetLemmatizer()
nltk.download('punkt', quiet=True)

# Définition du répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration pour l'API (si utilisée en mode API)
API_MODE = os.getenv('USE_API', 'False').lower() == 'true'
API_URL = os.getenv('API_URL', 'http://localhost:5001/api')
API_KEY = os.getenv('API_KEY', 'dev_key_123456789')

# Configuration du mode de réponse
RESPONSE_MODE = os.getenv('RESPONSE_MODE', 'balanced')  # minimal/balanced/natural

# Chargement des ressources (fallback)
model = None
intents = None
words = None
classes = None
db = None

def init_resources():
    """Initialise les ressources (base de données et/ou modèle legacy)"""
    global model, intents, words, classes, db
    
    try:
        # Initialisation de la base de données
        if not API_MODE:
            db = init_database(migrate_intents=True)
            logger.info("Base de données initialisée")
        
        # Chargement des ressources legacy (fallback)
        model_path = os.path.join(BASE_DIR, "chatbot_model.keras")
        if os.path.exists(model_path):
            model = load_model(model_path)
            logger.info("Modèle Keras chargé")
        
        intents_path = os.path.join(BASE_DIR, "intents.json")
        if os.path.exists(intents_path):
            with open(intents_path) as file:
                intents = json.load(file)
            logger.info("Intents chargés")
        
        words_path = os.path.join(BASE_DIR, "words.pkl")
        if os.path.exists(words_path):
            words = pickle.load(open(words_path, "rb"))
        
        classes_path = os.path.join(BASE_DIR, "classes.pkl")
        if os.path.exists(classes_path):
            classes = pickle.load(open(classes_path, "rb"))
            
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation des ressources: {e}")

# Initialisation des ressources au démarrage
init_resources()

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# Mémoire de la conversation pour stocker l'historique des échanges
conversation_memory = []

# Route pour la page d'accueil
@app.route("/")
def home():
    return render_template("index.html")

# Route pour changer le mode de réponse
@app.route("/set_mode", methods=["POST"])
def set_response_mode():
    """Change le mode de réponse dynamiquement"""
    try:
        global RESPONSE_MODE
        new_mode = request.form.get("mode", "balanced")
        
        if new_mode in ["minimal", "balanced", "natural"]:
            RESPONSE_MODE = new_mode
            logger.info(f"Mode de réponse changé vers: {new_mode}")
            
            # Informations sur le mode sélectionné
            mode_info = {
                "minimal": "Mode minimal activé : Réponses directes et rapides",
                "balanced": "Mode équilibré activé : Réponses reformulées avec templates",
                "natural": "Mode naturel activé : Réponses contextuelles et conversationnelles"
            }
            
            return {"status": "success", "mode": new_mode, "message": mode_info[new_mode]}
        else:
            return {"status": "error", "message": "Mode invalide. Utilisez : minimal, balanced, ou natural"}
            
    except Exception as e:
        logger.error(f"Erreur lors du changement de mode: {e}")
        return {"status": "error", "message": "Erreur lors du changement de mode"}

# Route pour obtenir des informations sur les modes
@app.route("/modes_info", methods=["GET"])
def get_modes_info():
    """Retourne des informations sur les modes disponibles"""
    return {
        "current_mode": RESPONSE_MODE,
        "available_modes": {
            "minimal": {
                "name": "Minimal (Faibles ressources)",
                "description": "Réponses directes de la base, très rapide, faible utilisation mémoire",
                "pros": ["Très rapide", "Faible consommation RAM", "Stable"],
                "cons": ["Réponses robotiques", "Pas de contextualisation"]
            },
            "balanced": {
                "name": "Équilibré (Recommandé)", 
                "description": "Reformulation avec templates, bon compromis performance/qualité",
                "pros": ["Réponses plus naturelles", "Performance correcte", "Variété dans les réponses"],
                "cons": ["Légèrement plus lent", "Consommation mémoire modérée"]
            },
            "natural": {
                "name": "Naturel (Haute qualité)",
                "description": "Utilise sentence-transformers pour des réponses contextuelles",
                "pros": ["Réponses très naturelles", "Contextualisation avancée", "Mémoire conversationnelle"],
                "cons": ["Plus lent au démarrage", "Consommation mémoire élevée", "Nécessite sentence-transformers"]
            }
        }
    }

# Route pour obtenir la réponse du chatbot
@app.route("/get", methods=["POST"])
def chatbot_response():
    try:
        msg = request.form["msg"]
        session_id = request.form.get("session_id", "web_session")
        
        sentences = sent_tokenize(msg)
        responses = []

        for sentence in sentences:
            # Gestion spéciale pour les présentations
            if sentence.lower().startswith(("je m'appelle", "bonjour, je m'appelle")):
                name = sentence.split("appelle", 1)[1].strip()
                response = get_personalized_response(sentence, name)
            else:
                response = get_smart_response(sentence, session_id)

            responses.append(response)

        # Ajout de l'échange à la mémoire de conversation
        final_response = " ".join(responses)
        conversation_memory.append({"user": msg, "bot": final_response, "timestamp": datetime.now()})
        
        return final_response
        
    except Exception as e:
        logger.error(f"Erreur dans chatbot_response: {e}")
        return "Désolé, une erreur s'est produite. Pouvez-vous réessayer ?"

def get_smart_response(sentence, session_id="default"):
    """Obtient une réponse intelligente en utilisant la base de données vectorielle d'abord"""
    try:
        # Méthode 1: API externe (si configurée)
        if API_MODE:
            response = get_response_from_api(sentence, session_id)
            if response:
                return generate_contextual_response(response, sentence)
        
        # Méthode 2: Base de données locale
        if db:
            best_match = db.get_best_response(sentence, threshold=0.7, mode=RESPONSE_MODE)
            if best_match:
                logger.info(f"Réponse trouvée en DB (similarité: {best_match['similarity']:.2f})")
                return best_match['response']  # Réponse déjà améliorée par le système de modes
        
        # Méthode 3: Système legacy (fallback)
        if model and words and classes:
            ints = predict_class(sentence)
            if ints:
                legacy_response = get_response(ints)
                logger.info("Réponse du système legacy")
                return generate_contextual_response(legacy_response, sentence)
        
        # Réponse par défaut
        return generate_contextual_response("Désolé, je ne vous ai pas compris.", sentence)
        
    except Exception as e:
        logger.error(f"Erreur dans get_smart_response: {e}")
        return "Désolé, une erreur s'est produite."

def get_response_from_api(message, session_id):
    """Obtient une réponse via l'API externe"""
    try:
        headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
        data = {
            'message': message,
            'session_id': session_id,
            'threshold': 0.7
        }
        
        response = requests.post(f"{API_URL}/chat", json=data, headers=headers, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result.get('response')
        
        logger.warning(f"API response error: {response.status_code}")
        return None
        
    except Exception as e:
        logger.error(f"Erreur API: {e}")
        return None

def get_personalized_response(sentence, name):
    """Gère les réponses personnalisées avec nom"""
    try:
        # Recherche avec la base de données
        if db:
            best_match = db.get_best_response(sentence, threshold=0.6)
            if best_match:
                response = best_match['response'].replace("{n}", name)
                return generate_contextual_response(response, sentence)
        
        # Fallback vers système legacy
        if model and words and classes:
            ints = predict_class(sentence)
            response = get_response(ints, name)
            return generate_contextual_response(response, sentence)
        
        return f"Bonjour {name}, ravi de vous rencontrer !"
        
    except Exception as e:
        logger.error(f"Erreur dans get_personalized_response: {e}")
        return f"Bonjour {name} !"

# Route pour gérer les retours utilisateurs
@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        question = request.form["question"]
        expected_response = request.form["expected"]
        current_response = request.form.get("current_response", "")
        
        # Sauvegarde dans la base de données
        if db:
            success = db.save_feedback(question, expected_response, current_response)
            if success:
                return "Feedback reçu et sauvegardé en base de données."
        
        # Fallback vers le système de fichier
        Thread(target=save_feedback_legacy, args=(question, expected_response)).start()
        return "Feedback reçu et sauvegardé."
        
    except Exception as e:
        logger.error(f"Erreur dans feedback: {e}")
        return "Erreur lors de la sauvegarde du feedback."

# Route pour traiter les feedbacks et mettre à jour
@app.route("/process-feedbacks", methods=["POST"])
def process_feedbacks():
    try:
        if db:
            success = db.process_pending_feedbacks()
            if success:
                return "Feedbacks traités avec succès."
        
        return "Aucun feedback à traiter."
        
    except Exception as e:
        logger.error(f"Erreur dans process_feedbacks: {e}")
        return "Erreur lors du traitement des feedbacks."

# Route pour quitter l'application
@app.route("/quit", methods=["POST"])
def quit():
    Thread(target=update_and_quit).start()
    return "Application en cours de fermeture."

def update_and_quit():
    """Met à jour le modèle et quitte l'application"""
    try:
        # Traiter les feedbacks en base si disponible
        if db:
            db.process_pending_feedbacks()
        
        # Système legacy
        feedback_path = os.path.join(BASE_DIR, "data", "user_feedback.json")
        if os.path.exists(feedback_path):
            with open(feedback_path, 'r', encoding='utf-8') as file:
                feedback = json.load(file)
            if feedback:
                subprocess.run(["python", os.path.join(BASE_DIR, "update_model.py")])
                subprocess.run(["python", os.path.join(BASE_DIR, "train.py")])
        
        os._exit(0)
    except Exception as e:
        logger.error(f"Erreur lors de la fermeture: {e}")
        os._exit(1)

def save_feedback_legacy(question, expected_response):
    """Sauvegarde legacy des feedbacks"""
    try:
        feedback_path = os.path.join(BASE_DIR, "data", "user_feedback.json")
        os.makedirs(os.path.dirname(feedback_path), exist_ok=True)
        
        if os.path.exists(feedback_path):
            with open(feedback_path, 'r', encoding='utf-8') as file:
                feedback = json.load(file)
        else:
            feedback = []

        feedback.append({"question": question, "expected_response": expected_response})

        with open(feedback_path, 'w', encoding='utf-8') as file:
            json.dump(feedback, file, ensure_ascii=False, indent=2)
            
    except Exception as e:
        logger.error(f"Erreur sauvegarde legacy: {e}")

# Fonctions legacy (pour compatibilité)
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

def bow(sentence, words, show_details=False):
    if not words:
        return np.array([])
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"trouvé dans le sac : {w}")
    return np.array(bag)

def predict_class(sentence):
    if not model or not words or not classes:
        return []
    
    try:
        p = bow(sentence, words, show_details=False)
        if len(p) != len(words):
            p = np.pad(p, (0, len(words) - len(p)), mode='constant')
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]
    except Exception as e:
        logger.error(f"Erreur dans predict_class: {e}")
        return []

def get_response(ints, name=None):
    if not ints or not intents:
        return "Désolé, je ne vous ai pas compris."
    
    try:
        tag = ints[0]["intent"]
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                response = random.choice(intent["responses"])
                return response.replace("{n}", name) if name else response
        return "Désolé, je ne vous ai pas compris."
    except Exception as e:
        logger.error(f"Erreur dans get_response: {e}")
        return "Désolé, une erreur s'est produite."

def generate_contextual_response(response, user_input):
    """Reformule la réponse avec des variations naturelles"""
    try:
        # Templates de reformulation
        reformulation_templates = [
            response,  # Réponse originale
            f"D'accord, {response.lower()}" if not response.lower().startswith(('d\'accord', 'ok', 'très bien')) else response,
            f"Je vois. {response}" if not response.lower().startswith(('je', 'oui', 'non')) else response,
            f"Parfait ! {response}" if '?' not in response else response,
        ]
        
        # Ajout de variations contextuelles
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['merci', 'thanks']):
            reformulation_templates.append(f"De rien ! {response}")
        
        if any(word in user_lower for word in ['aide', 'aider', 'support']):
            reformulation_templates.append(f"Bien sûr, je suis là pour vous aider. {response}")
        
        if '?' in user_input:
            reformulation_templates.append(f"Voici ma réponse : {response}")
        
        # Sélection aléatoire
        selected_response = random.choice(reformulation_templates)
        
        if len(selected_response.strip()) < 5:
            return response
            
        return selected_response
        
    except Exception as e:
        logger.error(f"Erreur dans generate_contextual_response: {e}")
        return response

# Route pour les statistiques (nouvelle fonctionnalité)
@app.route("/stats", methods=["GET"])
def get_stats():
    try:
        if db:
            stats = db.get_stats()
            return f"""
            <h2>Statistiques du Chatbot</h2>
            <p>Entrées en base: {stats.get('total_entries', 0)}</p>
            <p>Feedbacks: {stats.get('total_feedbacks', 0)}</p>
            <p>Feedbacks en attente: {stats.get('pending_feedbacks', 0)}</p>
            <p>Conversations en mémoire: {len(conversation_memory)}</p>
            """
        else:
            return f"<p>Base de données non disponible. Conversations en mémoire: {len(conversation_memory)}</p>"
    except Exception as e:
        logger.error(f"Erreur dans get_stats: {e}")
        return "<p>Erreur lors de la récupération des statistiques</p>"

# Point d'entrée de l'application
if __name__ == "__main__":
    HOST = os.getenv('HOST', 'localhost')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Démarrage du chatbot sur {HOST}:{PORT}")
    logger.info(f"Mode API: {API_MODE}")
    logger.info(f"Base de données: {'Disponible' if db else 'Non disponible'}")
    logger.info(f"Modèle legacy: {'Disponible' if model else 'Non disponible'}")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
