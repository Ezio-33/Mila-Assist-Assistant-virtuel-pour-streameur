#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic complet pour l'API française refactorisée V2.0
Teste tous les endpoints incluant les nouvelles routes françaises spécialisées
Architecture 100% française avec nomenclature complète
"""

import requests
import json
import os
from datetime import datetime
import time
from dotenv import load_dotenv

# Charger la configuration depuis .env
load_dotenv()

# Configuration sécurisée depuis les variables d'environnement
API_URL = os.getenv('API_URL', 'http://localhost:5000/api')
API_KEY = os.getenv('API_KEY', 'your-api-key-here')

def get_headers():
    """Obtenir les headers pour l'API"""
    return {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
    }

def test_api_health():
    """Test 1: Vérifier que l'API répond"""
    print("🔍 TEST 1: Health check de l'API")
    try:
        url = f"{API_URL}/health"
        print(f"   URL: {url}")
        
        response = requests.get(url, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:200]}")
        
        if response.status_code == 200:
            print("   ✅ API accessible")
            return True
        else:
            print("   ❌ API non accessible")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_chat_endpoint():
    """Test 2: Tester l'endpoint chat"""
    print("\n🔍 TEST 2: Endpoint chat")
    try:
        url = f"{API_URL}/chat"
        payload = {
            'message': 'Test de diagnostic',
            'session_id': f'debug_session_{int(time.time())}',
            'threshold': 0.7
        }
        
        print(f"   URL: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Chat endpoint fonctionne")
                return data
            else:
                print("   ❌ Chat endpoint répond mais pas de succès")
                return None
        else:
            print("   ❌ Chat endpoint ne fonctionne pas")
            return None
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return None

def test_conversation_logging(session_id, question, reponse):
    """Test 3: Tester l'endpoint /api/journal_conversation (NOUVEAU)"""
    print("\n🔍 TEST 3: Endpoint journal_conversation (Nomenclature française)")
    try:
        url = f"{API_URL}/journal_conversation"
        payload = {
            'id_session': session_id,
            'question': question,
            'reponse': reponse,
            'id_connaissance': 1,  # Test avec une connaissance
            'score_confiance': 0.85,
            'temps_reponse_ms': 125.7
        }
        
        print(f"   URL: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Conversation enregistrée avec succès")
                print(f"   ID conversation: {data.get('conversation_id')}")
                return True
            else:
                print(f"   ❌ Erreur enregistrement: {data.get('error')}")
                return False
        else:
            print("   ❌ Endpoint journal_conversation ne fonctionne pas")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False



