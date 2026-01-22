# ========================================
# IMPORTS - Bibliothèques nécessaires
# ========================================
import pygame      # Bibliothèque pour créer des jeux 2D
import random      # Pour générer des nombres aléatoires (choix des notes)
import sys         # Pour accéder aux fonctions système
import os          # Pour gérer les chemins de fichiers
import numpy as np # Pour les calculs mathématiques (génération de sons)

# ========================================
# INITIALISATION DE PYGAME
# ========================================
pygame.init()  # Démarre tous les modules Pygame
# Initialise le système audio :
# - frequency=22050 : 22050 échantillons par seconde (qualité CD)
# - size=-16 : audio 16 bits signé
# - channels=1 : mono (une seule piste audio)
# - buffer=512 : taille du tampon audio (plus petit = moins de latence)
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

# ========================================
# CONSTANTES - Valeurs qui ne changent pas
# ========================================
# Dimensions de la fenêtre
LARGEUR = 800  # Largeur en pixels
HAUTEUR = 600  # Hauteur en pixels
FPS = 60       # Images par seconde (fluidité de l'animation)

# Définition des couleurs en RGB (Rouge, Vert, Bleu)
# Chaque composante va de 0 à 255
BLANC = (255, 255, 255)  # Maximum de toutes les couleurs = blanc
NOIR = (0, 0, 0)         # Absence de couleur = noir
VERT = (0, 200, 0)       # Vert pour les messages de succès
ROUGE = (200, 0, 0)      # Rouge pour les erreurs
BLEU = (50, 100, 200)    # Bleu pour les titres et boutons
JAUNE = (255, 215, 0)    # Jaune pour les avertissements

# ========================================
# CONFIGURATION DE LA FENÊTRE
# ========================================
# Crée la fenêtre de jeu avec les dimensions définies
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
# Définit le titre qui apparaît dans la barre de la fenêtre
pygame.display.set_caption("Apprendre les Notes de Musique")
# Crée une horloge pour contrôler le nombre d'images par seconde
horloge = pygame.time.Clock()

# ========================================
# POLICES DE CARACTÈRES
# ========================================
# Crée différentes tailles de police pour le texte
# None = police par défaut de Pygame, le nombre = taille en pixels
police_grande = pygame.font.Font(None, 72)  # Pour les titres
police_moyenne = pygame.font.Font(None, 48) # Pour les sous-titres
police_petite = pygame.font.Font(None, 36)  # Pour le texte normal

# Police musicale pour les clés
try:
    # Fonction pour obtenir le chemin des ressources (pour PyInstaller)
    def resource_path(relative_path):
        try:
            # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    police_musicale = pygame.font.Font(resource_path("Bravura.otf"), 80)
except Exception as e:
    # Fallback si la police n'est pas trouvée
    print(f"Avertissement: impossible de charger la police Bravura.otf - {e}")
    police_musicale = police_grande

# ========================================
# NOTES MUSICALES
# ========================================
# Liste des 7 notes de la gamme
NOTES = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']

# Association des touches du clavier (1-7) avec les notes
# pygame.K_1 = touche "1" du clavier, etc.
TOUCHES = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]

# Fréquences des notes en Hertz (vibrations par seconde) - octave 4
# Chaque note a une fréquence spécifique qui détermine sa hauteur
# Par exemple, le La (A4) = 440 Hz est la note de référence internationale
FREQUENCIES = {
    'Do': 261.63,   # C4 - Note la plus grave de notre jeu
    'Ré': 293.66,   # D4
    'Mi': 329.63,   # E4
    'Fa': 349.23,   # F4
    'Sol': 392.00,  # G4
    'La': 440.00,   # A4 - Note de référence (diapason)
    'Si': 493.88,   # B4 - Note la plus aiguë de notre jeu
}

