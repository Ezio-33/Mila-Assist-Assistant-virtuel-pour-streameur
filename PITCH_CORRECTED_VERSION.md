# ML Portfolio Pitch: Mila-Assist (Version Corrigée)

## Projet

- **Nom**: Mila-Assist — Assistant virtuel IA pour streameurs (RAG + base vectorielle)
- **Auteur**: Samuel VERSCHUEREN  
- **Rôles**: Full-Stack Developer & ML Engineer

## Introduction

Mila-Assist est un assistant virtuel conçu pour les streameurs, s'appuyant sur une **architecture RAG hybride** avec recherche sémantique (TF‑IDF + similarité cosinus) et système de fallback intelligent. L'objectif est de fournir une assistance technique 24/7 pour la configuration et réduire la charge de support pour les développeurs d'AI_Licia.

## Description — Expérience utilisateur

- **Interface web Flask** simple pour poser des questions et obtenir des réponses instantanées
- **API REST sécurisée** (authentification JWT + rate limiting) pour intégration OBS/StreamerBot  
- **Architecture hybride en cascade** : TF-IDF vectoriel → Modèle Keras legacy → Reformulation adaptative
- **3 modes de réponse** : minimal (rapide), balanced (optimal), natural (avec sentence-transformers)
- **Disponibilité 24/24** avec système de fallback intelligent

## Architecture Technique Réelle

### **Base de Données Vectorielle**
- **SQLite** (développement) / **MySQL** (production) via SQLAlchemy
- **TF-IDF** avec scikit-learn pour la vectorisation (1000 features max)
- **Similarité cosinus** pour la recherche sémantique
- **Cache intelligent** des embeddings avec recalcul automatique

### **Modèles IA Implémentés**

#### 1. **Système TF-IDF Principal** (Niveau 1)
```python
# Recherche vectorielle rapide avec seuil configurable
self.vectorizer = TfidfVectorizer(max_features=1000, stop_words=None)
similarities = cosine_similarity(query_vector, self.question_vectors)[0]
```

#### 2. **Modèle Keras Legacy** (Niveau 2 - Fallback)
- **Fichier** : `chatbot_model.keras` (339 KB)
- **Classes** : 45 intentions spécifiques streameur (validé via intents.json)
- **Usage** : Classification d'intentions quand recherche vectorielle échoue
- **Architecture** : Non documentée dans le code source (legacy)

#### 3. **Sentence Transformer** (Niveau 3 - Mode Natural)
```python
# Chargement conditionnel pour économiser les ressources
from sentence_transformers import SentenceTransformer
self.sentence_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
```

### **Système de Modes Adaptatifs**
```python
class ResponseMode:
    MINIMAL = "minimal"      # TF-IDF direct, <50ms
    BALANCED = "balanced"    # TF-IDF + templates, <100ms  
    NATURAL = "natural"      # + sentence-transformers, <400ms
```

## Données

### **Sources de Données**
- **Intents.json** : 45 intentions streameur, 608 lignes de configuration
- **Base vectorielle** : Questions/réponses avec embeddings TF-IDF
- **Feedbacks utilisateurs** : Système de collecte avec protection anti-abus
- **Logs d'audit** : Traçabilité des interactions avec anonymisation

### **Gestion des Données**
- **Migration automatisée** depuis intents.json vers base SQL
- **Recalcul automatique** des vecteurs lors d'ajouts
- **Compteurs d'usage** pour optimiser les réponses populaires
- **Rate limiting** : Protection contre l'abus (configurable par IP)

## Sécurité et Conformité

### **Authentification API**
- **JWT tokens** avec expiration configurable
- **Clés API hachées** (SHA-256) avec permissions granulaires
- **Rate limiting** intégré (100 requêtes/minute par défaut)
- **Validation des entrées** contre injections SQL/XSS

### **Protection des Données** 
- **Anonymisation automatique** des feedbacks (IP hashée avec HMAC)
- **Pas de stockage d'informations personnelles** sensibles
- **Logs limités dans le temps** avec rotation automatique
- **Consentement explicite** pour la collecte de feedbacks

