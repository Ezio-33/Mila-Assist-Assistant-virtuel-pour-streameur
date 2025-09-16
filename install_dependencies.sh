#!/bin/bash
# Installation des dépendances pour Priv-_Mila-Assit

echo "🚀 Installation des dépendances Python..."
pip install -r requirements_full.txt

echo "📦 Configuration des ressources NLTK..."
python -c "
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
print('✅ Ressources NLTK téléchargées')
"

echo "✅ Installation terminée!"
