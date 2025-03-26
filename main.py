import sys
import pygame
import cv2
import niveau_1
import niveau_2
import pygame.mixer
from sauvegarde import ecrire_variable, lire_variable

pygame.init()

# Constantes de la fenêtre
info = pygame.display.Info()
LARGEUR_ECRAN, HAUTEUR_ECRAN = info.current_w, info.current_h

# Calculer un multiplicateur basé sur la hauteur de l'écran
base_height = 768  # Hauteur de référence
scale_multiplier = HAUTEUR_ECRAN / base_height


try:
    FENETRE = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.FULLSCREEN)
    pygame.display.set_caption("Mon Jeu")
except pygame.error as e:
    print(f"Erreur lors de la création de la fenêtre : {e}")
    sys.exit()

# Chargement des images
try:
    fond = pygame.image.load("images/fond.png").convert()
    logo = pygame.image.load("images/logo.png").convert_alpha()
except pygame.error as e:
    print(f"Erreur lors du chargement des images : {e}")
    sys.exit()

# Redimensionnement des images pour s'adapter à la résolution de l'écran
fond = pygame.transform.scale(fond, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
logo = pygame.transform.scale(logo, (int(LARGEUR_ECRAN * 0.175), int(LARGEUR_ECRAN * 0.175)))  # 300/800 = 0.375, 150/600 = 0.25

# Charger les images des étoiles
etoiles_0 = pygame.image.load('images/etoiles0.png').convert_alpha()
etoiles_1 = pygame.image.load('images/etoiles1.png').convert_alpha()
etoiles_2 = pygame.image.load('images/etoiles2.png').convert_alpha()
etoiles_3 = pygame.image.load('images/etoiles3.png').convert_alpha()

# Redimensionner les images des étoiles pour s'adapter à l'interface
etoiles_0 = pygame.transform.scale(etoiles_0, (int(100 * scale_multiplier), int(50 * scale_multiplier)))
etoiles_1 = pygame.transform.scale(etoiles_1, (int(100 * scale_multiplier), int(50 * scale_multiplier)))
etoiles_2 = pygame.transform.scale(etoiles_2, (int(100 * scale_multiplier), int(50 * scale_multiplier)))
etoiles_3 = pygame.transform.scale(etoiles_3, (int(100 * scale_multiplier), int(50 * scale_multiplier)))

# Boutons
class Bouton:
    def __init__(self, texte, position, action, image=None):
        self.texte = texte
        self.position = position
        self.action = action
        self.image = image
        if self.image:
            self.rect = self.image.get_rect(topleft=position)
        else:
            self.rect = pygame.Rect(position[0], position[1], int(100*scale_multiplier), int(50*scale_multiplier))  # Taille par défaut pour un bouton sans image
        self.couleur = (64, 0, 0)  # Rouge par défaut
        self.couleur_hover = (100, 50, 50)  # Rouge clair pour hover

    def dessiner(self, surface):
        couleur = self.couleur_hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.couleur
        if self.image:
            surface.blit(self.image, self.rect.topleft)
        else:
            pygame.draw.rect(surface, couleur, self.rect, border_radius=5)
            # Utiliser une police qui prend en charge les émojis
            font = pygame.font.Font(pygame.font.match_font("segoeuiemoji"), int(36*scale_multiplier))
            texte_surface = font.render(self.texte, True, (255, 255, 255))
            texte_rect = texte_surface.get_rect(center=self.rect.center)
            surface.blit(texte_surface, texte_rect)

    def clic(self, pos):
        return self.rect.collidepoint(pos)

def jouer_cinematique(niveau):
    cap = cv2.VideoCapture(f'images/cinematique_{niveau}.mp4')
    if not cap.isOpened():
        print(f"Erreur : Impossible de lire la cinématique {niveau}")
        return
    
    # Charger et jouer l'audio
    pygame.mixer.init()
    pygame.mixer.music.load(f'images/cinematique_{niveau}.mp3')
    pygame.mixer.music.play()
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    clock = pygame.time.Clock()
    son_active = True
    font = pygame.font.Font(None, int(36*scale_multiplier))
    echap_appuye = False
    temps_appui = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (LARGEUR_ECRAN, HAUTEUR_ECRAN))  # Redimensionner la frame
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        FENETRE.blit(frame, (0, 0))
        
        # Afficher le texte
        text_surface = font.render("Appuyez sur Espace pour activer/désactiver le son.", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(LARGEUR_ECRAN // 2, HAUTEUR_ECRAN - 50))
        FENETRE.blit(text_surface, text_rect)
        
        # Afficher le cercle de progression pour passer la cinématique
        if echap_appuye:
            temps_appui += clock.get_time()
            pygame.draw.circle(FENETRE, (255, 255, 255), (int(50*scale_multiplier), HAUTEUR_ECRAN - int(50*scale_multiplier)), int(20*scale_multiplier), int(2*scale_multiplier))
            pygame.draw.arc(FENETRE, (255, 255, 255), (int(30*scale_multiplier), HAUTEUR_ECRAN - int(70*scale_multiplier), int(40*scale_multiplier), int(40*scale_multiplier)), 0, (temps_appui / 2000) * 2 * 3.14159, int(4*scale_multiplier))
            if temps_appui >= 2000:
                break
        else:
            temps_appui = 0
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if son_active:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(1)
                son_active = not son_active
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                echap_appuye = True
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                echap_appuye = False
        
        clock.tick(fps)
    
    cap.release()
    pygame.mixer.music.stop()

def draw_etoiles_image(niveau, etoiles, bouton_rect):
    """Affiche l'image des étoiles obtenues à gauche du bouton du niveau."""
    if etoiles == 0:
        etoiles_image = etoiles_0
    elif etoiles == 1:
        etoiles_image = etoiles_1
    elif etoiles == 2:
        etoiles_image = etoiles_2
    else:
        etoiles_image = etoiles_3

    # Positionner l'image à gauche du bouton
    etoiles_x = bouton_rect.left - int(100 * scale_multiplier)  # Décalage à gauche
    etoiles_y = bouton_rect.centery - etoiles_image.get_height() // 2  # Centrer verticalement
    FENETRE.blit(etoiles_image, (etoiles_x, etoiles_y))


def lancer_niveau_1():
    global etoiles_niveau_1
    jouer_cinematique(1)
    etoiles_obtenues = niveau_1.main()
    if etoiles_obtenues > etoiles_niveau_1:
        etoiles_niveau_1 = etoiles_obtenues
    

def lancer_niveau_2():
    global etoiles_niveau_2
    #jouer_cinematique(2)
    etoiles_obtenues = niveau_2.main()
    if etoiles_obtenues > etoiles_niveau_1:
        etoiles_niveau_1 = etoiles_obtenues

def reinitialiser_niveau_1():
    niveau_1.reinitialiser()
    print("Progression du niveau 1 réinitialisée.")

def reinitialiser_niveau_2():
    niveau_2.reinitialiser()
    print("Progression du niveau 2 réinitialisée.")

def afficher_menu_principal():
    """Affiche le menu principal."""
    clock = pygame.time.Clock()
    
    # Charger les images des boutons
    image_niveau_1 = pygame.image.load('images/bouton_niveau1.png').convert_alpha()
    image_niveau_2 = pygame.image.load('images/bouton_niveau2.png').convert_alpha()
    image_controles = pygame.image.load('images/bouton_controles.png').convert_alpha()
    image_quitter = pygame.image.load('images/bouton_quitter.png').convert_alpha()
    
    # Redimensionner les images des boutons pour qu'elles aient la taille souhaitée
    largeur_bouton = int(200*scale_multiplier)  # Largeur souhaitée pour les boutons
    hauteur_bouton = int(110*scale_multiplier)   # Hauteur souhaitée pour les boutons
    image_niveau_1 = pygame.transform.scale(image_niveau_1, (largeur_bouton, hauteur_bouton))
    image_niveau_2 = pygame.transform.scale(image_niveau_2, (largeur_bouton, hauteur_bouton))
    image_controles = pygame.transform.scale(image_controles, (largeur_bouton, hauteur_bouton))
    image_quitter = pygame.transform.scale(image_quitter, (largeur_bouton, hauteur_bouton))
    
    boutons = [
        Bouton("Niveau 1", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 - int(140*scale_multiplier)), lancer_niveau_1, image=image_niveau_1),
        Bouton("🔄️", (LARGEUR_ECRAN // 2 + largeur_bouton // 2 + 20, HAUTEUR_ECRAN // 2 - int(140*scale_multiplier) + hauteur_bouton//4), reinitialiser_niveau_1),
        Bouton("Niveau 2", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 - int(20*scale_multiplier)), lancer_niveau_2, image=image_niveau_2),
        Bouton("🔄️", (LARGEUR_ECRAN // 2 + largeur_bouton // 2 + 20, HAUTEUR_ECRAN // 2 - int(20*scale_multiplier) + hauteur_bouton//4), reinitialiser_niveau_2),
        Bouton("Contrôles", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 + int(100*scale_multiplier)), afficher_controles, image=image_controles),
        Bouton("Quitter", (LARGEUR_ECRAN // 2 - largeur_bouton // 2, HAUTEUR_ECRAN // 2 + int(220*scale_multiplier)), lambda: pygame.quit() or sys.exit(), image=image_quitter)
    ]
    
    while True:
        FENETRE.blit(fond, (0, 0))
        FENETRE.blit(logo, (LARGEUR_ECRAN // 2 - logo.get_width() // 2, 50))

        for bouton in boutons:
            bouton.dessiner(FENETRE)

            if bouton.texte == "Niveau 1":
                etoiles_obtenues1 = lire_variable("sauvegarde1.txt", "etoiles_obtenues1")
                draw_etoiles_image(1, etoiles_obtenues1, bouton.rect)
            
            elif bouton.texte == "Niveau 2":
                etoiles_obtenues2 = lire_variable("sauvegarde2.txt", "etoiles_obtenues2")
                draw_etoiles_image(2, etoiles_obtenues2, bouton.rect)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bouton in boutons:
                    if bouton.clic(event.pos):
                        print(f"Bouton cliqué : {bouton.texte}")
                        bouton.action()
        
        clock.tick(30)

# Charger et redimensionner les images des touches
touche_Z = pygame.transform.scale(pygame.image.load('images/touche_Z.png').convert_alpha(), (int(64*scale_multiplier), int(64*scale_multiplier)))
touche_S = pygame.transform.scale(pygame.image.load('images/touche_S.png').convert_alpha(), (int(64*scale_multiplier), int(64*scale_multiplier)))
touche_D = pygame.transform.scale(pygame.image.load('images/touche_D.png').convert_alpha(), (int(64*scale_multiplier), int(64*scale_multiplier)))
touche_Q = pygame.transform.scale(pygame.image.load('images/touche_Q.png').convert_alpha(), (int(64*scale_multiplier), int(64*scale_multiplier)))
touche_Echap = pygame.transform.scale(pygame.image.load('images/touche_Echap.png').convert_alpha(), (int(64*scale_multiplier), int(64*scale_multiplier)))
touche_E = pygame.transform.scale(pygame.image.load('images/touche_E.png').convert_alpha(), (int(64*scale_multiplier), int(64*scale_multiplier)))
touche_CliqueDroit = pygame.transform.scale(pygame.image.load('images/touche_CliqueDroit.png').convert_alpha(), (int(64*scale_multiplier), int(64*scale_multiplier)))
touche_CliqueGauche = pygame.transform.scale(pygame.image.load('images/touche_CliqueGauche.png').convert_alpha(), (int(64*scale_multiplier), int(64*scale_multiplier)))

def draw_text_with_outline(surface, text, font, color, outline_color, pos, outline_width=2):
    text_surface = font.render(text, True, color)
    outline_surface = font.render(text, True, outline_color)
    x, y = pos
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                surface.blit(outline_surface, (x + dx, y + dy))
    surface.blit(text_surface, pos)

def afficher_controles():
    """Affiche une fenêtre avec les contrôles du jeu."""
    controles_actif = True
    font = pygame.font.Font(None, int(36*scale_multiplier))
    controles = [
        ("Aller en haut", touche_Z),
        ("Aller en bas", touche_S),
        ("Aller à droite", touche_D),
        ("Aller à gauche", touche_Q),
        ("Accéder au menu", touche_Echap),
        ("Accéder à la carte", touche_E),
        ("Allumer la lampe torche", touche_CliqueDroit),
        ("Nettoyer la moisissure", touche_CliqueGauche)
    ]
    
    bouton_retour = Bouton("Retour",((LARGEUR_ECRAN // 2) - (int(100 * scale_multiplier) // 2), HAUTEUR_ECRAN - int(100 * scale_multiplier)),afficher_menu_principal) 


    while controles_actif:
        fond_controles = pygame.image.load("images/fond.jpg").convert()
        fond_controles = pygame.transform.scale(fond_controles, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
        
        # Convertir l'image en format compatible avec OpenCV
        fond_controles_array = pygame.surfarray. array3d(fond_controles)
        fond_controles_array = cv2.cvtColor(fond_controles_array, cv2.COLOR_RGB2BGR)
        
        # Appliquer un flou léger
        fond_controles_array = cv2.GaussianBlur(fond_controles_array, (15, 15), 0)
        
        # Convertir l'image floue en format compatible avec Pygame
        fond_controles_array = cv2.cvtColor(fond_controles_array, cv2.COLOR_BGR2RGB)
        fond_controles = pygame.surfarray.make_surface(fond_controles_array)
        
        FENETRE.blit(fond_controles, (0, 0))      

        y_offset_left = int(HAUTEUR_ECRAN * 0.2)
        y_offset_right = int(HAUTEUR_ECRAN * 0.2)
        
        for i, (texte, image) in enumerate(controles):
            # Calculer la largeur totale (image + texte) pour centrer
            texte_surface = font.render(texte, True, (255, 255, 255))
            total_width = image.get_width() + texte_surface.get_width() + int(20 * scale_multiplier)  # Espacement entre image et texte
            
            if i < 4:  # Colonne de gauche
                x_centered = (LARGEUR_ECRAN // 4) - (total_width // 2)  # Centrer dans le quart gauche
                FENETRE.blit(image, (x_centered, y_offset_left))
                draw_text_with_outline(FENETRE, texte, font, (255, 255, 255), (0, 0, 0), 
                                       (x_centered + image.get_width() + int(20 * scale_multiplier), y_offset_left + image.get_height() // 4))
                y_offset_left += int(HAUTEUR_ECRAN * 0.15)
            else:  # Colonne de droite
                x_centered = (3 * LARGEUR_ECRAN // 4) - (total_width // 2)  # Centrer dans le quart droit
                FENETRE.blit(image, (x_centered, y_offset_right))
                draw_text_with_outline(FENETRE, texte, font, (255, 255, 255), (0, 0, 0), 
                                       (x_centered + image.get_width() + int(20 * scale_multiplier), y_offset_right + image.get_height() // 4))
                y_offset_right += int(HAUTEUR_ECRAN * 0.15)
        
        bouton_retour.dessiner(FENETRE)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                controles_actif = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_retour.clic(event.pos):
                    controles_actif = False
                    afficher_menu_principal()

def main():
    afficher_menu_principal()

if __name__ == "__main__":
    main()