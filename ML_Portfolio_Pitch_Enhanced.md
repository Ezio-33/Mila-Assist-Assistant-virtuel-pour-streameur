# ML - Portfolio Pitch: Mila-Assist - Version Enrichie

## Projet

- Nom: Mila-Assist — Assistant virtuel IA pour streameurs (RAG + base vectorielle)
- Auteur:
- Lead Developer & ML Engineer (architecture RAG, base de données vectorielle): Samuel VERSCHUEREN
- Backend Developer (API REST, sécurité): Samuel VERSCHUEREN
- Frontend Developer (interface utilisateur, UX): Samuel VERSCHUEREN
- Data Engineer (preprocessing, optimisation des modèles): Samuel VERSCHUEREN

## Introduction

Mila-Assist est un assistant virtuel conçu pour les streameurs. Il s'appuie sur une **architecture hybride multi-modèles** combinant une recherche sémantique (TF‑IDF + similarité cosinus), un système de fallback avec réseau de neurones **Keras**, et une reformulation avancée avec **Sentence Transformers**. Objectifs: fournir de l'aide à la configuration et réduire la charge de l'assistance pour les développeurs de l'IA AI_Licia.

## Architecture IA - Modèles et Transformers

### 🧠 Modèle Principal: chatbot_model.keras

**Type**: Réseau de neurones dense (Sequential) pour classification d'intentions  
**Framework**: TensorFlow/Keras 2.7.0  
**Taille**: ~330 KB (modèle optimisé pour CPU)

#### Architecture du modèle:
```
Input Layer → Dense(128, ReLU) → Dropout(0.5) 
           → Dense(64, ReLU) → Dropout(0.5) 
           → Dense(45, Softmax)
```

#### Caractéristiques techniques:
- **Entrée**: Vectorisation Bag-of-Words (vocabulaire lemmatisé de ~800 mots)
- **Classes de sortie**: 45 intents spécialisés (greetings, configuration, troubleshooting, etc.)
- **Optimiseur**: SGD avec décroissance exponentielle du learning rate (0.01 → 0.96^epoch)
- **Dropout**: 50% pour éviter le surapprentissage
- **Activation**: ReLU pour les couches cachées, Softmax pour la classification

#### Pourquoi ce modèle ?
1. **Rapidité**: Inférence < 50ms sur CPU (i5, 8GB RAM)
2. **Robustesse**: Testé sur 45 catégories avec 200+ patterns d'entraînement
3. **Fallback fiable**: Garantit une réponse même si la base vectorielle échoue
4. **Légèreté**: Pas de dépendance GPU, compatible NAS/VPS

### 🔄 Transformer: paraphrase-multilingual-MiniLM-L12-v2

**Type**: Sentence Transformer multilingue  
**Modèle de base**: Microsoft MiniLM-L12  
**Usage**: Mode "naturel" pour reformulation contextuelle avancée

#### Spécifications:
- **Taille**: ~130 MB (modèle compact optimisé)
- **Langues**: Support français/anglais natif
- **Dimensions**: 384-dimensional sentence embeddings
- **Performance**: ~200-400ms par requête sur CPU

#### Pourquoi ce transformer ?
1. **Multilingual**: Optimisé pour le français (important pour le public streameur francophone)
2. **Compact**: MiniLM-L12 vs modèles lourds (BERT-Large: 1.3GB)
3. **Paraphrase-optimized**: Spécialement entraîné pour la reformulation de phrases
4. **Production-ready**: Stable avec sentence-transformers 2.2.2

### 🏗️ Architecture Hybride - Cascade Intelligente

```
Requête utilisateur
        ↓
1️⃣ Recherche vectorielle TF-IDF (SQL + cosinus)
   ├─ Similarité > 0.7 → Réponse directe
   └─ Échec ↓
2️⃣ Modèle Keras (chatbot_model.keras)
   ├─ Probabilité > 0.25 → Classification intent
   └─ Échec ↓
3️⃣ Réponse par défaut

Reformulation finale selon le mode:
├─ MINIMAL: Réponse brute
├─ BALANCED: Templates + variations
└─ NATURAL: Sentence Transformer + contexte conversationnel
```

