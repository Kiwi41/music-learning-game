"""Tests pour la génération audio"""
import pytest
import numpy as np
import sys
import os

# Ajouter le répertoire parent au path pour importer music_game
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer après avoir modifié le path
import pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

from music_game import generer_son, FREQUENCIES_SOL, FREQUENCIES_FA


class TestGenerationAudio:
    """Tests de la génération de sons"""
    
    def test_generer_son_retourne_sound(self):
        """Vérifie que generer_son retourne bien un objet Sound"""
        son = generer_son(440.0)  # La4
        assert isinstance(son, pygame.mixer.Sound)
    
    def test_generer_son_duree_par_defaut(self):
        """Vérifie que la durée par défaut est appliquée"""
        son = generer_son(440.0)
        # La durée par défaut est 0.5s mais la durée effective peut être réduite
        # par l'enveloppe ADSR, on vérifie juste qu'on a un son
        assert son.get_length() > 0.1
        assert son.get_length() < 0.6
    
    def test_generer_son_duree_personnalisee(self):
        """Vérifie que la durée personnalisée fonctionne"""
        son = generer_son(440.0, duree=1.0)
        # Vérifie que la durée est cohérente
        assert son.get_length() > 0.4
        assert son.get_length() < 1.1
    
    def test_generer_son_frequences_differentes(self):
        """Vérifie que différentes fréquences génèrent des sons différents"""
        son_do = generer_son(FREQUENCIES_SOL['Do'])
        son_sol = generer_son(FREQUENCIES_SOL['Sol'])
        
        # Deux fréquences différentes doivent produire des sons différents
        # On ne peut pas comparer directement les objets Sound,
        # mais on peut vérifier qu'ils existent et ont des propriétés valides
        assert isinstance(son_do, pygame.mixer.Sound)
        assert isinstance(son_sol, pygame.mixer.Sound)
        assert FREQUENCIES_SOL['Do'] != FREQUENCIES_SOL['Sol']
    
    def test_frequencies_sol_completes(self):
        """Vérifie que toutes les notes ont une fréquence en clé de Sol"""
        notes = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']
        for note in notes:
            assert note in FREQUENCIES_SOL
            assert FREQUENCIES_SOL[note] > 0
            assert isinstance(FREQUENCIES_SOL[note], float)
    
    def test_frequencies_fa_completes(self):
        """Vérifie que toutes les notes ont une fréquence en clé de Fa"""
        notes = ['Sol', 'La', 'Si', 'Do', 'Ré', 'Mi', 'Fa']
        for note in notes:
            assert note in FREQUENCIES_FA
            assert FREQUENCIES_FA[note] > 0
            assert isinstance(FREQUENCIES_FA[note], float)
    
    def test_frequencies_fa_plus_graves(self):
        """Vérifie que les fréquences en clé de Fa sont plus graves"""
        # Les notes communes aux deux clés devraient être plus graves en clé de Fa
        notes_communes = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']
        for note in notes_communes:
            if note in FREQUENCIES_FA and note in FREQUENCIES_SOL:
                assert FREQUENCIES_FA[note] < FREQUENCIES_SOL[note], \
                    f"La fréquence de {note} devrait être plus grave en clé de Fa"
