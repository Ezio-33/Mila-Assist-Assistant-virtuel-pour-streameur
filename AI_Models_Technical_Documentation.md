# Documentation Technique - Modèles IA Mila-Assist

## 🧠 Vue d'ensemble de l'architecture IA

Mila-Assist utilise une **architecture hybride multi-modèles** optimisée pour des contraintes de ressources limitées (CPU-only, <4GB RAM) tout en maintenant une qualité de réponse élevée.

## 📋 Inventaire des modèles IA

### 1. Modèle Principal: chatbot_model.keras

**Type**: Réseau de neurones feed-forward pour classification d'intentions  
**Framework**: TensorFlow/Keras 2.7.0  
**Fichier**: `chatbot_model.keras` (330 KB)  
**Rôle**: Système de fallback intelligent pour classification d'intentions  

#### Architecture détaillée:
```python
model = Sequential([
    Input(shape=(len(vocabulary),)),           # ~800 features (vocabulaire)
    Dense(128, activation='relu'),             # Couche cachée 1
    Dropout(0.5),                             # Régularisation
    Dense(64, activation='relu'),              # Couche cachée 2  
    Dropout(0.5),                             # Régularisation
    Dense(45, activation='softmax')            # Classification 45 intents
])
```

#### Paramètres d'entraînement:
- **Optimiseur**: SGD avec momentum (0.9) et Nesterov
- **Learning Rate**: Décroissance exponentielle (0.01 → 0.96^epoch)
- **Loss**: Categorical Crossentropy
- **Epochs**: 200
- **Batch Size**: 5
- **Données**: ~300 patterns d'entraînement sur 45 classes

#### Preprocessing:
1. **Tokenisation**: NLTK word_tokenize
2. **Lemmatisation**: WordNetLemmatizer (anglais/français)
3. **Vectorisation**: Bag-of-Words binaire
4. **Vocabulaire**: Sauvegardé dans `words.pkl` (~800 mots uniques)
5. **Classes**: Sauvegardées dans `classes.pkl` (45 intents)

#### Performance:
- **Seuil de confiance**: 0.25 (25%)
- **Latence**: < 50ms sur CPU i5
- **Mémoire**: ~10MB chargé en RAM
- **Accuracy**: ~85% sur données de validation

#### Utilisation dans le code:
```python
# Chargement (app_v2.py ligne 58-61)
model_path = os.path.join(BASE_DIR, "chatbot_model.keras")
if os.path.exists(model_path):
    model = load_model(model_path)

# Prédiction (app_v2.py ligne 359-374)  
def predict_class(sentence):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]
```

### 2. Transformer: paraphrase-multilingual-MiniLM-L12-v2

**Type**: Sentence Transformer multilingue  
**Base**: Microsoft MiniLM-L12  
**Taille**: ~130 MB  
**Rôle**: Reformulation contextuelle avancée (mode "natural")  

#### Spécifications techniques:
- **Architecture**: 12 couches Transformer
- **Attention heads**: 12
- **Hidden size**: 384
- **Vocabulaire**: 250k tokens (multilingue)
- **Langues supportées**: 50+ dont français optimisé
- **Max sequence length**: 128 tokens

#### Utilisation:
```python
# Chargement (response_modes.py ligne 97-100)
from sentence_transformers import SentenceTransformer
self.sentence_model = SentenceTransformer(
    'paraphrase-multilingual-MiniLM-L12-v2'
)
```

#### Fonctionnalités:
1. **Reformulation contextuelle**: Amélioration des réponses brutes
2. **Mémoire conversationnelle**: Continuité entre échanges
3. **Détection de similarité**: Comparaison sémantique entre questions
4. **Templates intelligents**: Adaptation du style selon le contexte

### 3. Vectorisation TF-IDF

**Type**: Term Frequency - Inverse Document Frequency  
**Implémentation**: scikit-learn TfidfVectorizer  
**Rôle**: Recherche sémantique primaire (niveau 1)  

#### Configuration:
```python
# Vectorisation (database.py)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words=None,  # Personnalisé pour français
    ngram_range=(1, 2)  # Unigrammes + bigrammes
)
```

#### Performance:
- **Latence**: 10-30ms par requête
- **Seuil similarité**: 0.7 (70%)
- **Stockage**: Base SQLite avec index optimisés
- **Couverture**: ~80% des requêtes résolues au niveau 1

## 🔄 Pipeline de traitement hybride

