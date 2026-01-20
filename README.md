# 🎵 Jeu d'Apprentissage des Notes de Musique

Un jeu éducatif interactif développé avec Pygame pour apprendre à reconnaître les notes de musique sur une portée musicale.

## 🎮 Fonctionnalités

- **Deux clés musicales** : Clé de Sol et Clé de Fa
- **Trois modes de jeu** :
  - Clé de Sol uniquement
  - Clé de Fa uniquement
  - Mode mixte (alternance aléatoire)
- **Sons réels des notes** : Génération synthétique des fréquences musicales (Do = 261.63 Hz, etc.)
- **Contrôle du son** : Activer/désactiver à tout moment avec la touche M
- **Navigation fluide** : ESC retourne au menu depuis le jeu, quitte depuis le menu
- **Système de niveaux progressifs** : La difficulté augmente au fur et à mesure
- **Interaction multiple** : Cliquez sur les boutons ou utilisez les touches 1-7
- **Retour visuel immédiat** avec messages de feedback colorés
- **Barre de temps dynamique** qui change de couleur selon l'urgence
- **Score** qui évolue avec vos bonnes et mauvaises réponses

## 📋 Prérequis

- Python 3.7+
- Pygame
- NumPy

## 🚀 Installation

### Option 1 : Télécharger l'exécutable (Recommandé)

**Pas besoin d'installer Python !**

Téléchargez l'exécutable correspondant à votre système depuis la section [Releases](https://github.com/Kiwi41/music-learning-game/releases) :

- **Windows** : `MusicLearningGame-windows.exe`
- **Linux** : `MusicLearningGame-linux`
- **macOS** : `MusicLearningGame-macos`

**Lancement** :
- **Windows** : Double-cliquez sur le fichier
- **Linux/macOS** : `chmod +x MusicLearningGame-* && ./MusicLearningGame-*`

### Option 2 : Installation depuis les sources

1. Clonez le dépôt :
```bash
git clone https://github.com/Kiwi41/music-learning-game.git
cd music-learning-game
```

2. Installez les dépendances :
```bash
pip install pygame numpy
```

## 🔨 Compiler l'exécutable (optionnel)

### Build automatique via GitHub Actions ⭐

**Les exécutables sont buildés automatiquement !** À chaque tag `v*.*.*`, GitHub Actions crée automatiquement les 3 versions (Windows, Linux, macOS) et les publie dans les releases.

Pour créer une nouvelle release avec builds automatiques :
```bash
git tag v1.0.1
git push origin v1.0.1
```

### Build manuel (si nécessaire)

#### Sur Linux/macOS :

1. Installez PyInstaller :
```bash
pip install pyinstaller
```

2. Lancez le script de build :
```bash
./build.sh
```

3. L'exécutable sera créé dans le dossier `dist/`

#### Sur Windows :

**Important** : Ne pas utiliser depuis WSL! Clonez le projet directement sur Windows (ex: `C:\Users\...\music-learning-game`)

1. Installez Python et les dépendances :
```cmd
pip install pygame numpy pyinstaller
```

2. Lancez le script de build :
```cmd
build.bat
```

3. L'exécutable `MusicLearningGame.exe` sera créé dans le dossier `dist\`

## 🎯 Comment jouer

1. Lancez le jeu :
```bash
python music_game.py
```

2. **Menu principal** : Choisissez votre mode de jeu
   - Cliquez sur un bouton ou appuyez sur 1, 2 ou 3

3. **Pendant le jeu** :
   - Une note apparaît sur la portée musicale et son son est joué automatiquement
   - Identifiez-la en cliquant sur le bouton correspondant ou en utilisant les touches 1-7
   - Les 7 notes : Do (1), Ré (2), Mi (3), Fa (4), Sol (5), La (6), Si (7)
   - Répondez avant que le temps ne s'écoule !
   - Appuyez sur M pour activer/désactiver le son

4. **Progression** :
   - +10 points × niveau pour chaque bonne réponse
   - -5 points pour chaque erreur ou temps écoulé
   - Le niveau augmente tous les 50 points
   - Le temps de réponse diminue à chaque nouveau niveau

## ⌨️ Commandes

- **Touches 1-7** : Sélectionner une note
- **Clic souris** : Cliquer sur les boutons
- **M** : Activer/Désactiver le son
- **ESC** : Retour au menu (depuis le jeu) ou quitter (depuis le menu)

## 🎨 Captures d'écran

Le jeu affiche :
- Une portée musicale avec 5 lignes
- La clé actuelle (Sol ou Fa) dessinée et étiquetée
- Les notes positionnées correctement sur la portée
- Un système de score et niveau
- Une barre de progression temporelle
- Des boutons interactifs avec effet de survol
- Un indicateur visuel de l'état du son (ON/OFF)

## 🛠️ Technologies utilisées

- **Python 3** : Langage de programmation
- **Pygame** : Bibliothèque de jeu 2D
- **NumPy** : Génération synthétique des sons

## 📝 Licence

Projet personnel à but éducatif.

## 👤 Auteur

Kiwi41

---

Bon apprentissage musical ! 🎼