#### Justification de l'approche hybride:
1. **Performance**: TF-IDF pour 80% des cas courants (ultra-rapide)
2. **Robustesse**: Keras pour les cas complexes (fallback intelligent)
3. **Qualité**: Sentence Transformer pour l'expérience utilisateur premium
4. **Évolutivité**: Ajout facile de nouveaux modèles sans casser l'existant

### 📊 Vectorisation et Embedding

#### TF-IDF (Primary):
- **Algorithme**: Term Frequency - Inverse Document Frequency
- **Implémentation**: scikit-learn TfidfVectorizer
- **Stockage**: Base SQLite avec index optimisés
- **Performance**: ~10-30ms par requête

#### Sentence Embeddings (Enhanced):
- **Méthode**: Transformations contextuelles via MiniLM
- **Utilisation**: Reformulation et continuité conversationnelle
- **Cache**: Embeddings mis en cache pour optimisation

## Description — Expérience utilisateur

- Interface web (Flask) simple pour poser des questions et obtenir des réponses instantanées.
- API REST sécurisée (clé API) pour intégration avec OBS/StreamerBot.
- **Mode adaptatif**: Le système choisit automatiquement le modèle optimal selon les ressources disponibles
- **3 modes de qualité**:
  - **Minimal**: TF-IDF pur (< 50ms, 50MB RAM)
  - **Balanced**: TF-IDF + templates (< 100ms, 100MB RAM)
  - **Natural**: TF-IDF + Sentence Transformers (< 400ms, 200MB RAM)
- Gain de temps et Disponibilité 24/24

## Données

- Types: questions/patterns, tags/intents, réponses, feedbacks, journaux d'interactions, scores de similarité.
- Collecte:
  - Import automatisé depuis intents.json (legacy).
  - Migration intelligente vers base vectorielle TF-IDF
  - Feedbacks saisis via l'UI/API, avec quotas pour éviter l'abus.
- Stockage:
  - SQLite (dev/local) ou MySQL (prod/NAS) via SQLAlchemy.
  - Embeddings: TF‑IDF persisté, recalcul périodique.
  - **Modèles persistés**: chatbot_model.keras + vocabulaire (words.pkl, classes.pkl)
  - Logs: fichiers ou table dédiée.

### 🔄 Pipeline de données IA:
```
intents.json → Preprocessing (NLTK) → 
├─ TF-IDF Vectorization → SQLite/MySQL
├─ Keras Training Data → chatbot_model.keras
└─ Vocabulary → words.pkl + classes.pkl
```

## Choix Techniques et Justifications IA

### Pourquoi ne pas utiliser un LLM complet ?
1. **Ressources limitées**: Déploiement sur NAS Synology (ARM, 2-4GB RAM)
2. **Coût**: Pas d'API externe payante (OpenAI, Claude)
3. **Latence**: < 500ms requis pour l'expérience streameur
4. **Contrôle**: Réponses prédictibles et modérables

### Pourquoi TensorFlow/Keras vs PyTorch ?
1. **Écosystème mature**: TF 2.7 stable pour production
2. **Optimisation CPU**: TensorFlow Lite compatible si besoin
3. **Déploiement**: Support Docker + serving simple
4. **Legacy**: Compatibilité avec modèle existant v1.0

### Pourquoi MiniLM vs autres transformers ?
1. **Taille**: 130MB vs 1.3GB (BERT-Large) vs 500MB (CamemBERT)
2. **Multilingual**: Français natif vs modèles anglais uniquement
3. **Paraphrase**: Spécialisé reformulation vs classification générale
4. **CPU Performance**: Optimisé pour inférence sans GPU

## Éthique et conformité

- Pas de données personnelles stockées.
- **Modèles locaux**: Aucune donnée envoyée vers API externes
- Anonymisation des feedbacks; rate‑limit + modération basique pour éviter les abus.
- **Transparence**: README détaillé + architecture ouverte
- Droit à l'oubli: aucune donnée utilisateur n'est stockée
- **Auditabilité**: Logs des prédictions et scores de confiance

## Plateformes ciblées

