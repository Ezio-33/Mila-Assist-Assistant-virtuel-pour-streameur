"""
Système de génération de réponses à plusieurs niveaux de qualité
Version 2.0 - Modes adaptatifs selon les ressources disponibles
"""

import os
import json
import random
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseMode:
    """Énumération des modes de réponse"""
    MINIMAL = "minimal"      # TF-IDF simple, réponse directe
    BALANCED = "balanced"    # TF-IDF + templates de reformulation
    NATURAL = "natural"      # sentence-transformers + génération avancée

class ResponseTemplates:
    """Templates pour la reformulation des réponses"""
    
    # Modèles d'introduction
    INTROS = [
        "D'après mes connaissances, {response}",
        "Je peux vous dire que {response}",
        "Voici ce que je sais : {response}",
        "Permettez-moi de vous expliquer : {response}",
        "Bien sûr ! {response}",
        "Excellente question ! {response}",
        "Je suis ravi de vous aider. {response}",
        "C'est une bonne question. {response}",
        "{response}",  # Direct parfois
    ]
    
    # Modèles de conclusion
    OUTROS = [
        " Est-ce que cela répond à votre question ?",
        " J'espère que cela vous aide !",
        " N'hésitez pas si vous avez d'autres questions.",
        " Y a-t-il autre chose que vous aimeriez savoir ?",
        " Avez-vous besoin de plus de détails ?",
        "",  # Pas de conclusion parfois
        "",
        "",
    ]
    
    # Templates pour différents types de questions
    QUESTION_TYPES = {
        "greeting": [
            "Bonjour ! {response}",
            "Salut ! {response}",
            "Hello ! {response}",
            "{response} Comment puis-je vous aider aujourd'hui ?",
        ],
        "goodbye": [
            "{response} À bientôt !",
            "{response} Passez une excellente journée !",
            "{response} Au revoir !",
            "{response}",
        ],
        "thanks": [
            "{response} C'est avec plaisir !",
            "Je vous en prie ! {response}",
            "Pas de problème ! {response}",
            "{response}",
        ],
        "help": [
            "Bien sûr, je peux vous aider ! {response}",
            "Voici comment je peux vous assister : {response}",
            "Je suis là pour ça ! {response}",
            "{response}",
        ],
        "question": [
            # Pour les questions d'identité ou de présentation, on évite les intros génériques
            "{response}",
            "Voici ce que je sais : {response}",
        ],
    }