def test_feedback_endpoint():
    """Test 4: Tester l'endpoint feedback (Version française)"""
    print("\n🔍 TEST 4: Endpoint feedback (Version 100% française)")
    try:
        url = f"{API_URL}/feedback"
        payload = {
            'question': 'Question de test diagnostic après refactoring français',
            'expected_response': 'Réponse attendue pour tester la nouvelle API 100% française',
            'current_response': 'Réponse actuelle générée par le système refactorisé'
        }
        
        print(f"   URL: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Feedback enregistré avec succès (table retours_utilisateur)")
                return True
            else:
                print(f"   ❌ Erreur feedback: {data.get('error')}")
                return False
        else:
            print("   ❌ Endpoint feedback ne fonctionne pas")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_knowledge_endpoint():
    """Test 5: Tester l'endpoint knowledge (Version française)"""
    print("\n🔍 TEST 5: Endpoint knowledge (Version 100% française)")
    try:
        url = f"{API_URL}/knowledge"
        timestamp = int(time.time())
        payload = {
            'tag': f'test_diagnostic_{timestamp}',
            'question': f'Comment tester la nouvelle API française ? Test {timestamp}',
            'response': 'La nouvelle API fonctionne parfaitement avec tous les endpoints français et utilise uniquement les tables françaises.',
            'metadata': {
                'source': 'test_diagnostic_complet',
                'priority': 'high',
                'version': '2.0.0-FR',
                'timestamp': timestamp
            }
        }
        
        print(f"   URL: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Connaissance ajoutée avec succès (table base_connaissances)")
                return True
            else:
                print(f"   ❌ Erreur knowledge: {data.get('error')}")
                return False
        else:
            print("   ❌ Endpoint knowledge ne fonctionne pas")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_process_feedbacks_endpoint():
    """Test 6: Tester l'endpoint process-feedbacks (Traitement des feedbacks)"""
    print("\n🔍 TEST 6: Endpoint process-feedbacks (Traitement automatique)")
    try:
        url = f"{API_URL}/process-feedbacks"
        payload = {
            'auto_process': True,
            'max_feedbacks': 10
        }
        
        print(f"   URL: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, headers=get_headers(), timeout=15, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Feedbacks traités: {data.get('processed', 0)} feedbacks")
                return True
            else:
                print(f"   ❌ Erreur traitement: {data.get('error')}")
                return False
        else:
            print("   ❌ Endpoint process-feedbacks ne fonctionne pas")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_search_endpoint():
    """Test 7: Tester l'endpoint search (Recherche dans la base de connaissances)"""
    print("\n🔍 TEST 7: Endpoint search (Recherche sémantique)")
    try:
        url = f"{API_URL}/search"
        payload = {
            'query': 'test diagnostic API française',
            'top_k': 5,
            'threshold': 0.3
        }
        
        print(f"   URL: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:400]}...")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                count = data.get('count', 0)
                print(f"   ✅ Recherche effectuée: {count} résultats trouvés")
                if count > 0:
                    results = data.get('results', [])
                    print(f"   📋 Premier résultat: {results[0].get('question', 'N/A')[:50]}...")
                return True
            else:
                print(f"   ❌ Erreur search: {data.get('error')}")
                return False
        else:
            print("   ❌ Endpoint search ne fonctionne pas")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_stats_endpoint():
    """Test 8: Vérifier les stats avec nomenclature française"""
    print("\n🔍 TEST 8: Statistiques avec nomenclature française")
    try:
        url = f"{API_URL}/stats"
        
        response = requests.get(url, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('stats', {})
            
            # Statistiques françaises
            conv_stats = stats.get('conversations_francaises', {})
            print("   ✅ Statistiques récupérées (nomenclature française):")
            print(f"   Total conversations: {conv_stats.get('total_conversations', 0)}")
            print(f"   Sessions uniques: {conv_stats.get('sessions_uniques', 0)}")
            print(f"   Confiance moyenne: {conv_stats.get('confiance_moyenne', 0):.2f}")
            print(f"   Temps réponse moyen: {conv_stats.get('temps_reponse_moyen_ms', 0):.2f}ms")
            
            # Base de connaissances
            kb_stats = stats.get('base_connaissances', {})
            print(f"   Total connaissances: {kb_stats.get('total_entries', 0)}")
            print(f"   Utilisations totales: {kb_stats.get('total_utilisations', 0)}")
            
            # Feedbacks
            feedback_stats = stats.get('retours_utilisateur', {})
            print(f"   Total feedbacks: {sum(feedback_stats.values()) if feedback_stats else 0}")
            
            return stats
        else:
            print("   ❌ Impossible de récupérer les stats")
            return None
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return None

def test_security_status():
    """Test 8: Tester l'endpoint security-status (Sécurité administrative)"""
    print("\n🔍 TEST 8: Endpoint security-status (Statut de sécurité)")
    try:
        url = f"{API_URL}/security-status"
        
        response = requests.get(url, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:300]}...")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                security = data.get('security_status', {})
                print("   ✅ Statut de sécurité récupéré:")
                print(f"   IPs bloquées: {security.get('total_blocked_ips', 0)}")
                print(f"   IPs en alerte: {security.get('total_warning_ips', 0)}")
                print(f"   Tentatives max: {security.get('max_attempts_before_block', 0)}")
                print(f"   Durée blocage: {security.get('block_duration_seconds', 0)}s")
                return True
            else:
                print(f"   ❌ Erreur security: {data.get('error')}")
                return False
        else:
            print("   ❌ Endpoint security-status ne fonctionne pas")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_nouvelles_routes_francaises():
    """Test 10-13: Tester les nouvelles routes françaises spécialisées"""
    print("\n🔹 Phase 6: Test des nouvelles routes françaises")
    
    results = {}
    
    # Test 10: /api/fr/connaissances (GET - Liste)
    print("\n🔍 TEST 10: Endpoint fr/connaissances (Liste des connaissances)")
    try:
        url = f"{API_URL}/fr/connaissances"
        response = requests.get(url, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                connaissances = data.get('connaissances', [])
                print(f"   ✅ Connaissances françaises récupérées: {len(connaissances)} entrées")
                if len(connaissances) > 0:
                    print(f"   📋 Exemple: {connaissances[0].get('question', 'N/A')[:50]}...")
                results['fr_connaissances_get'] = True
            else:
                print(f"   ❌ Erreur: {data.get('error')}")
                results['fr_connaissances_get'] = False
        else:
            print(f"   ❌ Erreur HTTP: {response.text[:200]}")
            results['fr_connaissances_get'] = False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        results['fr_connaissances_get'] = False
    
    # Test 11: /api/fr/connaissances (POST - Ajout)
    print("\n🔍 TEST 11: Endpoint fr/connaissances (Ajout de connaissance)")
    try:
        url = f"{API_URL}/fr/connaissances"
        timestamp = int(time.time())
        payload = {
            'tag': f'test_fr_route_{timestamp}',
            'question': f'Test route française - Comment ça marche ? {timestamp}',
            'response': 'Les nouvelles routes françaises permettent une gestion complète des données avec une nomenclature française.',
            'metadata': {
                'source': 'test_routes_francaises',
                'version': '2.0.0-FR-PLUS',
                'timestamp': timestamp
            }
        }
        
        response = requests.post(url, json=payload, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Connaissance ajoutée via route française")
                results['fr_connaissances_post'] = True
            else:
                print(f"   ❌ Erreur: {data.get('error')}")
                results['fr_connaissances_post'] = False
        else:
            print(f"   ❌ Erreur HTTP: {response.text[:200]}")
            results['fr_connaissances_post'] = False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        results['fr_connaissances_post'] = False
    
    # Test 12: /api/fr/conversations (GET - Liste)
    print("\n🔍 TEST 12: Endpoint fr/conversations (Liste des conversations)")
    try:
        url = f"{API_URL}/fr/conversations"
        params = {'limit': 10, 'page': 1}
        response = requests.get(url, headers=get_headers(), params=params, timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                conversations = data.get('conversations', [])
                pagination = data.get('pagination', {})
                print(f"   ✅ Conversations françaises récupérées: {len(conversations)} entrées")
                print(f"   📊 Total: {pagination.get('total', 0)}, Pages: {pagination.get('pages', 0)}")
                results['fr_conversations'] = True
            else:
                print(f"   ❌ Erreur: {data.get('error')}")
                results['fr_conversations'] = False
        else:
            print(f"   ❌ Erreur HTTP: {response.text[:200]}")
            results['fr_conversations'] = False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        results['fr_conversations'] = False
    
    # Test 13: /api/fr/feedbacks (GET - Liste)
    print("\n🔍 TEST 13: Endpoint fr/feedbacks (Liste des feedbacks)")
    try:
        url = f"{API_URL}/fr/feedbacks"
        params = {'limit': 10, 'page': 1}
        response = requests.get(url, headers=get_headers(), params=params, timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                feedbacks = data.get('feedbacks', [])
                pagination = data.get('pagination', {})
                print(f"   ✅ Feedbacks français récupérés: {len(feedbacks)} entrées")
                print(f"   📊 Total: {pagination.get('total', 0)}, Pages: {pagination.get('pages', 0)}")
                results['fr_feedbacks'] = True
            else:
                print(f"   ❌ Erreur: {data.get('error')}")
                results['fr_feedbacks'] = False
        else:
            print(f"   ❌ Erreur HTTP: {response.text[:200]}")
            results['fr_feedbacks'] = False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        results['fr_feedbacks'] = False
    
    # Test 14: /api/fr/statistiques (GET - Statistiques détaillées)
    print("\n🔍 TEST 14: Endpoint fr/statistiques (Statistiques françaises détaillées)")
    try:
        url = f"{API_URL}/fr/statistiques"
        response = requests.get(url, headers=get_headers(), timeout=10, verify=False)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                stats = data.get('statistiques', {})
                print("   ✅ Statistiques françaises détaillées récupérées:")
                
                # Conversations
                conv_stats = stats.get('conversations', {})
                print(f"   📊 Conversations: {conv_stats.get('total', 0)} total, {conv_stats.get('sessions_uniques', 0)} sessions")
                print(f"       Confiance: {conv_stats.get('confiance_moyenne', 0):.2f}, Temps: {conv_stats.get('temps_reponse_moyen_ms', 0):.1f}ms")
                
                # Connaissances  
                kb_stats = stats.get('connaissances', {})
                print(f"   🧠 Connaissances: {kb_stats.get('total', 0)} total, {kb_stats.get('tags_uniques', 0)} tags uniques")
                print(f"       Utilisations: {kb_stats.get('utilisations_totales', 0)}, Seuil: {kb_stats.get('seuil_confiance_moyen', 0):.2f}")
                
                # Feedbacks
                feedback_stats = stats.get('feedbacks', {})
                total_feedbacks = sum(feedback_stats.values()) if feedback_stats else 0
                print(f"   💭 Feedbacks: {total_feedbacks} total ({feedback_stats})")
                
                # Top tags
                top_tags = stats.get('top_tags', [])
                if top_tags:
                    tag_names = [tag['tag'] for tag in top_tags[:3]]
                    print(f"   🏷️ Top tags: {', '.join(tag_names)}")
                
                results['fr_statistiques'] = True
            else:
                print(f"   ❌ Erreur: {data.get('error')}")
                results['fr_statistiques'] = False
        else:
            print(f"   ❌ Erreur HTTP: {response.text[:200]}")
            results['fr_statistiques'] = False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        results['fr_statistiques'] = False
    
    return results

def test_invalid_endpoints():
    """Test 15: Tester des endpoints non valides (Test de robustesse)"""
    print("\n🔍 TEST 15: Endpoints non valides (Test de robustesse)")
    invalid_endpoints = [
        '/api/sessions',  # Supprimé dans la refactorisation
        '/api/nonexistent',  # N'existe pas
        '/api/admin',  # N'existe pas
        '/api/invalid',  # N'existe pas
        '/api/fr/inexistant'  # Route française inexistante
    ]
    
    valid_404_count = 0
    total_tests = len(invalid_endpoints)
    
    for endpoint in invalid_endpoints:
        try:
            url = f"{API_URL}{endpoint}"
            response = requests.get(url, headers=get_headers(), timeout=5, verify=False)
            if response.status_code == 404:
                valid_404_count += 1
                print(f"   ✅ {endpoint} → 404 (correct)")
            else:
                print(f"   ⚠️ {endpoint} → {response.status_code} (inattendu)")
        except Exception as e:
            print(f"   ❌ {endpoint} → Erreur: {e}")
    
    success_rate = (valid_404_count / total_tests) * 100
    print(f"   📊 Robustesse: {valid_404_count}/{total_tests} endpoints retournent 404 correctement ({success_rate:.1f}%)")
    
    return success_rate >= 75

def test_complet():
    """Lancer tous les tests dans l'ordre pour l'API française refactorisée avec nouvelles routes"""
    print("🚀 DIAGNOSTIC COMPLET DE L'API FRANÇAISE COMPLÈTE V2.0")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Health check
    print("🔹 Phase 1: Vérification de l'accessibilité")
    results['health'] = test_api_health()
    if not results['health']:
        print("\n❌ DIAGNOSTIC ARRÊTÉ: API non accessible")
        return False
    
    # Test 2: Chat endpoint
    print("\n🔹 Phase 2: Test des fonctionnalités de base")
    chat_response = test_chat_endpoint()
    results['chat'] = chat_response is not None
    if not results['chat']:
        print("\n❌ DIAGNOSTIC ARRÊTÉ: Chat endpoint ne fonctionne pas")
        return False
    
    # Test 3: Enregistrement conversation (Nomenclature française)
    print("\n🔹 Phase 3: Test des endpoints français de logging")
    session_id = f'debug_session_{int(time.time())}'
    question = "Test de diagnostic complet de la nouvelle API française avec routes complètes"
    reponse = chat_response.get('response', 'Réponse de test')
    
    results['conversation_logging'] = test_conversation_logging(session_id, question, reponse)
    
    # Test 4-7: Endpoints métier français
    print("\n🔹 Phase 4: Test des endpoints métier français")
    results['feedback'] = test_feedback_endpoint()
    results['knowledge'] = test_knowledge_endpoint()
    results['process_feedbacks'] = test_process_feedbacks_endpoint()
    results['search'] = test_search_endpoint()
    
    # Test 8-9: Administration
    print("\n🔹 Phase 5: Vérification des données et administration")
    final_stats = test_stats_endpoint()
    results['stats'] = final_stats is not None
    results['security'] = test_security_status()
    
    # Test 10-14: Nouvelles routes françaises
    nouvelles_routes_results = test_nouvelles_routes_francaises()
    results.update(nouvelles_routes_results)
    
    # Test 15: Robustesse des endpoints
    print("\n🔹 Phase 7: Tests de robustesse")
    results['robustesse'] = test_invalid_endpoints()
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📋 RÉSUMÉ COMPLET DU DIAGNOSTIC DE L'API FRANÇAISE COMPLÈTE")
    print("=" * 70)
    
    print("\n🔹 ENDPOINTS DE BASE:")
    print(f"   Health check:     {'✅ OK' if results['health'] else '❌ ÉCHEC'}")
    print(f"   Chat:             {'✅ OK' if results['chat'] else '❌ ÉCHEC'}")
    print(f"   Statistiques:     {'✅ OK' if results['stats'] else '❌ ÉCHEC'}")
    
    print("\n🔹 ENDPOINTS FRANÇAIS DE LOGGING:")
    print(f"   Journal conversation: {'✅ OK' if results['conversation_logging'] else '❌ ÉCHEC'}")
    
    print("\n🔹 ENDPOINTS MÉTIER FRANÇAIS:")
    print(f"   Feedback:             {'✅ OK' if results['feedback'] else '❌ ÉCHEC'}")
    print(f"   Base connaissances:   {'✅ OK' if results['knowledge'] else '❌ ÉCHEC'}")
    print(f"   Traitement feedbacks: {'✅ OK' if results['process_feedbacks'] else '❌ ÉCHEC'}")
    print(f"   Recherche:            {'✅ OK' if results['search'] else '❌ ÉCHEC'}")
    
    print("\n🔹 NOUVELLES ROUTES FRANÇAISES:")
    print(f"   fr/connaissances GET: {'✅ OK' if results.get('fr_connaissances_get') else '❌ ÉCHEC'}")
    print(f"   fr/connaissances POST:{'✅ OK' if results.get('fr_connaissances_post') else '❌ ÉCHEC'}")
    print(f"   fr/conversations:     {'✅ OK' if results.get('fr_conversations') else '❌ ÉCHEC'}")
    print(f"   fr/feedbacks:         {'✅ OK' if results.get('fr_feedbacks') else '❌ ÉCHEC'}")
    print(f"   fr/statistiques:      {'✅ OK' if results.get('fr_statistiques') else '❌ ÉCHEC'}")
    
    print("\n🔹 ENDPOINTS ADMINISTRATIFS:")
    print(f"   Sécurité:             {'✅ OK' if results['security'] else '❌ ÉCHEC'}")
    
    print("\n🔹 TESTS DE ROBUSTESSE:")
    print(f"   Endpoints invalides:  {'✅ OK' if results['robustesse'] else '❌ ÉCHEC'}")
    
    # Analyse des données
    if final_stats:
        conv_stats = final_stats.get('conversations_francaises', {})
        print(f"\n🔹 DONNÉES EN BASE (NOMENCLATURE FRANÇAISE):")
        print(f"   Conversations:    {conv_stats.get('total_conversations', 0)}")
        print(f"   Sessions:         {conv_stats.get('sessions_uniques', 0)}")
        
        kb_stats = final_stats.get('base_connaissances', {})
        print(f"   Connaissances:    {kb_stats.get('total_entries', 0)}")
        
        feedback_stats = final_stats.get('retours_utilisateur', {})
        total_feedbacks = sum(feedback_stats.values()) if feedback_stats else 0
        print(f"   Feedbacks:        {total_feedbacks}")
    
    # Score final détaillé
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    success_rate = (passed_tests / total_tests) * 100
    
    # Score par catégorie
    base_endpoints = ['health', 'chat', 'stats']
    base_score = sum(1 for k in base_endpoints if results.get(k)) / len(base_endpoints) * 100
    
    fr_endpoints = ['conversation_logging', 'feedback', 'knowledge', 'search']
    fr_score = sum(1 for k in fr_endpoints if results.get(k)) / len(fr_endpoints) * 100
    
    nouvelles_routes = ['fr_connaissances_get', 'fr_connaissances_post', 'fr_conversations', 'fr_feedbacks', 'fr_statistiques']
    nouvelles_score = sum(1 for k in nouvelles_routes if results.get(k)) / len(nouvelles_routes) * 100
    
    print(f"\n🎯 SCORES DÉTAILLÉS:")
    print(f"   📊 Score global:              {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    print(f"   🔧 Endpoints de base:         {base_score:.1f}%")
    print(f"   🇫🇷 Endpoints français:        {fr_score:.1f}%")
    print(f"   ✨ Nouvelles routes françaises: {nouvelles_score:.1f}%")
    
    # Évaluation finale
    if success_rate >= 95:
        print("\n🎉 PARFAIT: Votre API française complète est entièrement fonctionnelle!")
        print("   ✨ Architecture 100% française réussie avec toutes les fonctionnalités")
        print("   🚀 Prêt pour la production avec nomenclature française complète")
    elif success_rate >= 85:
        print("\n🎉 EXCELLENT: Votre API française fonctionne très bien!")
        print("   ✅ La migration vers l'architecture française est largement réussie")
        print("   🔧 Quelques ajustements mineurs possibles")
    elif success_rate >= 70:
        print("\n✅ BIEN: Votre API fonctionne globalement bien")
        print("   🔧 Quelques endpoints peuvent nécessiter des corrections")
        print("   📈 La base française est solide")
    elif success_rate >= 50:
        print("\n⚠️ MOYEN: Certains endpoints ont des problèmes")
        print("   🚨 La migration française nécessite des corrections importantes")
    else:
        print("\n❌ CRITIQUE: Plusieurs endpoints ne fonctionnent pas")
        print("   🆘 Révision complète de l'architecture française nécessaire")
    
    # Recommandations spécialisées
    print(f"\n💡 RECOMMANDATIONS TECHNIQUES:")
    if not results.get('knowledge'):
        print("   🔧 Vérifiez la table base_connaissances et la méthode _ajouter_connaissance_francaise")
    if not results.get('feedback'):
        print("   🔧 Vérifiez la table retours_utilisateur et la méthode _sauvegarder_feedback_francais")
    if not results.get('process_feedbacks'):
        print("   � Implémentez complètement l'endpoint /api/process-feedbacks")
    if not results.get('fr_connaissances_get'):
        print("   🔧 Vérifiez l'endpoint /api/fr/connaissances (GET) et les requêtes SQL")
    if nouvelles_score < 80:
        print("   🔧 Les nouvelles routes françaises nécessitent une attention particulière")
    if base_score == 100 and fr_score >= 75:
        print("   ✅ Excellente base ! Focus sur l'optimisation des routes françaises")
    
    return success_rate >= 70

if __name__ == "__main__":
    print("Configuration utilisée:")
    print(f"API_URL: {API_URL}")
    print(f"API_KEY: {API_KEY[:20]}...")
    print()
    
    test_complet()