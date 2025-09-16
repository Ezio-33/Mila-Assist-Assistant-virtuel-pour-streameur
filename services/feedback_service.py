#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service de gestion des feedbacks utilisateur - VERSION RNCP-6
Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import json
import os
import requests
from datetime import datetime
from typing import Optional, List, Dict
import logging
import threading
from .api_client import ApiClient

logger = logging.getLogger(__name__)

class FeedbackService:
    """Service de gestion des feedbacks utilisateur - VERSION AVEC API FRANÇAISE"""
    
    def __init__(self, config):
        self.config = config
        self.feedback_local_path = os.path.join(config.BASE_DIR, "data", "user_feedback.json")
        
        # Initialiser le client API
        self.api_client = ApiClient(config)
        
        # Créer le répertoire data s'il n'existe pas
        os.makedirs(os.path.dirname(self.feedback_local_path), exist_ok=True)
        
        # Statistiques de debugging
        self.stats = {
            'feedbacks_envoyes': 0,
            'feedbacks_success': 0,
            'feedbacks_failed': 0,
            'feedbacks_api_success': 0,
            'feedbacks_local_fallback': 0
        }
        
        logger.info("✅ Service feedback initialisé avec API française")
        
    def soumettre_feedback(self, question: str, reponse_attendue: str, reponse_actuelle: str = "") -> bool:
        """Soumettre un feedback utilisateur via l'API française"""
        try:
            logger.info(f"📝 Soumission feedback via API française: {question[:50]}...")
            
            # Essayer d'abord via l'API française
            success_api = self._soumettre_feedback_api(question, reponse_attendue, reponse_actuelle)
            if success_api:
                self.stats['feedbacks_api_success'] += 1
                self.stats['feedbacks_success'] += 1
                logger.info("✅ Feedback envoyé avec succès via API française")
                return True
            else:
                # Fallback vers stockage local
                logger.warning("⚠️ API feedback indisponible, fallback vers stockage local")
                success_local = self._sauvegarder_feedback_local(question, reponse_attendue, reponse_actuelle)
                if success_local:
                    self.stats['feedbacks_local_fallback'] += 1
                    self.stats['feedbacks_success'] += 1
                    logger.info("✅ Feedback sauvegardé localement (fallback)")
                    return True
                else:
                    self.stats['feedbacks_failed'] += 1
                    return False
        except Exception as e:
            logger.error(f"Erreur soumission feedback: {e}")
            self.stats['feedbacks_failed'] += 1
            return False
            
        except Exception as e:
            logger.error(f"Erreur lors de la soumission du feedback: {e}")
            self.stats['feedbacks_failed'] += 1
            return False
        finally:
            self.stats['feedbacks_envoyes'] += 1
    
    def _soumettre_feedback_api(self, question: str, reponse_attendue: str, reponse_actuelle: str) -> bool:
        """Soumettre le feedback via l'API française"""
        try:
            # Utiliser le client API français
            success = self.api_client.soumettre_feedback(question, reponse_attendue, reponse_actuelle)
            return success
        except Exception as e:
            logger.error(f"Erreur soumission feedback API: {e}")
            return False
    
    def _sauvegarder_feedback_local(self, question: str, reponse_attendue: str, reponse_actuelle: str) -> bool:
        """Sauvegarder le feedback localement"""
        try:
            # Charger les feedbacks existants
            feedbacks = self._charger_feedbacks_locaux()
            
            # Nouveau feedback avec toutes les nomenclatures pour compatibilité future
            nouveau_feedback = {
                'question': question,
                'expected_response': reponse_attendue,
                'current_response': reponse_actuelle,
                'reponse_attendue': reponse_attendue,  # Nomenclature française
                'reponse_donnee': reponse_actuelle,    # Nomenclature française
                'statut': 'local_seulement',
                'priorite': 'moyenne',
                'date_creation': datetime.now().isoformat(),
                'source': 'app_local',
                'api_status': 'erreur_500'  # Marquer pourquoi c'est local
            }
            
            feedbacks.append(nouveau_feedback)
            
            # Sauvegarder
            with open(self.feedback_local_path, 'w', encoding='utf-8') as f:
                json.dump(feedbacks, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Feedback local sauvegardé: {len(feedbacks)} total")
            return True
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde feedback local: {e}")
            return False
    
    def _charger_feedbacks_locaux(self) -> List[Dict]:
        """Charger les feedbacks stockés localement"""
        try:
            if os.path.exists(self.feedback_local_path):
                with open(self.feedback_local_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Erreur chargement feedbacks: {e}")
            return []
    
    def synchroniser_feedbacks_locaux(self) -> bool:
        """Synchronisation désactivée (API en erreur)"""
        logger.warning("🚫 Synchronisation désactivée - API feedback en erreur 500")
        return False
    
    def obtenir_statistiques_feedbacks(self) -> Dict:
        """Obtenir les statistiques des feedbacks"""
        try:
            feedbacks = self._charger_feedbacks_locaux()
            
            total = len(feedbacks)
            local_seulement = len([f for f in feedbacks if f.get('statut') == 'local_seulement'])
            
            return {
                'total_feedbacks': total,
                'mode': 'LOCAL_SEULEMENT',
                'statuts': {
                    'local_seulement': local_seulement,
                    'api_erreur': total - local_seulement
                },
                'api_status': 'ERREUR_500',
                'stats_envoi': self.stats,
                'message': 'Feedbacks stockés localement uniquement (API indisponible)'
            }
            
        except Exception as e:
            logger.error(f"Erreur statistiques feedbacks: {e}")
            return {
                'total_feedbacks': 0,
                'mode': 'LOCAL_SEULEMENT',
                'api_status': 'ERREUR_500',
                'stats_envoi': self.stats,
                'message': 'Erreur de lecture des feedbacks locaux'
            }
    
    def nettoyer_feedbacks_anciens(self, jours: int = 30) -> int:
        """Nettoyer les feedbacks anciens"""
        try:
            feedbacks = self._charger_feedbacks_locaux()
            feedbacks_initiaux = len(feedbacks)
            
            from datetime import timedelta
            date_limite = datetime.now() - timedelta(days=jours)
            
            # Garder seulement les feedbacks récents
            feedbacks_filtres = []
            for feedback in feedbacks:
                try:
                    date_creation = datetime.fromisoformat(
                        feedback.get('date_creation', feedback.get('timestamp', ''))
                    )
                    if date_creation > date_limite:
                        feedbacks_filtres.append(feedback)
                except:
                    # Garder en cas d'erreur de parsing
                    feedbacks_filtres.append(feedback)
            
            # Sauvegarder si des changements
            if len(feedbacks_filtres) != feedbacks_initiaux:
                with open(self.feedback_local_path, 'w', encoding='utf-8') as f:
                    json.dump(feedbacks_filtres, f, ensure_ascii=False, indent=2)
                
                supprimes = feedbacks_initiaux - len(feedbacks_filtres)
                logger.info(f"🧹 Nettoyage: {supprimes} anciens feedbacks supprimés")
                return supprimes
            
            return 0
            
        except Exception as e:
            logger.error(f"Erreur nettoyage feedbacks: {e}")
            return 0
    
    def test_feedback_api(self) -> bool:
        """Test de l'API feedback (pour confirmer l'erreur 500)"""
        try:
            url = f"{self.config.API_URL}/feedback"
            payload = {
                'question': 'Test API',
                'expected_response': 'Test',
                'current_response': 'Test'
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=self.config.get_api_headers(),
                timeout=5,
                verify=False
            )
            
            logger.info(f"🔍 Test API feedback: {response.status_code}")
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Test feedback API échoué: {e}")
            return False
    
    def export_feedbacks_for_manual_import(self) -> str:
        """Exporter les feedbacks pour import manuel dans la base"""
        try:
            feedbacks = self._charger_feedbacks_locaux()
            
            # Créer un fichier SQL pour import manuel
            export_file = os.path.join(
                os.path.dirname(self.feedback_local_path), 
                f"feedbacks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            )
            
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write("-- Feedbacks à importer manuellement dans retours_utilisateur\n")
                f.write("-- Générés le " + datetime.now().isoformat() + "\n\n")
                
                for feedback in feedbacks:
                    question = feedback.get('question', '').replace("'", "''")
                    reponse_donnee = feedback.get('current_response', '').replace("'", "''")
                    reponse_attendue = feedback.get('expected_response', '').replace("'", "''")
                    date_creation = feedback.get('date_creation', datetime.now().isoformat())
                    
                    sql = f"""INSERT INTO retours_utilisateur (question, reponse_donnee, reponse_attendue, statut, priorite, date_creation, commentaire_admin) 
VALUES ('{question}', '{reponse_donnee}', '{reponse_attendue}', 'nouveau', 'moyenne', '{date_creation}', 'Import manuel depuis app locale');
"""
                    f.write(sql)
            
            logger.info(f"📄 Export SQL créé: {export_file}")
            return export_file
            
        except Exception as e:
            logger.error(f"Erreur export feedbacks: {e}")
            return ""
    
    def demarrer_synchronisation_automatique(self):
        """Synchronisation désactivée"""
        logger.warning("🚫 Synchronisation automatique désactivée (API indisponible)")
        pass