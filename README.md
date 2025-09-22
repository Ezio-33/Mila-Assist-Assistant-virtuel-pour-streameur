# 🤖 Mila Assist - Assistant Virtuel pour Streameurs

![Python](https://img.shields.io/badge/python-3.13+-green)
![Flask](https://img.shields.io/badge/flask-2.3+-orange)
![TensorFlow](https://img.shields.io/badge/tensorflow-2.13+-red)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-yellow)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

**Mila Assist** est un assistant virtuel destiné aux créateurs de contenu utilisant la plateforme AI_Licia.
Son objectif : guider les streameurs dans la configuration de leur profil IA (voix, personnalité, comportements) et répondre aux questions récurrentes pour soulagé le support sur discord.
Grâce à une architecture hybride (modèle local + API externe), Mila Assist est disponible 24h/24, 7j/7 avec des réponses rapides et pertinentes.
Dans le futur je souhaite aussi integré des question et des aides pour le monde du stream.
Ce projet, initié dans le cadre de la formation RNCP 6, constitue un portfolio technique complet.

---

## 📋 Table des matières

1. [Objectifs](#objectifs)
2. [Fonctionnalités](#fonctionnalites)
3. [Architecture](#architecture)
4. [Prérequis](#prerequis)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Utilisation](#utilisation)
8. [Modes de fonctionnement](#modes-de-fonctionnement)
9. [Entraînement du modèle](#entrainement-du-modele)
10. [Tests](#tests)
11. [Contribution](#contribution)
12. [Licence](#licence)
13. [Auteur](#auteur)

---

## 🎯 Objectifs

- **Assistance automatisée** : répondre aux questions fréquentes des spectateurs avec un haut niveau de précision.
- **Haute disponibilité** : basculement automatique vers le modèle local en cas d’indisponibilité de l’API.
- **Performances optimales** : temps de réponse courts grâce au préchargement du modèle et à l’optimisation du code.
- **Évolutivité** : architecture modulaire en micro‑services pour faciliter l’ajout de fonctionnalités et la maintenance.
- **Simplicité d’utilisation** : interface web responsive accessible à tous, assistance 24h/24.

---

## ✨ Fonctionnalités

- **Configuration guidée d’AI_Licia** : création et personnalisation du profil IA (apparence, voix, personnalité).
- **Chargement asynchrone du modèle** : TensorFlow chargé en arrière‑plan, disponible en local en cas de panne API.
- **Gestion de session** : conversation fluide et contextuelle pour chaque utilisateur.
- **Système de feedback** : évaluation des réponses et suggestions pour améliorer le modèle.
- **Monitoring et journalisation** : surveillance en temps réel, logs structurés avec rotation et masquage des clés sensibles.
- **Micro‑services spécialisés** : client API, gestion des sessions, feedback, accès aux données.
- **Protection et sécurité** : validation des entrées, anti‑injection, gestion mémoire intelligente, masquage des clés API, limitation de la taille des messages.
- **Techniques avancées** :
  - Architecture microservices (5 services métier)
  - Configuration sécurisée via variables d'environnement
  - Logging structuré
  - Tests automatisés
  - Mémoire optimisée (< 800MB)

---

## 🏗️ Architecture

L’architecture suit un modèle micro‑services, facilitant la maintenance et l’évolution :

- **Interface Web** : templates HTML, CSS responsive, JavaScript
- **Services métier** :
  - ChatbotService : orchestration des réponses (API ou modèle local)
  - SessionService : gestion et persistance des sessions utilisateur
  - FeedbackService : collecte et stockage des évaluations
  - DatabaseService/API Client : connexion aux bases et API externes
- **Données & IA** :
  - Modèle local TensorFlow (chatbot_model.keras)
  - Cache JSON, fichiers pickles (words.pkl, classes.pkl, training_patterns.pkl)

---

## 🛠️ Prérequis

- Python ≥ 3.13
- pip
- Accès réseau (optionnel, fallback local disponible)
- 1 Go de RAM libre pour TensorFlow

---

## 🚀 Installation

### Installation rapide

```bash
git clone https://github.com/Ezio-33/Mila-Assist-Assistant-virtuel-pour-streameur.git
cd Mila-Assist-Assistant-virtuel-pour-streameur
pip install -r requirements_full.txt
cp .env.example .env
python start.py web
```

### Installation avec script automatisé

```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Installation manuelle

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install flask>=2.3.0 tensorflow>=2.13.0 nltk>=3.8.0 requests>=2.31.0 python-dotenv>=1.0.0
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
cp .env.example .env
python start.py web
```

---

## ⚙️ Configuration

Les paramètres sensibles sont centralisés dans `.env` (exemple fourni) :

```env
HOST=localhost
PORT=5000
DEBUG=false
USE_API=true
API_URL=https://votre-api.com/chat
API_KEY=votre_cle_api
API_TIMEOUT=1
USE_LEGACY_FALLBACK=true
SECRET_KEY=votre_cle_secrete
```

**Bonnes pratiques** :

- Ne jamais publier de clés sensibles en clair
- Les clés sont automatiquement masquées dans les logs

---

## 🎮 Utilisation

Après démarrage, ouvrez votre navigateur à l’URL :

- http://localhost:5000/
- API de statut : /model_status
- API de santé : /health

**Interface** :

1. Posez votre question
2. Envoyez (Entrée ou bouton)
3. Recevez la réponse (API ou modèle local)

---

## ⚡ Modes de fonctionnement

- **Hybride (par défaut)** : API externe prioritaire, fallback local automatique
- **Local intelligent** : modèle local optimisé (cache, pré‑traitement, gestion d’erreurs)

---

## 🧠 Entraînement du modèle

Le modèle Keras est entraîné à partir de données Q/R :

- 122 entrées API, tokenisation et lemmatisation NLTK
- Validation sur 99 questions de référence
- Fichiers générés : chatbot_model.keras, words.pkl, classes.pkl, training_patterns.pkl

Pour relancer l’entraînement :

```bash
python train.py
```

---

## 🧪 Tests

Suite de tests automatisés pour valider stabilité et performance :

```bash
python -m pytest tests/ -v
```

Scripts ciblés : test_performance_leger.py, test_fonctionnement_local.py, etc.

**Résultats (17/09/2025)**

- Chargement config : ~14 ms
- Précision/temps :
  - Local intelligent : ~95 %, ~418 ms
  - Local brut : ~90 %, ~114 ms
  - API : ~99 %, ~620 ms
- Sécurité anti‑injection : toutes les entrées malveillantes filtrées
- Dépendances : 11 modules critiques
- Charge : 5, 10, 20 requêtes simultanées traitées
- Mémoire : ~1 GB, gestion correcte du cache
- Cas limites : taux de succès élevé

---

**Bonnes pratiques** :

- Style Python PEP 8
- Docstrings et type hints
- Tests unitaires
- Journalisation appropriée
- Respect de l’architecture modulaire (services/, config/)

---

## 📄 Licence

Mila Assist est distribué sous licence Creative Commons Attribution – Pas d’usage commercial 4.0 International (CC BY‑NC 4.0).
Vous êtes libre de partager et d’adapter le projet à condition d’indiquer l’auteur original et de ne pas l’utiliser à des fins commerciales sans accord préalable.

---

## 👨‍💻 Auteur

Projet créé par **Samuel Verschueren** dans le cadre de la certification RNCP 6 – Concepteur Développeur d’Applications.
Auteur et mainteneur principal de Mila Assist.
Contact : [LinkedIn](https://www.linkedin.com/in/samuel-verschueren)
