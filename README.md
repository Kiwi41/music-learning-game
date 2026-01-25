# 🎵 Jeu d'Apprentissage des Notes de Musique

Un jeu éducatif interactif développé avec Pygame pour apprendre à reconnaître les notes de musique sur une portée musicale.

![Menu Principal](images/screenshot_menu.png)
![Jeu en cours](images/screenshot_game.png)
![Mode Entraînement](images/screenshot_training.png)

## 🎮 Fonctionnalités

### Modes de Jeu
- **Deux clés musicales** : Clé de Sol et Clé de Fa avec symboles musicaux professionnels (police Bravura)
- **Quatre modes de jeu** :
  - Clé de Sol uniquement (octave 4, Do à Si)
  - Clé de Fa uniquement (octaves 3-4, Do central identique à la clé de Sol)
  - Mode mixte (alternance aléatoire)
  - **Mode entraînement** : Explorez les notes à votre rythme sans timer ni score

### Engagement & Progression
- **🏆 High Score persistant** : Votre meilleur score est sauvegardé automatiquement
- **🔥 Système de combo** : Enchaînez les bonnes réponses pour des bonus (+2 points par niveau de combo)
- **📊 Statistiques détaillées** :
  - Nombre de sessions jouées
  - Taux de réussite global
  - Statistiques par note (tentatives, réussites, pourcentage)
- **Système de niveaux progressifs** : La difficulté augmente au fur et à mesure (modes jeu)
- **Sauvegarde portable** : Vos données sont stockées dans le même dossier que l'exécutable

### Audio & Interactivité
- **Sons réels des notes** : Génération synthétique avec fréquences authentiques
  - Clé de Sol : Do4 (261.63 Hz) à Si4 (493.88 Hz)
  - Clé de Fa : Do4 (261.6 Hz) identique à la clé de Sol, gamme cohérente de Sol3 à Fa3
- **Contrôle du son** : Activer/désactiver à tout moment avec la touche M
- **Interaction multiple** : Cliquez sur les boutons ou utilisez les touches 1-7

### Interface & Visuel
- **Navigation fluide** : ESC retourne au menu depuis le jeu, quitte depuis le menu
- **Retour visuel immédiat** avec messages de feedback colorés
- **Barre de temps dynamique** qui change de couleur selon l'urgence (modes jeu)
- **Score en temps réel** qui évolue avec vos bonnes et mauvaises réponses
- **Notation musicale authentique** : 
  - Noires professionnelles avec police Bravura (taille optimisée 55px)
  - Lignes additionnelles correctes (Do en dessous pour clé de Sol, Do au-dessus pour clé de Fa)
  - Symboles de clés précisément positionnés
  - Positionnement exact des notes sur la portée
- **Interface épurée** : Layout optimisé, aucun chevauchement de texte
- **Exécutables portables** pour Windows, Linux et macOS (aucune installation requise)

## 📋 Prérequis

### Pour l'exécutable (recommandé)
Aucun prérequis ! Les exécutables sont autonomes et incluent tout le nécessaire.

### Pour l'installation depuis les sources
- Python 3.7+
- Pygame 2.x
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

### Si vous avez téléchargé l'exécutable :

- **Windows** : Double-cliquez sur `MusicLearningGame-windows.exe`
- **Linux** : Ouvrez un terminal et lancez :
  ```bash
  chmod +x MusicLearningGame-linux
  ./MusicLearningGame-linux
  ```
- **macOS** : Ouvrez un terminal et lancez :
  ```bash
  chmod +x MusicLearningGame-macos
  ./MusicLearningGame-macos
  ```

### Si vous avez installé depuis les sources :

```bash
python music_game.py
```

### Dans le jeu :

1. **Menu principal** : Choisissez votre mode
   - Cliquez sur un bouton ou appuyez sur 1, 2, 3, 4 ou 5
   - **Option 5** : Statistiques - consultez vos performances