class ResponseEnhancer:
    """Classe pour améliorer les réponses selon le mode choisi"""
    
    def __init__(self, mode: str = ResponseMode.BALANCED):
        self.mode = mode
        self.templates = ResponseTemplates()
        self.conversation_context = []
        
        # Chargement optionnel de sentence-transformers pour mode NATURAL
        self.sentence_model = None
        if mode == ResponseMode.NATURAL:
            try:
                from sentence_transformers import SentenceTransformer
                self.sentence_model = SentenceTransformer(
                    'paraphrase-multilingual-MiniLM-L12-v2'
                )
                logger.info("Modèle sentence-transformers chargé pour mode naturel")
            except (ImportError, Exception) as e:
                logger.warning(f"sentence-transformers non disponible ({e}), utilisation du mode naturel sans transformer")
                # On garde le mode NATURAL mais sans sentence-transformers
    
    def detect_question_type(self, question: str) -> str:
        """Détecte le type de question pour choisir le bon template"""
        question_lower = question.lower().strip()
        
        # Salutations
        if any(word in question_lower for word in ['bonjour', 'salut', 'hello', 'hey', 'bonsoir']):
            return "greeting"
        
        # Au revoir
        if any(word in question_lower for word in ['au revoir', 'bye', 'adieu', 'à bientôt']):
            return "goodbye"
        
        # Remerciements
        if any(word in question_lower for word in ['merci', 'thanks', 'remercie']):
            return "thanks"
        
        # Demande d'aide
        if any(word in question_lower for word in ['aide', 'help', 'assister', 'comment', 'peux-tu']):
            return "help"
        
        # Question générale
        if question_lower.endswith('?') or any(word in question_lower for word in ['qui', 'que', 'quoi', 'où', 'quand', 'pourquoi', 'comment']):
            return "question"
        
        return "question"  # Par défaut
    
    def enhance_response_minimal(self, response: str, question: str, confidence: float) -> str:
        """Mode minimal : retourne la réponse directement (TF-IDF simple)"""
        return response.strip()
    
    def enhance_response_balanced(self, response: str, question: str, confidence: float) -> str:
        """Mode équilibré : ajoute des templates de reformulation"""
        question_type = self.detect_question_type(question)
        
        # Choix d'un template selon le type de question
        if question_type in self.templates.QUESTION_TYPES:
            templates = self.templates.QUESTION_TYPES[question_type]
            template = random.choice(templates)
            enhanced_response = template.format(response=response.strip())
        else:
            # Template générique
            intro = random.choice(self.templates.INTROS)
            outro = random.choice(self.templates.OUTROS)
            enhanced_response = intro.format(response=response.strip()) + outro
        
        # Ajout de variations selon la confiance
        if confidence < 0.6:
            uncertainty_phrases = [
                "Je pense que ",
                "Il me semble que ",
                "Si je comprends bien, ",
                "D'après mes informations, ",
            ]
            uncertainty = random.choice(uncertainty_phrases)
            enhanced_response = uncertainty + enhanced_response.lower()
        
        return enhanced_response
    
    def enhance_response_natural(self, response: str, question: str, confidence: float) -> str:
        """Mode naturel : génération pseudo-LLM sans sentence-transformers"""
        if self.sentence_model is None:
            # Version naturelle améliorée SANS sentence-transformers
            return self._enhance_response_natural_fallback(response, question, confidence)
        
        # Si sentence-transformers est disponible, utilisation avancée
        enhanced = self.enhance_response_balanced(response, question, confidence)
        
        # Ajout de contexte conversationnel
        if len(self.conversation_context) > 0:
            last_topic = self.conversation_context[-1]
            if self._is_related_topic(question, last_topic):
                continuity_phrases = [
                    "Pour continuer sur ce sujet, ",
                    "En rapport avec votre précédente question, ",
                    "Dans la même lignée, ",
                ]
                continuity = random.choice(continuity_phrases)
                enhanced = continuity + enhanced.lower()
        
        # Mémorisation du contexte
        self.conversation_context.append(question)
        if len(self.conversation_context) > 5:  # Garde seulement les 5 dernières
            self.conversation_context.pop(0)
        
        return enhanced
    
    def _enhance_response_natural_fallback(self, response: str, question: str, confidence: float) -> str:
        """Mode naturel sans sentence-transformers : génération pseudo-LLM"""
        # Analyse sémantique simple de la question
        question_sentiment = self._analyze_question_sentiment(question)
        question_complexity = self._analyze_question_complexity(question)
        
        # Reformulation de la réponse de base
        reformulated = self._reformulate_response_naturally(response, question_sentiment, question_complexity)
        
        # Ajout d'éléments conversationnels
        conversational = self._add_conversational_elements(reformulated, question, confidence)
        
        # Ajout de contexte si pertinent
        if len(self.conversation_context) > 0:
            conversational = self._add_contextual_continuity(conversational, question)
        
        # Mémorisation du contexte
        self.conversation_context.append(question)
        if len(self.conversation_context) > 5:
            self.conversation_context.pop(0)
        
        return conversational
    
    def _analyze_question_sentiment(self, question: str) -> str:
        """Analyse simple du sentiment de la question"""
        question_lower = question.lower()
        
        positive_words = ['merci', 'super', 'génial', 'parfait', 'excellent', 'bien', 'content']
        negative_words = ['problème', 'erreur', 'mauvais', 'difficile', 'ennui', 'souci']
        neutral_words = ['comment', 'pourquoi', 'que', 'qui', 'où', 'quand']
        
        if any(word in question_lower for word in positive_words):
            return "positive"
        elif any(word in question_lower for word in negative_words):
            return "negative"
        else:
            return "neutral"
    
    def _analyze_question_complexity(self, question: str) -> str:
        """Analyse la complexité de la question"""
        question_lower = question.lower()
        
        # Mots indiquant une question complexe
        complex_indicators = ['expliquer', 'détailler', 'pourquoi', 'comment', 'différence', 'comparaison']
        simple_indicators = ['qui', 'que', 'quoi', 'où', 'quand']
        
        if len(question.split()) > 10 or any(word in question_lower for word in complex_indicators):
            return "complex"
        elif any(word in question_lower for word in simple_indicators):
            return "simple"
        else:
            return "medium"
    
    def _reformulate_response_naturally(self, response: str, sentiment: str, complexity: str) -> str:
        """Reformule la réponse de manière plus naturelle"""
        base_response = response.strip()
        
        # Templates selon sentiment et complexité
        natural_templates = {
            "positive": {
                "simple": [
                    f"Je suis ravi de vous aider ! {base_response}",
                    f"Avec plaisir ! {base_response}",
                    f"Excellente question ! {base_response}",
                ],
                "medium": [
                    f"C'est effectivement important de comprendre cela. {base_response}",
                    f"Je vais vous expliquer ça clairement. {base_response}",
                    f"Bonne question ! Laissez-moi vous éclairer : {base_response}",
                ],
                "complex": [
                    f"C'est un sujet passionnant ! Pour bien répondre : {base_response}",
                    f"Excellente question qui mérite une explication détaillée. {base_response}",
                    f"Je comprends votre curiosité sur ce point. Voici ce qu'il faut savoir : {base_response}",
                ]
            },
            "negative": {
                "simple": [
                    f"Je comprends votre préoccupation. {base_response}",
                    f"Pas d'inquiétude, je peux vous aider. {base_response}",
                    f"C'est effectivement embêtant. {base_response}",
                ],
                "medium": [
                    f"Je vois que cela vous pose problème. Laissez-moi vous expliquer : {base_response}",
                    f"C'est frustrant, je comprends. Voici la solution : {base_response}",
                    f"Ne vous inquiétez pas, c'est résolvable. {base_response}",
                ],
                "complex": [
                    f"Je comprends que ce soit complexe et préoccupant. Analysons cela ensemble : {base_response}",
                    f"C'est effectivement un point délicat qui mérite attention. {base_response}",
                    f"Votre préoccupation est légitime. Pour bien comprendre la situation : {base_response}",
                ]
            },
            "neutral": {
                "simple": [
                    f"Bien sûr ! {base_response}",
                    f"Voici la réponse : {base_response}",
                    f"C'est simple : {base_response}",
                ],
                "medium": [
                    f"Laissez-moi vous expliquer. {base_response}",
                    f"C'est une bonne question. {base_response}",
                    f"Voici ce qu'il faut savoir : {base_response}",
                ],
                "complex": [
                    f"C'est une question intéressante qui nécessite quelques explications. {base_response}",
                    f"Pour bien répondre à votre question : {base_response}",
                    f"Laissez-moi vous donner une explication complète : {base_response}",
                ]
            }
        }
        
        templates = natural_templates.get(sentiment, natural_templates["neutral"])
        complexity_templates = templates.get(complexity, templates["medium"])
        
        return random.choice(complexity_templates)
    
    def _add_conversational_elements(self, response: str, question: str, confidence: float) -> str:
        """Ajoute des éléments conversationnels naturels"""
        # Ajout d'incertitude si confiance faible
        if confidence < 0.6:
            uncertainty_phrases = [
                "Si je comprends bien, ",
                "D'après ce que je sais, ",
                "Il me semble que ",
                "Autant que je puisse en juger, ",
            ]
            response = random.choice(uncertainty_phrases) + response.lower()
        
        # Ajout de conclusions naturelles
        ending_phrases = [
            " Cela répond-il à votre question ?",
            " J'espère que c'est clair pour vous !",
            " N'hésitez pas si vous avez besoin de précisions.",
            " Y a-t-il un aspect particulier que vous aimeriez approfondir ?",
            " Dites-moi si quelque chose n'est pas clair.",
            "",  # Parfois pas de conclusion
            "",
        ]
        
        # 60% de chance d'ajouter une conclusion
        if random.random() < 0.6:
            response += random.choice(ending_phrases)
        
        return response
    
    def _add_contextual_continuity(self, response: str, current_question: str) -> str:
        """Ajoute une continuité contextuelle basée sur les questions précédentes"""
        if len(self.conversation_context) == 0:
            return response
        
        last_question = self.conversation_context[-1]
        
        # Détection de continuité thématique simple
        if self._is_related_topic(current_question, last_question):
            continuity_phrases = [
                "Effectivement, pour compléter ma réponse précédente, ",
                "En lien avec ce dont nous parlions, ",
                "Pour continuer sur le même sujet, ",
                "Comme je le mentionnais, ",
            ]
            if random.random() < 0.4:  # 40% de chance d'ajouter la continuité
                response = random.choice(continuity_phrases) + response.lower()
        
        return response
    
    def _is_related_topic(self, current_question: str, previous_question: str) -> bool:
        """Détermine si deux questions sont liées (version simple)"""
        current_words = set(current_question.lower().split())
        previous_words = set(previous_question.lower().split())
        
        # Exclusion des mots vides
        stop_words = {'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou', 'mais', 'est', 'ce', 'que', 'qui', 'comment', 'pourquoi'}
        current_words -= stop_words
        previous_words -= stop_words
        
        # Si plus de 2 mots en commun, considéré comme lié
        common_words = current_words.intersection(previous_words)
        return len(common_words) >= 2
    
    def enhance_response(self, response: str, question: str, confidence: float = 1.0) -> str:
        """Point d'entrée principal pour l'amélioration des réponses"""
        try:
            if self.mode == ResponseMode.MINIMAL:
                return self.enhance_response_minimal(response, question, confidence)
            elif self.mode == ResponseMode.BALANCED:
                return self.enhance_response_balanced(response, question, confidence)
            elif self.mode == ResponseMode.NATURAL:
                return self.enhance_response_natural(response, question, confidence)
            else:
                logger.warning(f"Mode inconnu: {self.mode}, utilisation du mode équilibré")
                return self.enhance_response_balanced(response, question, confidence)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'amélioration de la réponse: {e}")
            return response  # Retour à la réponse originale en cas d'erreur

