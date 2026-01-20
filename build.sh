#!/bin/bash

# Script de build pour créer l'exécutable du jeu

echo "🎵 Building Music Learning Game..."

# Nettoyer les anciens builds
rm -rf build dist *.spec

# Créer l'exécutable avec PyInstaller
pyinstaller --onefile \
    --windowed \
    --name "MusicLearningGame" \
    --icon=NONE \
    --add-data "Bravura.otf:." \
    music_game.py

echo "✅ Build terminé!"
echo "📦 L'exécutable se trouve dans le dossier 'dist/'"
