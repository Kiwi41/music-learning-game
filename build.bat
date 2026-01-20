@echo off
REM Script de build pour Windows

echo Building Music Learning Game...

REM Nettoyer les anciens builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

REM Créer l'exécutable avec PyInstaller
pyinstaller --onefile --windowed --name "MusicLearningGame" music_game.py

echo Build terminé!
echo L'exécutable se trouve dans le dossier 'dist/'
pause