class AdaptiveResponseSystem:
    """Système adaptatif qui choisit automatiquement le meilleur mode selon les ressources"""
    
    def __init__(self, force_mode: Optional[str] = None):
        self.force_mode = force_mode
        self.current_mode = self._detect_optimal_mode()
        self.enhancer = ResponseEnhancer(self.current_mode)
        logger.info(f"Système de réponse initialisé en mode: {self.current_mode}")
    
    def _detect_optimal_mode(self) -> str:
        """Détecte automatiquement le mode optimal selon les ressources disponibles"""
        if self.force_mode:
            return self.force_mode
        
        try:
            # Test de disponibilité de sentence-transformers
            import sentence_transformers
            # Test de la mémoire disponible (simpliste)
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            
            if memory_gb >= 4:  # Si plus de 4GB de RAM
                return ResponseMode.NATURAL
            else:
                return ResponseMode.BALANCED
                
        except ImportError:
            # sentence-transformers non disponible
            return ResponseMode.BALANCED
        except Exception:
            # Fallback sécurisé
            return ResponseMode.MINIMAL
    
    def switch_mode(self, new_mode: str):
        """Change le mode de réponse à la volée"""
        if new_mode in [ResponseMode.MINIMAL, ResponseMode.BALANCED, ResponseMode.NATURAL]:
            self.current_mode = new_mode
            self.enhancer = ResponseEnhancer(new_mode)
            logger.info(f"Mode de réponse changé vers: {new_mode}")
        else:
            logger.error(f"Mode invalide: {new_mode}")
    
    def get_enhanced_response(self, response: str, question: str, confidence: float = 1.0) -> Dict:
        """Retourne une réponse améliorée avec métadonnées"""
        enhanced_response = self.enhancer.enhance_response(response, question, confidence)
        
        return {
            'response': enhanced_response,
            'original_response': response,
            'mode': self.current_mode,
            'confidence': confidence,
            'question_type': self.enhancer.detect_question_type(question),
            'enhancement_applied': enhanced_response != response,
            'timestamp': datetime.now().isoformat()
        }

# Fonction utilitaire pour l'intégration facile
def create_response_system(mode: Optional[str] = None) -> AdaptiveResponseSystem:
    """Crée un système de réponse adaptatif"""
    return AdaptiveResponseSystem(force_mode=mode)

# Test de démonstration
if __name__ == "__main__":
    # Test des différents modes
    test_question = "Comment ça va ?"
    test_response = "Je vais bien, merci de demander."
    
    for mode in [ResponseMode.MINIMAL, ResponseMode.BALANCED, ResponseMode.NATURAL]:
        print(f"\n--- Mode {mode.upper()} ---")
        system = create_response_system(mode)
        result = system.get_enhanced_response(test_response, test_question, 0.8)
        print(f"Question: {test_question}")
        print(f"Réponse originale: {test_response}")
        print(f"Réponse améliorée: {result['response']}")
        print(f"Métadonnées: {result}")
