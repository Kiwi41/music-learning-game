"""Tests pour la persistance des données"""
import pytest
import sys
import os
import tempfile
import json

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import music_game
from music_game import NOTES


class TestPersistanceDonnees:
    """Tests de sauvegarde et chargement des données"""
    
    def test_charger_donnees_fichier_inexistant(self):
        """Vérifie que charger_donnees() retourne une structure par défaut si le fichier n'existe pas"""
        # Utiliser un fichier temporaire qui n'existe pas
        with tempfile.TemporaryDirectory() as tmpdir:
            fichier_temp = os.path.join(tmpdir, 'inexistant.json')
            music_game.FICHIER_DONNEES = fichier_temp
            
            donnees = music_game.charger_donnees()
            
            # Vérifier la structure par défaut
            assert 'high_score' in donnees
            assert donnees['high_score'] == 0
            assert 'stats' in donnees
            assert 'total_notes' in donnees['stats']
            assert 'notes_correctes' in donnees['stats']
            assert 'sessions' in donnees['stats']
            assert 'par_note' in donnees['stats']
    
    def test_charger_donnees_structure_par_note(self):
        """Vérifie que chaque note a une structure de stats"""
        with tempfile.TemporaryDirectory() as tmpdir:
            fichier_temp = os.path.join(tmpdir, 'test.json')
            music_game.FICHIER_DONNEES = fichier_temp
            
            donnees = music_game.charger_donnees()
            
            for note in NOTES:
                assert note in donnees['stats']['par_note']
                assert 'tentatives' in donnees['stats']['par_note'][note]
                assert 'reussites' in donnees['stats']['par_note'][note]
                assert donnees['stats']['par_note'][note]['tentatives'] == 0
                assert donnees['stats']['par_note'][note]['reussites'] == 0
    
    def test_sauvegarder_et_charger_donnees(self):
        """Vérifie que les données sauvegardées peuvent être rechargées"""
        with tempfile.TemporaryDirectory() as tmpdir:
            fichier_temp = os.path.join(tmpdir, 'test.json')
            music_game.FICHIER_DONNEES = fichier_temp
            
            # Créer des données de test
            donnees_test = {
                'high_score': 150,
                'stats': {
                    'total_notes': 50,
                    'notes_correctes': 40,
                    'sessions': 5,
                    'par_note': {
                        note: {'tentatives': 7, 'reussites': 5}
                        for note in NOTES
                    }
                }
            }
            
            # Sauvegarder
            music_game.sauvegarder_donnees(donnees_test)
            
            # Recharger
            donnees_chargees = music_game.charger_donnees()
            
            # Vérifier que les données sont identiques
            assert donnees_chargees['high_score'] == 150
            assert donnees_chargees['stats']['total_notes'] == 50
            assert donnees_chargees['stats']['notes_correctes'] == 40
            assert donnees_chargees['stats']['sessions'] == 5
            
            for note in NOTES:
                assert donnees_chargees['stats']['par_note'][note]['tentatives'] == 7
                assert donnees_chargees['stats']['par_note'][note]['reussites'] == 5
    
    def test_sauvegarder_donnees_format_json(self):
        """Vérifie que les données sont sauvegardées en JSON valide"""
        with tempfile.TemporaryDirectory() as tmpdir:
            fichier_temp = os.path.join(tmpdir, 'test.json')
            music_game.FICHIER_DONNEES = fichier_temp
            
            donnees_test = {
                'high_score': 100,
                'stats': {
                    'total_notes': 20,
                    'notes_correctes': 15,
                    'sessions': 2,
                    'par_note': {note: {'tentatives': 3, 'reussites': 2} for note in NOTES}
                }
            }
            
            music_game.sauvegarder_donnees(donnees_test)
            
            # Lire directement le fichier JSON
            with open(fichier_temp, 'r', encoding='utf-8') as f:
                contenu = json.load(f)
            
            assert contenu == donnees_test
    
    def test_charger_donnees_json_corrompu(self):
        """Vérifie que charger_donnees() gère un fichier JSON corrompu"""
        with tempfile.TemporaryDirectory() as tmpdir:
            fichier_temp = os.path.join(tmpdir, 'corrompu.json')
            music_game.FICHIER_DONNEES = fichier_temp
            
            # Créer un fichier JSON invalide
            with open(fichier_temp, 'w') as f:
                f.write("{ invalid json }")
            
            # Devrait retourner la structure par défaut sans crasher
            donnees = music_game.charger_donnees()
            
            assert donnees['high_score'] == 0
            assert 'stats' in donnees
    
    def test_format_donnees_lisible(self):
        """Vérifie que le JSON est formaté de manière lisible (avec indentation)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            fichier_temp = os.path.join(tmpdir, 'test.json')
            music_game.FICHIER_DONNEES = fichier_temp
            
            donnees_test = {
                'high_score': 50,
                'stats': {
                    'total_notes': 10,
                    'notes_correctes': 8,
                    'sessions': 1,
                    'par_note': {'Do': {'tentatives': 2, 'reussites': 1}}
                }
            }
            
            music_game.sauvegarder_donnees(donnees_test)
            
            # Lire le contenu brut
            with open(fichier_temp, 'r') as f:
                contenu = f.read()
            
            # Vérifier qu'il y a de l'indentation (fichier formaté)
            assert '\n' in contenu
            assert '  ' in contenu  # Indentation présente
    
    def test_accents_preserves(self):
        """Vérifie que les accents sont préservés dans le JSON"""
        with tempfile.TemporaryDirectory() as tmpdir:
            fichier_temp = os.path.join(tmpdir, 'test.json')
            music_game.FICHIER_DONNEES = fichier_temp
            
            # Créer des données avec accents
            donnees_test = music_game.charger_donnees()
            music_game.sauvegarder_donnees(donnees_test)
            
            # Vérifier que les notes avec accents sont bien présentes
            donnees_chargees = music_game.charger_donnees()
            assert 'Ré' in donnees_chargees['stats']['par_note']