def generer_son(frequence, duree=0.5):
    """
    Génère un son musical à partir d'une fréquence donnée.
    
    Cette fonction crée une onde sonore synthétique qui ressemble
    à une note de musique réelle.
    
    Paramètres:
        frequence (float): La fréquence de la note en Hz (ex: 440 pour un La)
        duree (float): La durée du son en secondes (par défaut 0.5s)
    
    Retourne:
        pygame.mixer.Sound: Un objet son jouable par Pygame
    """
    # Nombre d'échantillons audio par seconde (qualité du son)
    sample_rate = 22050
    # Nombre total d'échantillons nécessaires pour la durée voulue
    n_samples = int(sample_rate * duree)  # Ex: 22050 * 0.5 = 11025 échantillons
    
    # ÉTAPE 1: Créer l'onde sinusoïdale (la forme de base du son)
    # np.linspace crée une liste de moments dans le temps de 0 à 'duree'
    t = np.linspace(0, duree, n_samples, False)
    # np.sin crée une onde qui monte et descend (comme une vague)
    # frequence * t * 2 * np.pi : formule mathématique pour créer le bon nombre de cycles
    note = np.sin(frequence * t * 2 * np.pi)
    
    # ÉTAPE 2: Adoucir le son avec une enveloppe ADSR
    # Sans ça, le son serait brutal (comme un bip électronique)
    # Attack: montée progressive du volume au début
    attack = int(0.01 * sample_rate)  # 10 millisecondes
    # Release: descente progressive du volume à la fin
    release = int(0.1 * sample_rate)  # 100 millisecondes
    
    # Appliquer l'attack: le volume monte progressivement de 0 à 1
    for i in range(attack):
        note[i] *= i / attack  # Multiplie par un coefficient qui augmente
    
    # Appliquer le release: le volume descend progressivement de 1 à 0
    for i in range(release):
        note[-(i+1)] *= i / release  # -(i+1) = partir de la fin du tableau
    
    # ÉTAPE 3: Normaliser (ajuster le volume) et convertir en format 16-bit
    # Les cartes son utilisent des nombres entiers de -32768 à +32767
    note = note * (2**15 - 1) / np.max(np.abs(note))  # Ajuste au maximum possible
    note = note.astype(np.int16)  # Convertit en entiers 16-bit
    
    # ÉTAPE 4: Convertir en stéréo (canal gauche + canal droit)
    # On duplique simplement le signal mono pour avoir le même son des deux côtés
    stereo_note = np.column_stack((note, note))  # Colle deux colonnes identiques
    
    # ÉTAPE 5: Créer un objet Sound que Pygame peut jouer
    sound = pygame.sndarray.make_sound(stereo_note)
    return sound

# Pré-générer tous les sons des notes au démarrage du programme
# Cela évite de recalculer les sons à chaque fois qu'on en a besoin
# {nom: generer_son(freq) ...} = dictionnaire par compréhension
# Pour chaque paire (nom, freq) dans FREQUENCIES, on crée un son
SONS_NOTES = {nom: generer_son(freq) for nom, freq in FREQUENCIES.items()}

# ========================================
# POSITIONS DES NOTES SUR LA PORTÉE
# ========================================
# Ces valeurs définissent où dessiner chaque note (coordonnée Y)
# Plus le nombre est grand, plus la note est basse à l'écran

# Positions pour la clé de SOL (clé de Sol)
POSITIONS_NOTES_SOL = {
    'Do': 380,   # En dessous de la portée (ligne additionnelle)
    'Ré': 365,   # Juste en dessous de la portée
    'Mi': 350,   # Sur la première ligne (du bas)
    'Fa': 335,   # Entre la 1ère et 2ème ligne
    'Sol': 320,  # Sur la 2ème ligne
    'La': 305,   # Entre la 2ème et 3ème ligne
    'Si': 290,   # Sur la 3ème ligne (en haut de la portée)
}

# Positions pour la clé de FA (clé de Fa)
# Les notes sont différemment placées en clé de Fa
POSITIONS_NOTES_FA = {
    'Sol': 380,  # En dessous de la portée (ligne additionnelle)
    'La': 365,   # Juste en dessous de la portée
    'Si': 350,   # Sur la première ligne
    'Do': 335,   # Entre la 1ère et 2ème ligne
    'Ré': 320,   # Sur la 2ème ligne
    'Mi': 305,   # Entre la 2ème et 3ème ligne
    'Fa': 290,   # Sur la 3ème ligne
}