- Développement: Linux/Windows, CPU only (min i5, 8 Go RAM).
- Déploiement: Docker, NAS Synology/VPS, API HTTP.
- **Modèles optimisés**: Pas de dépendance GPU; modèles compacts privilégiés.
- **Monitoring IA**: Métriques de performance des modèles intégrées

## Contraintes et hypothèses

- Ressources limitées: **Choix délibéré de modèles légers** vs gros LLM/embeddings lourds.
- **Compromis qualité/performance**: TF‑IDF + Keras vs Transformers lourds
- Sécurité: accès API restreint par clé.
- Disponibilité: **Système de fallback en cascade** pour assurer réponse même si composants IA échouent.

## MVP (fonctionnalités cœur)

- **Recherche hybride**: TF‑IDF + similarité cosinus sur base vectorielle (SQLite).
- **Fallback intelligent**: intents.json + modèle Keras si score < seuil.
- **API REST sécurisée** (clé API) + interface web.
- **Modes adaptatifs**: Détection automatique des ressources disponibles

## Feature ciblée (scope court)

- Refondre la gestion des retours utilisateurs:
  - **Amélioration des modèles via feedback**: Réentraînement incrémental
  - Amélioration de l'interface graphique par rapport à la version 1
  - Version du tchat en .exemples
  - Ajout du tchat sur le site
  - **Intégration semi‑auto**: Suggestions de nouveaux patterns/réponses basées sur l'analyse IA

## Données — Détails de la feature

- Schéma feedback:
  - id, timestamp, source (web/api), ip_hash, tag_candidat, message_utilisateur, reponse_fournie, commentaire.
  - **Scores de confiance**: Métriques IA pour qualité des prédictions
- Règles anti‑abus: rate‑limit par IP, seuils journaliers, blocage si spam détecté.
- Respect vie privée: ip_hash par HMAC(secret, ip), rotation possible.
- **Amélioration continue**: Feedback utilisé pour fine-tuning des modèles

## Métriques et Monitoring IA

### 📈 KPIs Techniques:
- **Latence par modèle**: TF-IDF (<30ms), Keras (<50ms), Sentence-T (<400ms)
- **Taux de couverture**: % requêtes résolues par niveau (vectoriel/keras/fallback)
- **Précision par intent**: Accuracy du modèle Keras par catégorie
- **Similarité moyenne**: Score cosinus pour recherche vectorielle

### 🔍 Monitoring Production:
- **Health checks**: Vérification disponibilité modèles au démarrage
- **Performance logs**: Temps de réponse par composant IA
- **Error tracking**: Échecs de prédiction et fallbacks activés
- **Resource usage**: RAM/CPU par modèle en temps réel

## Planification (4 semaines)

- S1 — Mise en service du chatbot (priorité au fonctionnement)
  - Vérifier l'installation, .env et initialisation DB; (re)construction de l'index TF‑IDF.
  - **Validation modèles IA**: Test chargement Keras + Sentence Transformers
  - Assurer le pipeline de réponse: UI/endpoint de question → recherche TF‑IDF → fallback intents → réponse.
  - Ajuster le seuil de similarité et corriger les erreurs bloquantes; tests manuels de bout en bout.
  - UI minimale opérationnelle (champ de saisie + affichage de la réponse).

- S2 — Enrichissement base + tests basiques
  - Collecter manuellement des Q/R pertinentes depuis le Discord officiel (sans données personnelles).
  - **Optimisation modèles**: Fine-tuning seuils TF-IDF + Keras confidence
  - Normaliser et insérer dans la knowledge_base (tags, question canonique, réponse); recalcul TF‑IDF.
  - Ajuster les seuils pour améliorer la pertinence CPU‑only.
  - Ajouter quelques tests unitaires **+ tests de performance IA**.

- S3 — Enrichissement avancé
  - Continuer l'enrichissement Q/R depuis Discord, catégoriser par tags, puis recalcul TF‑IDF.
  - **Intégration Sentence Transformers**: Mode naturel + reformulation contextuelle
  - Créer une table feedbacks minimale: id, timestamp, question, rating ∈ {−1,0,+1}, reponse_id|tag, commentaire optionnel.
  - **Métriques IA**: Dashboard monitoring performance modèles
  - UI: amélioration globale.
  - Ne pas stocker de message utilisateur; conserver uniquement des métriques (rating/tag/horodatage).
  - Nettoyage de code (organisation fichiers, PEP8).

