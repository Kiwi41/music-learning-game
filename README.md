# 🎵 Jeu d'Apprentissage des Notes de Musique

Un jeu éducatif interactif développé avec Pygame pour apprendre à reconnaître les notes de musique sur une portée musicale.

## 🎮 Fonctionnalités

- **Deux clés musicales** : Clé de Sol et Clé de Fa
- **Trois modes de jeu** :
  - Clé de Sol uniquement
  - Clé de Fa uniquement
  - Mode mixte (alternance aléatoire)
- **Système de niveaux progressifs** : La difficulté augmente au fur et à mesure
- **Interaction multiple** : Cliquez sur les boutons ou utilisez les touches 1-7
- **Retour visuel immédiat** avec messages de feedback colorés
- **Barre de temps dynamique** qui change de couleur selon l'urgence
- **Score** qui évolue avec vos bonnes et mauvaises réponses

## 📋 Prérequis

- Python 3.7+
- Pygame

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Kiwi41/music-learning-game.git
cd music-learning-game
```

2. Installez les dépendances :
```bash
pip install pygame
```

## 🎯 Comment jouer

1. Lancez le jeu :
```bash
python music_game.py
```

2. **Menu principal** : Choisissez votre mode de jeu
   - Cliquez sur un bouton ou appuyez sur 1, 2 ou 3

3. **Pendant le jeu** :
   - Une note apparaît sur la portée musicale
   - Identifiez-la en cliquant sur le bouton correspondant ou en utilisant les touches 1-7
   - Les 7 notes : Do (1), Ré (2), Mi (3), Fa (4), Sol (5), La (6), Si (7)
   - Répondez avant que le temps ne s'écoule !

4. **Progression** :
   - +10 points × niveau pour chaque bonne réponse
   - -5 points pour chaque erreur ou temps écoulé
   - Le niveau augmente tous les 50 points
   - Le temps de réponse diminue à chaque nouveau niveau

## ⌨️ Commandes

- **Touches 1-7** : Sélectionner une note
- **Clic souris** : Cliquer sur les boutons
- **ESC** : Quitter le jeu

## 🎨 Captures d'écran

Le jeu affiche :
- Une portée musicale avec 5 lignes
- La clé actuelle (Sol ou Fa) dessinée et étiquetée
- Les notes positionnées correctement sur la portée
- Un système de score et niveau
- Une barre de progression temporelle
- Des boutons interactifs avec effet de survol

## 🛠️ Technologies utilisées

- **Python 3** : Langage de programmation
- **Pygame** : Bibliothèque de jeu 2D

## 📝 Licence

Projet personnel à but éducatif.

## 👤 Auteur

Kiwi41

---

Bon apprentissage musical ! 🎼