# ========================================
# CLASSE BOUTON - Pour les boutons cliquables
# ========================================
class Bouton:
    """
    Représente un bouton cliquable à l'écran.
    
    Gère l'affichage, la détection de clic et l'effet de survol.
    """
    def __init__(self, x, y, largeur, hauteur, texte, index):
        """
        Initialise un nouveau bouton.
        
        Paramètres:
            x, y: Position du coin supérieur gauche du bouton
            largeur, hauteur: Dimensions du bouton en pixels
            texte: Le texte affiché sur le bouton
            index: Un numéro pour identifier le bouton (0-6 pour les notes)
        """
        # pygame.Rect crée un rectangle pour détecter les clics
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte          # Le texte à afficher (ex: "Do", "Ré"...)
        self.index = index          # L'identifiant du bouton
        self.survole = False        # True si la souris est sur le bouton
        
    def dessiner(self, surface):
        """
        Dessine le bouton sur la surface donnée.
        
        Paramètre:
            surface: La fenêtre Pygame où dessiner
        """
        # Choisir la couleur : bleu si survolé, gris sinon
        couleur = BLEU if self.survole else (150, 150, 150)
        # Dessiner le rectangle rempli avec des coins arrondis
        pygame.draw.rect(surface, couleur, self.rect, border_radius=10)
        # Dessiner le contour noir du bouton
        pygame.draw.rect(surface, NOIR, self.rect, 3, border_radius=10)
        
        # Afficher le texte au centre du bouton
        # render() crée une image du texte, True = antialiasing (lissage)
        texte_surface = police_petite.render(self.texte, True, BLANC if self.survole else NOIR)
        # Centrer le texte dans le rectangle du bouton
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        # blit() = coller l'image du texte sur la surface
        surface.blit(texte_surface, texte_rect)
        
    def verifier_clic(self, pos):
        """
        Vérifie si la position donnée est à l'intérieur du bouton.
        
        Paramètre:
            pos: Tuple (x, y) de la position de la souris
        
        Retourne:
            True si le clic est sur le bouton, False sinon
        """
        return self.rect.collidepoint(pos)  # Méthode de pygame.Rect
        
    def verifier_survol(self, pos):
        """
        Met à jour l'état de survol selon la position de la souris.
        
        Paramètre:
            pos: Tuple (x, y) de la position de la souris
        """
        # Met self.survole à True si la souris est sur le bouton
        self.survole = self.rect.collidepoint(pos)

# ========================================
# CLASSE NOTE - Représente une note musicale
# ========================================
class Note:
    """
    Représente une note de musique affichée sur la portée.
    
    Gère la position et l'affichage d'une note selon la clé musicale.
    """
    def __init__(self, nom, cle='sol'):
        """
        Crée une nouvelle note.
        
        Paramètres:
            nom: Le nom de la note ('Do', 'Ré', 'Mi', etc.)
            cle: La clé musicale ('sol' ou 'fa')
        """
        self.nom = nom
        self.cle = cle
        self.x = LARGEUR // 2
        if cle == 'sol':
            self.y = POSITIONS_NOTES_SOL[nom]
        else:
            self.y = POSITIONS_NOTES_FA[nom]
        self.rayon = 15
        
    def dessiner(self, surface):
        # Dessiner une ligne additionnelle si la note est en dehors de la portée
        # En clé de Sol: seul le Do (380) nécessite une ligne
        # En clé de Fa: seul le Sol (380) nécessite une ligne
        # Le Ré (365) en Sol et La (365) en Fa sont entre les lignes, pas de ligne additionnelle
        if self.y >= 380:  # Note vraiment en dessous de la portée
            # Ligne additionnelle
            pygame.draw.line(surface, NOIR, (self.x - 25, self.y), (self.x + 25, self.y), 2)
        
        # Dessiner la tête de noire avec le caractère Bravura U+E0A4 (noteheadBlack)
        # C'est une tête de noire (remplie) avec l'ovale parfaitement penché
        tete_note = police_musicale.render('\U0000E0A4', True, NOIR)
        rect_tete = tete_note.get_rect(center=(self.x, self.y))
        surface.blit(tete_note, rect_tete)
        
        # Dessiner la tige à droite de la tête de note
        # Calculer la position de départ de la tige (bord droit de la tête)
        x_tige = self.x + 12  # Décalage pour coller au bord droit de l'ovale
        pygame.draw.line(surface, NOIR, (x_tige, self.y), (x_tige, self.y - 50), 3)

