# +-------+-------+-------+-------+-------+-------+-------+ #
# Street Fighter made by Alexandre, Leo et Amine.           #
# Lycée Paul Lapie, 2023.                                   #
# +-------+-------+-------+-------+-------+-------+-------+ #

import pygame

class Personnage(pygame.sprite.Sprite):

    def __init__(self, window, pv, degats, x, y, sens_base, vitesse, cooldown,
                 id):
        ''' 
        pygame.Surface, int, int, int, int, int, int, int, int -> None.
        L'id a pour valeur 0 si il s'agit du joueur à gauche de l'écran au départ, sinon 1.
        '''
        super().__init__()
        self.pv = pv
        self.degats = degats
        self.sens_base = sens_base
        self.vitesse = vitesse
        self.id = id
        self.cooldown = cooldown
        self.temps_de_recup = self.cooldown + 1
        self.current_sprite_index = 0
        self.window = window

        self.pose_vers_gauche = self.import_sprites(
            ['./art/posebaseversgauche1.png', './art/posebaseversgauche2.png'])
        self.pose_vers_droite = self.import_sprites(
            ['./art/posebaseversdroite1.png', './art/posebaseversdroite2.png'])
        self.attaque_vers_gauche = self.import_sprites(
            ['./art/attaquegauche1.png', './art/attaquegauche2.png'])
        self.attaque_vers_droite = self.import_sprites(
            ['./art/attaquedroite1.png', './art/attaquedroite2.png'])

        if self.sens_base == SENS_DROITE:
            self.image = self.pose_vers_droite[self.current_sprite_index]
        else:
            self.image = self.pose_vers_gauche[self.current_sprite_index]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def import_sprites(self, images):
        ''' 
        List[str] -> List[pygame.Surface]
        '''
        tab = []
        for image in images:
            im_load = pygame.image.load(image)
            tab.append(
                pygame.transform.scale(im_load,
                                       (im_load.get_rect().width * 2,
                                        im_load.get_rect().height * 2)))
        return tab

    def update(self):
        ''' 
        None -> None
        Met à jour le sprite actuel de chaque personnage.
        C'est une méthode de la classe mère Sprite qui ne fait rien de base
        et qu'on décide donc de surcharger.
        '''
        self.current_sprite_index += 0.1

        if self.sens_base == SENS_DROITE:
            if self.current_sprite_index >= len(self.pose_vers_droite):
                self.current_sprite_index = 0

            self.image = self.pose_vers_droite[int(self.current_sprite_index)]

        else:
            if self.current_sprite_index >= len(self.pose_vers_gauche):
                self.current_sprite_index = 0

            self.image = self.pose_vers_gauche[int(self.current_sprite_index)]

    def update_inputs(self, autre_perso):
        '''
        Personnage -> None
        Déplace et oriente le personnage en fonction de la touche pressée.
        '''
        keys = pygame.key.get_pressed()
        self.temps_de_recup += 1

        if self.id == 1:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.vitesse
                self.sens_base = SENS_GAUCHE

            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.vitesse
                self.sens_base = SENS_DROITE

            elif keys[pygame.K_m]:
                self.attaque(autre_perso)
        else:
            if keys[pygame.K_q]:
                self.rect.x -= self.vitesse
                self.sens_base = SENS_GAUCHE

            elif keys[pygame.K_d]:
                self.rect.x += self.vitesse
                self.sens_base = SENS_DROITE

            elif keys[pygame.K_v]:
                self.attaque(autre_perso)

        win_w = self.window.get_width()
        win_h = self.window.get_height()

        self.rect.clamp_ip((0, 0, win_w, win_h))

    def attaque(self, autre_perso):
        ''' 
        Personnage -> None
        Permet au personnage d'attaquer un autre personnage (enlève à ce dernier un certain nombre de PV).
        '''
        if self.temps_de_recup > self.cooldown:
            if self.sens_base == SENS_DROITE:
                for i in range(len(self.attaque_vers_droite)):
                    self.image = self.attaque_vers_droite[i]

            else:
                for i in range(len(self.attaque_vers_gauche)):
                    self.image = self.attaque_vers_gauche[i]

            if self.rect.colliderect(autre_perso.rect):
                if self.sens_base == SENS_DROITE and self.rect.x < autre_perso.rect.x or self.sens_base == SENS_GAUCHE and self.rect.x > autre_perso.rect.x:
                    if autre_perso.pv - self.degats < 0:
                        autre_perso.pv = 0
                    else:
                        autre_perso.pv -= self.degats

            self.temps_de_recup = 0


SCREEN_SIZE = (1920, 1080)
FPS = 60
COLOR_BAR_PV = (55, 208, 70)
SENS_DROITE = 0
SENS_GAUCHE = 1

# +--------+--------+--------+ Initialisation +--------+--------+--------+

pygame.init()
pygame.display.set_caption('Street Fighter')

clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREEN_SIZE)
font = pygame.font.SysFont('Comic Sans MS', 150)

running = True

background = pygame.image.load('./art/terrain.jpg')

# +--------+--------+---+ Instanciations +---+--------+--------+

group_personnages = pygame.sprite.Group()
perso_1 = Personnage(window, 100, 10, 10, 770, SENS_DROITE, 10, 30, 0)
perso_2 = Personnage(window, 100, 10, 1700, 770, SENS_GAUCHE, 10, 30, 1)
group_personnages.add(perso_1)
group_personnages.add(perso_2)

bar_pv_perso_1 = pygame.Rect(20, 30, perso_1.pv, 30)
bar_pv_perso_1_background = pygame.Rect(20, 30, perso_1.pv, 30)

bar_pv_perso_2 = pygame.Rect(1700, 30, perso_2.pv, 30)
bar_pv_perso_2_background = pygame.Rect(1700, 30, perso_2.pv, 30)

# +--------+--------+-------+ Musique principale +--------+--------+-------+

music = pygame.mixer.Sound('./art/musique.mp3')
music.set_volume(0.1)
music.play(-1)

# +--------+--------+-------+ Boucle principale +-------+--------+--------+

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.blit(background, (0, 0))

    # On teste si un joueur n'a plus de PV : si c'est le cas, on met fin au jeu.
    if perso_1.pv == 0 or perso_2.pv == 0:
        texte = font.render(
            f"Le joueur {1 if perso_2.pv == 0 else 2} a gagné !", False,
            (255, 0, 0))
        text_rect = texte.get_rect(center=(SCREEN_SIZE[0] / 2,
                                           SCREEN_SIZE[1] / 2))
        window.blit(texte, text_rect) if perso_2.pv == 0 else window.blit(
            texte, text_rect)

        pygame.time.wait(6000)
        running = False

    bar_pv_perso_1.width = perso_1.pv
    bar_pv_perso_2.width = perso_2.pv

    pygame.draw.rect(window, (255, 255, 255), bar_pv_perso_1_background)
    pygame.draw.rect(window, COLOR_BAR_PV, bar_pv_perso_1)

    pygame.draw.rect(window, (255, 255, 255), bar_pv_perso_2_background)
    pygame.draw.rect(window, COLOR_BAR_PV, bar_pv_perso_2)

    perso_1.update_inputs(perso_2)
    perso_2.update_inputs(perso_1)

    group_personnages.draw(window)
    group_personnages.update()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
