#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service de gestion des sessions utilisateur - VERSION CORRIGÉE
Gère l'id_session unique pour chaque conversation
Utilise l'API externe pour le logging

Auteur: Samuel VERSCHUEREN
Date: 16-09-2025
"""

import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SessionService:
    """Service de gestion des sessions utilisateur - CORRIGÉ"""
    
    def __init__(self):
        # Stockage en mémoire des sessions actives
        self._sessions: Dict[str, dict] = {}
        self._session_timeout = 1800  # 30 minutes d'inactivité
        
    def create_session(self) -> str:
        """Créer une nouvelle session avec un ID unique"""
        session_id = f"session_{int(time.time())}_{str(uuid.uuid4())[:8]}"
        
        self._sessions[session_id] = {
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'message_count': 0,
            'total_response_time': 0.0,
            'average_response_time': 0.0
        }
        
        logger.info(f"Nouvelle session créée: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Récupérer les informations d'une session"""
        if session_id in self._sessions:
            session = self._sessions[session_id]
            
            # Vérifier l'expiration
            if self._is_session_expired(session):
                self.end_session(session_id)
                return None
                
            return session
        return None
    
    def update_session_activity(self, session_id: str, response_time_ms: float = 0.0):
        """Mettre à jour l'activité d'une session"""
        if session_id in self._sessions:
            session = self._sessions[session_id]
            session['last_activity'] = datetime.now()
            session['message_count'] += 1
            
            if response_time_ms > 0:
                session['total_response_time'] += response_time_ms
                session['average_response_time'] = session['total_response_time'] / session['message_count']
            
            logger.debug(f"Session {session_id} mise à jour - Messages: {session['message_count']}")
    
    def end_session(self, session_id: str) -> bool:
        """Terminer une session"""
        if session_id in self._sessions:
            session_info = self._sessions[session_id]
            del self._sessions[session_id]
            
            logger.info(f"Session {session_id} terminée - Durée: {session_info['message_count']} messages")
            return True
        return False
    
    def _is_session_expired(self, session: dict) -> bool:
        """Vérifier si une session a expiré"""
        last_activity = session['last_activity']
        expiration_time = last_activity + timedelta(seconds=self._session_timeout)
        return datetime.now() > expiration_time
    
    def cleanup_expired_sessions(self):
        """Nettoyer les sessions expirées"""
        expired_sessions = []
        
        for session_id, session in self._sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.end_session(session_id)
        
        if expired_sessions:
            logger.info(f"Nettoyage de {len(expired_sessions)} sessions expirées")
    
    def get_active_sessions_count(self) -> int:
        """Obtenir le nombre de sessions actives"""
        self.cleanup_expired_sessions()
        return len(self._sessions)
    
    def get_session_stats(self) -> dict:
        """Obtenir les statistiques des sessions"""
        self.cleanup_expired_sessions()
        
        if not self._sessions:
            return {
                'total_sessions': 0,
                'total_messages': 0,
                'average_response_time': 0.0,
                'average_session_duration': 0.0,
                'average_confidence_score': 0.0
            }
        
        total_messages = sum(session['message_count'] for session in self._sessions.values())
        total_response_time = sum(session['total_response_time'] for session in self._sessions.values())
        
        # Calcul de la durée moyenne des sessions
        now = datetime.now()
        session_durations = []
        for session in self._sessions.values():
            duration = (now - session['created_at']).total_seconds()
            session_durations.append(duration)
        
        average_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
        
        return {
            'total_sessions': len(self._sessions),
            'total_messages': total_messages,
            'average_response_time': total_response_time / total_messages if total_messages > 0 else 0.0,
            'average_session_duration': average_session_duration,
            'average_confidence_score': 0.0  # Géré par l'API externe
        }
    
    def is_valid_session(self, session_id: str) -> bool:
        """Vérifier si un ID de session est valide et actif"""
        if not session_id:
            return False
        
        session = self.get_session(session_id)
        return session is not None