class Jeu:
    def __init__(self, mode_cle='mixte'):
        self.score = 0
        self.niveau = 1
        self.note_actuelle = None
        self.mode_cle = mode_cle  # 'sol', 'fa', ou 'mixte'
        self.cle_actuelle = 'sol'
        self.temps_reponse = 0
        self.max_temps = 5000  # 5 secondes
        self.message = ""
        self.couleur_message = NOIR
        self.temps_message = 0
        self.son_active = True  # Son activé par défaut
        self.boutons = self.creer_boutons()
        self.nouvelle_note()
    
    def creer_boutons(self):
        """Crée les boutons pour chaque note"""
        boutons = []
        largeur_bouton = 80
        hauteur_bouton = 50
        x_debut = 50
        y = 450
        espacement = 100
        
        for i, note in enumerate(NOTES):
            x = x_debut + i * espacement
            bouton = Bouton(x, y, largeur_bouton, hauteur_bouton, note, i)
            boutons.append(bouton)
        
        return boutons
        
    def nouvelle_note(self):
        """Génère une nouvelle note aléatoire"""
        # Choisir la clé selon le mode
        if self.mode_cle == 'mixte':
            self.cle_actuelle = random.choice(['sol', 'fa'])
        else:
            self.cle_actuelle = self.mode_cle
        
        nom_note = random.choice(NOTES)
        self.note_actuelle = Note(nom_note, self.cle_actuelle)
        self.temps_reponse = pygame.time.get_ticks()
        
        # Jouer le son de la note si le son est activé
        if self.son_active:
            SONS_NOTES[nom_note].play()
        
    def dessiner_portee(self, surface):
        """Dessine la portée musicale"""
        y_debut = 290
        espacement = 15
        # Dessiner les 5 lignes de la portée
        for i in range(5):
            y = y_debut + i * espacement
            pygame.draw.line(surface, NOIR, (200, y), (600, y), 2)
        
        # Dessiner la clé selon le type avec la police musicale
        if self.cle_actuelle == 'sol':
            # Clé de Sol: 𝄞 (U+1D11E) - s'enroule autour de la ligne du Sol (2ème ligne du bas)
            texte_cle = police_musicale.render("\U0001D11E", True, NOIR)
            # Ajuster pour que la spirale centrale soit sur la ligne du Sol (y=335)
            surface.blit(texte_cle, (215, 170))
            # Étiquette texte
            texte_nom = police_moyenne.render("Sol", True, BLEU)
            surface.blit(texte_nom, (210, 140))
        else:
            # Clé de Fa: 𝄢 (U+1D122) - les deux points encadrent la ligne du Fa (4ème ligne)
            texte_cle = police_musicale.render("\U0001D122", True, NOIR)
            # Ajuster pour que les points soient autour de la ligne du Fa (y=305)
            surface.blit(texte_cle, (215, 165))
            # Étiquette texte
            texte_nom = police_moyenne.render("Fa", True, BLEU)
            surface.blit(texte_nom, (210, 140))
        
    def verifier_reponse(self, index_note):
        """Vérifie si la réponse est correcte"""
        if NOTES[index_note] == self.note_actuelle.nom:
            self.score += 10 * self.niveau
            self.message = "Correct!"
            self.couleur_message = VERT
            
            # Augmenter le niveau tous les 5 bonnes réponses
            if self.score % 50 == 0:
                self.niveau += 1
                self.max_temps = max(2000, self.max_temps - 500)  # Plus rapide à chaque niveau
                self.message = f"Niveau {self.niveau}!"
                self.couleur_message = JAUNE
            
            self.nouvelle_note()
        else:
            self.score = max(0, self.score - 5)
            self.message = f"Non! C'etait {self.note_actuelle.nom}"
            self.couleur_message = ROUGE
            self.nouvelle_note()
        
        self.temps_message = pygame.time.get_ticks()
    
    def temps_ecoule(self):
        """Vérifie si le temps est écoulé"""
        temps_actuel = pygame.time.get_ticks()
        return (temps_actuel - self.temps_reponse) > self.max_temps
    
    def dessiner(self, surface):
        """Dessine tous les éléments du jeu"""
        surface.fill(BLANC)
        
        # Titre avec la clé actuelle
        cle_nom = "Sol" if self.cle_actuelle == 'sol' else "Fa"
        titre = police_moyenne.render(f"Notes de Musique - Clé de {cle_nom}", True, BLEU)
        surface.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, 30))
        
        # Score et niveau
        texte_score = police_petite.render(f"Score: {self.score}", True, NOIR)
        texte_niveau = police_petite.render(f"Niveau: {self.niveau}", True, NOIR)
        surface.blit(texte_score, (50, 30))
        surface.blit(texte_niveau, (50, 70))
        
        # Barre de temps (déplacée plus bas pour être visible)
        temps_restant = max(0, self.max_temps - (pygame.time.get_ticks() - self.temps_reponse))
        pourcentage = temps_restant / self.max_temps
        largeur_barre = int(200 * pourcentage)
        couleur_barre = VERT if pourcentage > 0.5 else (JAUNE if pourcentage > 0.25 else ROUGE)
        
        # Position de la barre
        barre_x = 50
        barre_y = 120
        pygame.draw.rect(surface, couleur_barre, (barre_x, barre_y, largeur_barre, 20))
        pygame.draw.rect(surface, NOIR, (barre_x, barre_y, 200, 20), 2)
        
        # Texte "Temps" au-dessus de la barre
        texte_temps = police_petite.render("Temps:", True, NOIR)
        surface.blit(texte_temps, (barre_x, barre_y - 30))
        
        # Dessiner la portée
        self.dessiner_portee(surface)
        
        # Dessiner la note
        if self.note_actuelle:
            self.note_actuelle.dessiner(surface)
        
        # Instructions
        texte_instructions = police_petite.render("Cliquez ou utilisez les touches 1-7:", True, NOIR)
        surface.blit(texte_instructions, (LARGEUR // 2 - texte_instructions.get_width() // 2, 420))
        
        # Dessiner les boutons
        for bouton in self.boutons:
            bouton.dessiner(surface)
        
        # Message de feedback
        if self.temps_message > 0 and pygame.time.get_ticks() - self.temps_message < 1000:
            texte_msg = police_moyenne.render(self.message, True, self.couleur_message)
            surface.blit(texte_msg, (LARGEUR // 2 - texte_msg.get_width() // 2, 520))
        
        # Instructions ESC et son
        texte_esc = police_petite.render("ESC pour retour au menu", True, NOIR)
        surface.blit(texte_esc, (10, HAUTEUR - 40))
        
        # Indicateur de son
        etat_son = "ON" if self.son_active else "OFF"
        couleur_son = VERT if self.son_active else ROUGE
        texte_son = police_petite.render(f"Son: {etat_son} (M)", True, couleur_son)
        surface.blit(texte_son, (LARGEUR - texte_son.get_width() - 10, HAUTEUR - 40))

def ecran_accueil():
    """Affiche l'écran d'accueil avec sélection de clé"""
    en_attente = True
    mode_choisi = None
    
    # Créer les boutons de sélection
    bouton_sol = Bouton(200, 300, 150, 60, "Clé de Sol", 0)
    bouton_fa = Bouton(400, 300, 150, 60, "Clé de Fa", 1)
    bouton_mixte = Bouton(300, 380, 150, 60, "Les deux", 2)
    bouton_entrainement = Bouton(250, 460, 250, 60, "Entraînement", 3)
    boutons_menu = [bouton_sol, bouton_fa, bouton_mixte, bouton_entrainement]
    
    while en_attente:
        pos_souris = pygame.mouse.get_pos()
        for bouton in boutons_menu:
            bouton.verifier_survol(pos_souris)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Retourner None pour quitter
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    if bouton_sol.verifier_clic(pos):
                        mode_choisi = 'sol'
                        en_attente = False
                    elif bouton_fa.verifier_clic(pos):
                        mode_choisi = 'fa'
                        en_attente = False
                    elif bouton_mixte.verifier_clic(pos):
                        mode_choisi = 'mixte'
                        en_attente = False
                    elif bouton_entrainement.verifier_clic(pos):
                        mode_choisi = 'entrainement'
                        en_attente = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None  # Retourner None pour quitter
                elif event.key == pygame.K_1:
                    mode_choisi = 'sol'
                    en_attente = False
                elif event.key == pygame.K_2:
                    mode_choisi = 'fa'
                    en_attente = False
                elif event.key == pygame.K_3:
                    mode_choisi = 'mixte'
                    en_attente = False
                elif event.key == pygame.K_4:
                    mode_choisi = 'entrainement'
                    en_attente = False
        
        fenetre.fill(BLANC)
        
        # Titre
        titre = police_grande.render("Notes de Musique", True, BLEU)
        fenetre.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, 80))
        
        # Instructions
        instructions = [
            "Apprenez à reconnaître les notes!",
            "",
            "Choisissez votre mode de jeu:",
        ]
        
        y = 180
        for ligne in instructions:
            texte = police_petite.render(ligne, True, NOIR)
            fenetre.blit(texte, (LARGEUR // 2 - texte.get_width() // 2, y))
            y += 40
        
        # Dessiner les boutons
        for bouton in boutons_menu:
            bouton.dessiner(fenetre)
        
        # Instructions clavier
        texte_info = police_petite.render("Cliquez ou appuyez sur 1, 2, 3 ou 4", True, NOIR)
        fenetre.blit(texte_info, (LARGEUR // 2 - texte_info.get_width() // 2, 540))
        
        # Instruction ESC
        texte_esc = police_petite.render("ESC pour quitter", True, NOIR)
        fenetre.blit(texte_esc, (10, HAUTEUR - 40))
        
        pygame.display.flip()
        horloge.tick(FPS)
    
    return mode_choisi

def boucle_jeu(mode_cle='mixte'):
    """Boucle de jeu"""
    jeu = Jeu(mode_cle)
    en_cours = True
    retour_menu = False
    
    while en_cours:
        # Gérer le survol des boutons
        pos_souris = pygame.mouse.get_pos()
        for bouton in jeu.boutons:
            bouton.verifier_survol(pos_souris)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quitter l'application
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True  # Retour au menu
                elif event.key == pygame.K_m:
                    jeu.son_active = not jeu.son_active  # Toggle le son
                
                # Vérifier si une touche de note est pressée
                for i, touche in enumerate(TOUCHES):
                    if event.key == touche:
                        jeu.verifier_reponse(i)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    pos = event.pos
                    # Vérifier si un bouton a été cliqué
                    for bouton in jeu.boutons:
                        if bouton.verifier_clic(pos):
                            jeu.verifier_reponse(bouton.index)
        
        # Vérifier si le temps est écoulé
        if jeu.temps_ecoule():
            jeu.message = f"Temps écoulé! C'était {jeu.note_actuelle.nom}"
            jeu.couleur_message = ROUGE
            jeu.temps_message = pygame.time.get_ticks()
            jeu.score = max(0, jeu.score - 5)
            jeu.nouvelle_note()
        
        # Dessiner
        jeu.dessiner(fenetre)
        
        pygame.display.flip()
        horloge.tick(FPS)
    
    return False

def mode_entrainement():
    """Mode entraînement: cliquez sur une note pour la voir et l'entendre"""
    en_cours = True
    note_affichee = None
    cle_actuelle = 'sol'  # Commencer en clé de Sol
    son_active = True
    
    # Créer les boutons pour les notes
    boutons_notes = []
    notes_list = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']
    x_start = 50
    for i, nom_note in enumerate(notes_list):
        bouton = Bouton(x_start + i * 100, 450, 80, 50, nom_note, i)
        boutons_notes.append(bouton)
    
    # Bouton pour changer de clé
    bouton_changer_cle = Bouton(LARGEUR // 2 - 75, 520, 150, 40, "Changer clé", -1)
    
    while en_cours:
        pos_souris = pygame.mouse.get_pos()
        for bouton in boutons_notes:
            bouton.verifier_survol(pos_souris)
        bouton_changer_cle.verifier_survol(pos_souris)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quitter l'application
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True  # Retour au menu
                elif event.key == pygame.K_m:
                    son_active = not son_active  # Toggle le son
                
                # Vérifier si une touche de note est pressée
                for i, touche in enumerate(TOUCHES):
                    if event.key == touche:
                        nom_note = notes_list[i]
                        note_affichee = Note(nom_note, cle_actuelle)
                        if son_active:
                            SONS_NOTES[nom_note].play()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    pos = event.pos
                    # Vérifier si un bouton de note a été cliqué
                    for bouton in boutons_notes:
                        if bouton.verifier_clic(pos):
                            nom_note = bouton.texte
                            note_affichee = Note(nom_note, cle_actuelle)
                            if son_active:
                                SONS_NOTES[nom_note].play()
                    
                    # Vérifier si le bouton changer clé a été cliqué
                    if bouton_changer_cle.verifier_clic(pos):
                        cle_actuelle = 'fa' if cle_actuelle == 'sol' else 'sol'
                        # Recréer la note affichée avec la nouvelle clé
                        if note_affichee:
                            note_affichee = Note(note_affichee.nom, cle_actuelle)
        
        # Dessiner
        fenetre.fill(BLANC)
        
        # Titre
        titre = police_grande.render("Mode Entraînement", True, BLEU)
        fenetre.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, 30))
        
        # Sous-titre (nom de la clé)
        sous_titre = police_moyenne.render(f"Clé de {cle_actuelle.capitalize()}", True, BLEU)
        fenetre.blit(sous_titre, (LARGEUR // 2 - sous_titre.get_width() // 2, 220))
        
        # Instructions
        instruction = police_petite.render("Cliquez sur une note pour la voir et l'entendre", True, NOIR)
        fenetre.blit(instruction, (LARGEUR // 2 - instruction.get_width() // 2, 100))
        
        # Dessiner la portée
        y_debut = 290
        espacement = 15
        for i in range(5):
            y = y_debut + i * espacement
            pygame.draw.line(fenetre, NOIR, (200, y), (600, y), 2)
        
        # Dessiner la clé
        if cle_actuelle == 'sol':
            texte_cle = police_musicale.render("\U0001D11E", True, NOIR)
            fenetre.blit(texte_cle, (215, 170))
            texte_nom = police_moyenne.render("Sol", True, BLEU)
            fenetre.blit(texte_nom, (210, 140))
        else:
            texte_cle = police_musicale.render("\U0001D122", True, NOIR)
            fenetre.blit(texte_cle, (215, 165))
            texte_nom = police_moyenne.render("Fa", True, BLEU)
            fenetre.blit(texte_nom, (210, 140))
        
        # Dessiner la note si une est affichée
        if note_affichee:
            note_affichee.dessiner(fenetre)
        
        # Dessiner les boutons de notes
        for bouton in boutons_notes:
            bouton.dessiner(fenetre)
        
        # Dessiner le bouton changer clé
        bouton_changer_cle.dessiner(fenetre)
        
        # État du son
        etat_son = "ON" if son_active else "OFF"
        couleur_son = VERT if son_active else ROUGE
        texte_son = police_petite.render(f"Son: {etat_son} (M)", True, couleur_son)
        fenetre.blit(texte_son, (LARGEUR - texte_son.get_width() - 10, HAUTEUR - 40))
        
        # Instruction ESC
        texte_esc = police_petite.render("ESC pour revenir au menu", True, NOIR)
        fenetre.blit(texte_esc, (10, HAUTEUR - 40))
        
        pygame.display.flip()
        horloge.tick(FPS)
    
    return False

def boucle_principale():
    """Boucle principale avec menu"""
    continuer = True
    
    while continuer:
        mode = ecran_accueil()
        if mode is None:
            # L'utilisateur a quitté depuis le menu
            continuer = False
        elif mode == 'entrainement':
            # Lancer le mode entraînement
            continuer = mode_entrainement()
        else:
            # Lancer le jeu et vérifier si on doit continuer
            continuer = boucle_jeu(mode)
    
    pygame.quit()
    sys.exit()

# Lancement du jeu
if __name__ == "__main__":
    boucle_principale()