## Plateformes et Déploiement

- **Développement** : Linux/Windows, CPU uniquement (compatible Python 3.9+)
- **Production** : Docker, NAS Synology/VPS, reverse proxy ready
- **Base de données** : SQLite (local) → MySQL (production) sans migration
- **Monitoring** : Logs structurés, métriques d'utilisation intégrées

## Contraintes Techniques

### **Optimisations pour Ressources Limitées**
- **Pas de GPU** requis : architecture CPU-only
- **Modèles légers** : TF-IDF privilégié sur transformers lourds
- **Cache intelligent** : Réduction des calculs répétitifs
- **Fallback garantit** : Réponse assurée même si DB vide

### **Technologies Utilisées (Vérifiées)**
```python
# Dépendances principales
flask>=2.1.0          # Interface web
sqlalchemy>=1.4.46    # ORM base de données  
scikit-learn>=1.0.1   # TF-IDF et métriques
sentence-transformers>=2.2.2  # Mode natural (optionnel)
tensorflow>=2.7.0     # Modèle legacy (optionnel)
```

## Architecture des Fichiers (État Actuel)

```
Mila-Assist/
├── 📄 app_v2.py                # Application hybride principale (456 lignes)
├── 📄 api.py                   # Serveur API sécurisé (385 lignes)  
├── 📄 database.py              # Système RAG + vectorisation (417 lignes)
├── 📄 response_modes.py        # Modes adaptatifs (463 lignes)
├── 📄 start.py                 # Démarrage unifié (115 lignes)
├── 📄 requirements.txt         # Dépendances (à mettre à jour)
├── 📄 intents.json            # 45 intentions streameur (608 lignes)
├── 📄 chatbot_model.keras     # Modèle legacy (339 KB)
├── 📄 README_v2.md            # Documentation utilisateur
├── 🗂️ templates/              # Interface HTML/CSS
├── 🗂️ data/                   # Feedbacks et assets
└── 📄 chatbot_knowledge.db    # Base SQLite (générée)
```

## Roadmap Réaliste

### **Phase 1 (2 semaines) - Consolidation**
- ✅ Finaliser fichiers incomplets (app.py, vector_search.py vides)
- ✅ Corriger dépendances Python 3.12 compatibles
- ✅ Implémenter tests unitaires manquants
- ✅ Créer benchmarks de performance mesurables

### **Phase 2 (2 semaines) - Amélioration**  
- ✅ Interface d'administration web pour la gestion des connaissances
- ✅ Métriques de performance temps réel (dashboard)
- ✅ Documentation technique complète basée sur le code
- ✅ Démo fonctionnelle avec cas d'usage streameur

### **Évolutions Future (v2.1)**
- Support multi-langues automatique
- Intégration ChatGPT/Claude en fallback final
- Monitoring Prometheus + alertes
- Support Kubernetes pour scalabilité

## Valeur Ajoutée Démontrée

### **Innovation Technique**
- **Architecture adaptative** : 3 niveaux selon contraintes ressources
- **Système de fallback intelligent** : Garantie de réponse même en cas d'échec
- **Gestion des modes dynamique** : Changement à chaud selon la charge
- **Sécurité intégrée** : Authentication + rate limiting + protection données

### **Avantages Quantifiables**
- **Taille modèle** : 339 KB vs modèles BERT (500MB-1.3GB)
- **Mémoire requise** : Estimation <500MB vs >2GB pour alternatives lourdes
- **Compatibilité** : CPU-only vs GPU requis pour modèles récents
- **Temps de démarrage** : Estimation <10s vs >30s pour transformers lourds

*Note : Métriques de performance à valider par benchmarks à implémenter*

## Conclusion

Mila-Assist représente une **solution pragmatique et évolutive** pour l'assistance streameur, privilégiant la **fiabilité** et l'**accessibilité** plutôt que la performance brute. L'architecture hybride permet d'adapter les ressources selon les contraintes, tout en maintenant une qualité de service constante.

Le projet démontre une **maîtrise des contraintes réelles** de déploiement IA en production, avec une attention particulière à la sécurité et à la protection des données.