import pygame

# Initialisation de Pygame
pygame.init()

# Obtenir la taille de l'écran de l'utilisateur
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# Calculer un multiplicateur basé sur la hauteur de l'écran
base_height = 768  # Hauteur de référence
scale_multiplier = screen_height / base_height

# Paramètres du carré (personnage)
square_size = int(128 * scale_multiplier)

# Couleurs
blanc = (255, 255, 255)
rouge = (255, 0, 0)
vert = (9, 125, 20)
noir = (0, 0, 0)

# Angle et longueur du cône de lumière
cone_angle = 70  # Angle du cône
cone_length = int(400 * scale_multiplier)  # Portée de la lumière
cone_active = True  # Le cône est allumé au début

# Liste pour stocker les positions de la moisissure et des ennemis 
moisissures = []
moisissure_colliders = []
ennemis = []
ennemis_tues = 0

# Initialisation de la santé du joueur
player_health = 100

# Image du personnage au lancement du jeu
personnage = pygame.image.load('images/homme_droit_1.png')
personnage = pygame.transform.scale(personnage, (square_size, square_size))

largeur_map = int(1366 * 2 * scale_multiplier)

velocity = int(largeur_map / 300)  # Vitesse de déplacement

# Position de la caméra
camera_x, camera_y = 0, 0

# Ajouter une texture de moisissure
moisissure_image = pygame.image.load('images/tache1.png')
moisissure_image = pygame.transform.scale(moisissure_image, (int(150 * scale_multiplier), int(150 * scale_multiplier)))
# Ajouter une texture de moisissure2
moisissure_image2 = pygame.image.load('images/tache2.png')
moisissure_image2 = pygame.transform.scale(moisissure_image, (int(150 * scale_multiplier), int(150 * scale_multiplier)))