### Cascade intelligente:
```
1. 📊 TF-IDF Vectoriel (Primaire)
   ├─ Similarité ≥ 0.7 → ✅ Réponse directe
   └─ Échec → Niveau 2

2. 🧠 Modèle Keras (Fallback)  
   ├─ Confiance ≥ 0.25 → ✅ Classification intent
   └─ Échec → Niveau 3

3. 💬 Réponse par défaut
   └─ ✅ Message générique

4. 🎨 Reformulation (Post-processing)
   ├─ MINIMAL: Réponse brute
   ├─ BALANCED: Templates + variations  
   └─ NATURAL: Sentence Transformer + contexte
```

### Optimisations de performance:
1. **Détection automatique de mode**: Selon RAM disponible
2. **Cache embeddings**: Évite recalculs coûteux
3. **Lazy loading**: Chargement à la demande des modèles lourds
4. **Fallback graceful**: Jamais d'échec total

## 📈 Métriques et monitoring

### KPIs par modèle:
```python
# Métriques collectées en temps réel
{
    "tfidf": {
        "latency_ms": 25,
        "coverage_rate": 0.78,
        "avg_similarity": 0.82
    },
    "keras": {
        "latency_ms": 45,
        "usage_rate": 0.15,
        "avg_confidence": 0.67
    },
    "sentence_transformer": {
        "latency_ms": 350,
        "usage_rate": 0.12,
        "enhancement_applied": 0.45
    }
}
```

### Logs de performance:
```python
# Exemple de log (app_v2.py)
logger.info(f"Réponse trouvée en DB (similarité: {best_match['similarity']:.2f})")
logger.info("Réponse du système legacy")
logger.warning(f"sentence-transformers non disponible ({e})")
```

## 🔧 Configuration et déploiement

### Variables d'environnement:
```bash
# Mode de réponse IA  
RESPONSE_MODE=balanced  # minimal|balanced|natural

# Seuils de performance
TFIDF_THRESHOLD=0.7
KERAS_THRESHOLD=0.25

# Optimisations
SENTENCE_TRANSFORMER_CACHE=true
MODEL_PRELOAD=true
```

### Ressources système:
```yaml
Minimal (TF-IDF only):
  RAM: ~50MB
  CPU: <10% sur i5
  Latence: <30ms

Balanced (TF-IDF + Keras):
  RAM: ~100MB  
  CPU: <20% sur i5
  Latence: <100ms

Natural (Full stack):
  RAM: ~200MB
  CPU: <30% sur i5  
  Latence: <400ms
```

## 🔍 Justifications techniques

### Pourquoi cette architecture ?

1. **Contraintes matérielles**: NAS Synology, VPS basiques
2. **Contraintes budget**: Pas d'API externe payante
3. **Contraintes latence**: < 500ms pour UX streameur
4. **Contraintes qualité**: Réponses cohérentes et contrôlables

### Alternatives considérées et rejetées:

#### ❌ LLM complets (GPT, Claude):
- **Pro**: Qualité excellente
- **Con**: Coût prohibitif, latence réseau, dépendance externe

#### ❌ BERT-Large, CamemBERT:
- **Pro**: Précision élevée  
- **Con**: 1.3GB RAM, 2-5s latence, GPU requis

#### ❌ Modèles locaux (Llama, Mistral):
- **Pro**: Contrôle total
- **Con**: >8GB RAM, GPU requis, complexité déploiement

### ✅ Solution retenue:
**Cascade TF-IDF → Keras → MiniLM** offre le meilleur compromis:
- Performance acceptable sur hardware limité
- Qualité suffisante pour cas d'usage streameur  
- Coût opérationnel minimal
- Évolutivité vers modèles plus avancés

## 🛠️ Amélioration continue

### Feedback loop:
1. **Collecte**: Évaluations utilisateur via UI/API
2. **Analyse**: Identification patterns d'échec  
3. **Enrichissement**: Ajout données d'entraînement
4. **Réentraînement**: Périodique des modèles
5. **A/B Testing**: Validation amélioration

### Roadmap IA:
- **Court terme**: Fine-tuning seuils + cache optimisation
- **Moyen terme**: Ensemble methods, custom embeddings
- **Long terme**: Migration vers modèles plus avancés si ressources

Cette architecture démontre une **approche pragmatique de l'IA en production**, privilégiant la robustesse et l'efficacité aux performances académiques maximales.