2. **Mode Entraînement** :
   - Cliquez sur une note (Do à Si) pour la voir positionnée sur la portée et l'entendre
   - Bouton "Changer clé" pour basculer entre clé de Sol et clé de Fa
   - Pas de timer, pas de score : apprenez à votre rythme
   - Idéal pour se familiariser avec les positions des notes

3. **Modes Jeu (Sol, Fa, Mixte)** :
   - Une note apparaît sur la portée musicale et son son est joué automatiquement
   - Identifiez-la en cliquant sur le bouton correspondant ou en utilisant les touches 1-7
   - Les 7 notes : Do (1), Ré (2), Mi (3), Fa (4), Sol (5), La (6), Si (7)
   - Répondez avant que le temps ne s'écoule !
   - Appuyez sur M pour activer/désactiver le son
   - **Combo** : Enchaînez les bonnes réponses pour des points bonus !
   - **High Score** : Essayez de battre votre meilleur score

4. **Écran Statistiques** :
   - Consultez votre meilleur score
   - Nombre de sessions jouées
   - Taux de réussite global et par note
   - Identifiez les notes à améliorer

5. **Progression (modes jeu)** :
   - +10 points × niveau pour chaque bonne réponse
   - **Bonus combo** : +2 points supplémentaires par niveau de combo au-dessus de 1
   - -5 points pour chaque erreur ou temps écoulé
   - Le niveau augmente tous les 50 points
   - Le temps de réponse diminue à chaque nouveau niveau
   - Les combos se réinitialisent en cas d'erreur

## ⌨️ Commandes

- **Touches 1-7** : Sélectionner une note (Do à Si)
- **Touche 4** : Mode entraînement (depuis le menu)
- **Touche 5** : Statistiques (depuis le menu)
- **Clic souris** : Cliquer sur les boutons
- **M** : Activer/Désactiver le son
- **ESC** : Retour au menu (depuis le jeu/entraînement/stats) ou quitter (depuis le menu)

## 🎨 Captures d'écran

### Menu Principal
![Menu](images/screenshot_menu.png)

Choisissez votre mode : Clé de Sol, Clé de Fa, Mode Mixte, ou Entraînement.

### Jeu en cours
![Gameplay](images/screenshot_game.png)

Le jeu affiche :
- Une portée musicale authentique avec 5 lignes
- La clé actuelle (Sol 𝄞 ou Fa 𝄢) avec symboles musicaux professionnels
- Notes rondes parfaitement dessinées avec lignes additionnelles correctes
- Un système de score et niveau en temps réel (modes jeu)
- **High score** : Votre meilleur score affiché en permanence
- **Indicateur de combo** : Apparaît dès 2 bonnes réponses consécutives
- Une barre de progression temporelle (modes jeu)
- Sept boutons interactifs avec effet de survol (Do, Ré, Mi, Fa, Sol, La, Si)
- Un indicateur visuel de l'état du son (ON/OFF)
- Mode entraînement : interface épurée pour explorer les notes librement

### Écran Statistiques
Consultez vos performances détaillées :
- Meilleur score absolu
- Nombre de sessions jouées
- Taux de réussite global
- Statistiques par note avec code couleur (vert > 70%, jaune > 50%, rouge < 50%)

## 🛠️ Technologies utilisées

- **Python 3** : Langage de programmation
- **Pygame** : Bibliothèque de jeu 2D
- **NumPy** : Génération synthétique des sons musicaux avec enveloppe ADSR
- **PyInstaller** : Création d'exécutables portables
- **GitHub Actions** : Build automatique multi-plateforme (CI/CD)
- **Police Bravura** : Symboles musicaux professionnels (Steinberg)
- **Pytest** : Tests unitaires automatisés (36 tests, couverture 34%)

## 📝 Licence

Projet personnel à but éducatif.

## 👤 Auteur

Kiwi41

---

Bon apprentissage musical ! 🎼
