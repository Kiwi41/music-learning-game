import pygame
import random
import sys
import numpy as np

# Initialisation de pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

# Constantes
LARGEUR = 800
HAUTEUR = 600
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (0, 200, 0)
ROUGE = (200, 0, 0)
BLEU = (50, 100, 200)
JAUNE = (255, 215, 0)

# Configuration de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Apprendre les Notes de Musique")
horloge = pygame.time.Clock()

# Polices
police_grande = pygame.font.Font(None, 72)
police_moyenne = pygame.font.Font(None, 48)
police_petite = pygame.font.Font(None, 36)

# Notes musicales
NOTES = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']
TOUCHES = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]

# Fréquences des notes (en Hz) - octave 4
FREQUENCIES = {
    'Do': 261.63,   # C4
    'Ré': 293.66,   # D4
    'Mi': 329.63,   # E4
    'Fa': 349.23,   # F4
    'Sol': 392.00,  # G4
    'La': 440.00,   # A4
    'Si': 493.88,   # B4
}

def generer_son(frequence, duree=0.5):
    """Génère un son à partir d'une fréquence donnée"""
    sample_rate = 22050
    n_samples = int(sample_rate * duree)
    
    # Générer une onde sinusoïdale
    t = np.linspace(0, duree, n_samples, False)
    note = np.sin(frequence * t * 2 * np.pi)
    
    # Appliquer une enveloppe ADSR simplifiée pour adoucir le son
    attack = int(0.01 * sample_rate)  # 10ms
    decay = int(0.1 * sample_rate)    # 100ms
    release = int(0.1 * sample_rate)  # 100ms
    
    for i in range(attack):
        note[i] *= i / attack
    for i in range(release):
        note[-(i+1)] *= i / release
    
    # Normaliser et convertir en 16-bit
    note = note * (2**15 - 1) / np.max(np.abs(note))
    note = note.astype(np.int16)
    
    # Convertir en stéréo (dupliquer le canal)
    stereo_note = np.column_stack((note, note))
    
    # Créer un objet Sound
    sound = pygame.sndarray.make_sound(stereo_note)
    return sound

# Pré-générer tous les sons des notes
SONS_NOTES = {nom: generer_son(freq) for nom, freq in FREQUENCIES.items()}

# Positions des notes sur la portée en clé de SOL (y coordinate)
POSITIONS_NOTES_SOL = {
    'Do': 380,   # En dessous de la portée
    'Ré': 365,
    'Mi': 350,
    'Fa': 335,
    'Sol': 320,
    'La': 305,
    'Si': 290,
}

# Positions des notes sur la portée en clé de FA (y coordinate)
POSITIONS_NOTES_FA = {
    'Sol': 380,  # En dessous de la portée
    'La': 365,
    'Si': 350,
    'Do': 335,
    'Ré': 320,
    'Mi': 305,
    'Fa': 290,
}

class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, index):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.index = index
        self.survole = False
        
    def dessiner(self, surface):
        # Couleur du bouton selon si la souris survole
        couleur = BLEU if self.survole else (150, 150, 150)
        pygame.draw.rect(surface, couleur, self.rect, border_radius=10)
        pygame.draw.rect(surface, NOIR, self.rect, 3, border_radius=10)
        
        # Texte du bouton
        texte_surface = police_petite.render(self.texte, True, BLANC if self.survole else NOIR)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)
        
    def verifier_clic(self, pos):
        return self.rect.collidepoint(pos)
        
    def verifier_survol(self, pos):
        self.survole = self.rect.collidepoint(pos)

class Note:
    def __init__(self, nom, cle='sol'):
        self.nom = nom
        self.cle = cle
        self.x = LARGEUR // 2
        if cle == 'sol':
            self.y = POSITIONS_NOTES_SOL[nom]
        else:
            self.y = POSITIONS_NOTES_FA[nom]
        self.rayon = 15
        
    def dessiner(self, surface):
        # Dessiner la note
        pygame.draw.ellipse(surface, NOIR, (self.x - self.rayon, self.y - 8, self.rayon * 2, 16))
        # Dessiner la tige
        pygame.draw.line(surface, NOIR, (self.x + self.rayon, self.y), (self.x + self.rayon, self.y - 50), 3)

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
        largeur_bouton = 90
        hauteur_bouton = 50
        x_debut = 100
        y = 460
        espacement = 95
        
        for i, note in enumerate(NOTES):
            x = x_debut + i * espacement
            bouton = Bouton(x, y, largeur_bouton, hauteur_bouton, f"{i+1}. {note}", i)
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
        
        # Dessiner la clé selon le type
        if self.cle_actuelle == 'sol':
            # Clé de Sol (forme simplifiée)
            pygame.draw.circle(surface, NOIR, (230, 320), 12, 3)
            pygame.draw.arc(surface, NOIR, (218, 285, 24, 50), 0, 3.14, 3)
            pygame.draw.line(surface, NOIR, (230, 270), (230, 345), 3)
            # Étiquette texte
            texte_cle = police_moyenne.render("Sol", True, BLEU)
            surface.blit(texte_cle, (210, 240))
        else:
            # Clé de Fa (forme simplifiée)
            pygame.draw.arc(surface, NOIR, (210, 300, 30, 25), 0, 3.14, 3)
            pygame.draw.circle(surface, NOIR, (245, 305), 3)
            pygame.draw.circle(surface, NOIR, (245, 320), 3)
            # Étiquette texte
            texte_cle = police_moyenne.render("Fa", True, BLEU)
            surface.blit(texte_cle, (210, 240))
        
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
    bouton_sol = Bouton(200, 350, 150, 60, "Clé de Sol", 0)
    bouton_fa = Bouton(400, 350, 150, 60, "Clé de Fa", 1)
    bouton_mixte = Bouton(300, 430, 150, 60, "Les deux", 2)
    boutons_menu = [bouton_sol, bouton_fa, bouton_mixte]
    
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
        texte_info = police_petite.render("Cliquez ou appuyez sur 1, 2 ou 3", True, NOIR)
        fenetre.blit(texte_info, (LARGEUR // 2 - texte_info.get_width() // 2, 520))
        
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

def boucle_principale():
    """Boucle principale avec menu"""
    continuer = True
    
    while continuer:
        mode = ecran_accueil()
        if mode is None:
            # L'utilisateur a quitté depuis le menu
            continuer = False
        else:
            # Lancer le jeu et vérifier si on doit continuer
            continuer = boucle_jeu(mode)
    
    pygame.quit()
    sys.exit()

# Lancement du jeu
if __name__ == "__main__":
    boucle_principale()