- S4 — Finition et démo
  - **Optimisation finale**: Cache embeddings + compression modèles
  - Nettoyage de code (organisation fichiers, PEP8).
  - Mise à jour du README (captures, variables .env, endpoints, **architecture IA**, limites et choix éthiques).
  - **Vidéo démo**: question → réponse → 3 modes IA → ajout Q/R.
  - Demander la QA manuelle et préparer 3–4 slides de présentation **+ métriques IA**.

## Risques et mitigations

- Manque de temps: concentrer sur **modèles core** (TF-IDF + Keras) + API + UI, reporter Sentence Transformers avancé.
- **Ressources limitées**: Benchmark continu, fallback obligatoire, monitoring RAM/CPU
- **Performance IA**: Dégradation gracieuse entre modes, cache intelligent
- Sécurité: clés API, rate‑limit, logs d'audit; **pas de PII dans les modèles**.

## Indicateurs de succès (KPIs)

- **Couverture intelligente**: > 85% requêtes résolues par TF-IDF (niveau 1)
- **Précision Keras**: > 75% accuracy sur validation set
- **Performance**: < 500ms temps de réponse moyen (tous modes)
- Taux de feedback utile (> 70%).
- Réduction des questions sans réponse.
- **Latence IA**: TF-IDF < 30ms, Keras < 50ms, Sentence-T < 400ms
- Augmentation de la couverture de la base de connaissances.

## Dépendances

### 🔧 Core IA:
- **TensorFlow 2.7.0**: Modèle Keras + optimisations CPU
- **sentence-transformers 2.2.2**: MiniLM-L12 multilingue  
- **scikit-learn 1.0.1**: TF-IDF vectorization + similarité cosinus
- **nltk 3.6.5**: Preprocessing (tokenization, lemmatization)
- **numpy**: Calculs matriciels optimisés

### 🌐 Infrastructure:
- Python 3.9+, Flask, SQLAlchemy
- Optionnel: Docker, MySQL, reverse proxy (Caddy/Nginx).

## Démo

- **Web**: interface Flask + monitoring IA temps réel
- **API**: /api/ask, /api/feedback, /api/model_status
- **Données**: intents.json migrées + base vectorielle TF-IDF + modèle Keras
- **Modes**: Démonstration des 3 niveaux de qualité IA

## Blog post

**Titre**: « Construire un assistant streameur intelligent : Architecture hybride TF-IDF + Keras + Sentence Transformers (CPU-only) »

**Sections**: 
1. **Contexte**: Pourquoi pas un LLM complet ?
2. **Architecture IA**: Cascade TF-IDF → Keras → Transformers
3. **Choix techniques**: Modèles légers vs performance
4. **Optimisations CPU**: Latence < 500ms sans GPU  
5. **Sécurité & feedback**: Amélioration continue des modèles
6. **Démo**: 3 modes de qualité en action
7. **Leçons**: Compromis intelligents pour contraintes matérielles

---

## 🚀 Points différenciants ML/IA

### Innovation technique:
1. **Architecture cascade intelligente**: Optimisation ressources via fallbacks
2. **Modèles adaptatifs**: Auto-sélection selon ressources disponibles  
3. **Hybrid RAG**: Recherche vectorielle + classification neuronale
4. **CPU-optimized**: Production sans GPU sur hardware limité

### Valeur ajoutée:
- **Déploiement accessible**: NAS domestique vs cloud coûteux
- **Réponses contrôlées**: Prédictibilité vs hallucinations LLM
- **Amélioration continue**: Feedback loop pour fine-tuning
- **Multilingual native**: Français optimisé vs adaptation modèles anglais

Cette approche démontre une **maîtrise technique des contraintes réelles** de déploiement IA en production avec des ressources limitées, tout en maintenant une expérience utilisateur de qualité.