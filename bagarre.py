# +-------+-------+-------+-------+-------+-------+-------+ #
# Street Fighter made by par Léo, Alexandre et Amine        #
# Lycée Paul Lapie, 2023. NSI.                              #
# +-------+-------+-------+-------+-------+-------+-------+ #

import pygame


class Personnage(pygame.sprite.Sprite):

    def __init__(self, window, pv, degats, x, y, sens_base, vitesse, cooldown,
                 id):
        ''' 
        pygame.Surface, int, int, int, int, str, float, float -> None.
        '''
        super().__init__()
        self.pv = pv
        self.degats = degats
        self.sens_base = sens_base
        self.vitesse = vitesse
        self.id = id  # 0 = perso gauche et 1 = perso droite
        self.cooldown = cooldown
        self.temps_de_recup = self.cooldown + 1
        self.curseur = 0
        self.window = window

        self.pose_vers_gauche = self.import_sprites([
            'images/posebaseversgauche1.png', 'art/posebaseversgauche2.png'
        ])
        self.pose_vers_droite = self.import_sprites([
            'images/posebaseversdroite1.png', 'art/posebaseversdroite2.png'
        ])
        self.attaque_vers_gauche = self.import_sprites(
            ['images/attaquegauche1.png', 'art/attaquegauche2.png'])
        self.attaque_vers_droite = self.import_sprites(
            ['images/attaquedroite1.png', 'images/attaquedroite2.png'])

        if self.sens_base == "droite":
            self.image = self.pose_vers_droite[self.curseur]
        else:
            self.image = self.pose_vers_gauche[self.curseur]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def import_sprites(self, images):
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
        C'est une méthode de la classe mère Sprite qui ne fait rien de base
        et qu'on décide donc de surcharger.
        '''
        self.curseur += 0.1

        if self.sens_base == 'droite':
            if self.curseur >= len(self.pose_vers_droite):
                self.curseur = 0

            self.image = self.pose_vers_droite[int(self.curseur)]

        else:
            if self.curseur >= len(self.pose_vers_gauche):
                self.curseur = 0

            self.image = self.pose_vers_gauche[int(self.curseur)]

    def update_inputs(self, autre_perso):
        '''
        Personnage -> None
        Déplacement des personnages à GAUCHE, DROITE et attaque avec 'm ou 'v' selon p1 et p2 
        '''
        keys = pygame.key.get_pressed()
        self.temps_de_recup += 1

        if self.id == 1:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.vitesse
                self.sens_base = 'gauche'

            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.vitesse
                self.sens_base = 'droite'

            elif keys[pygame.K_m]:
                self.attaque(autre_perso)
        else:
            if keys[pygame.K_q]:
                self.rect.x -= self.vitesse
                self.sens_base = 'gauche'

            elif keys[pygame.K_d]:
                self.rect.x += self.vitesse
                self.sens_base = 'droite'

            elif keys[pygame.K_v]:
                self.attaque(autre_perso)

        win_w = self.window.get_width()
        win_h = self.window.get_height()

        self.rect.clamp_ip((0, 0, win_w, win_h))

    def attaque(self, autre_perso):
        ''' 
        Personnage -> None
        Permet au personnage d'attaquer un autre personnage en lui enlevant certain nombre de pv propre a celui-ci.
        '''
        if self.temps_de_recup > self.cooldown:
            if self.sens_base == 'droite':  # sprite qui frappe à gauche
                for i in range(len(self.attaque_vers_droite)):
                    self.image = self.attaque_vers_droite[i]

            if self.sens_base == 'gauche':  # sprite qui frappe à droite
                for i in range(len(self.attaque_vers_gauche)):
                    self.image = self.attaque_vers_gauche[i]

            if self.rect.colliderect(autre_perso.rect):
                if self.sens_base == 'droite' and self.rect.x < autre_perso.rect.x or self.sens_base == 'gauche' and self.rect.x > autre_perso.rect.x:

                    if autre_perso.pv - self.degats < 0:
                        autre_perso.pv = 0

                    else:
                        autre_perso.pv -= self.degats

            self.temps_de_recup = 0


SCREEN_SIZE = (1920, 1080)
FPS = 60
COLOR_BAR_PV = (55, 208, 70)

# +--------+--------+--------+ Initialisation +--------+--------+--------+

pygame.init()
pygame.display.set_caption('Combattant de la street')

clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREEN_SIZE)
running = True
font = pygame.font.SysFont('Comic Sans MS', 150)

background = pygame.image.load('./art/terrain.jpg')

# +--------+--------+---+ Instanciations des objets +---+--------+--------+

group_personnages = pygame.sprite.Group()
perso_1 = Personnage(window, 100, 10, 10, 770, 'droite', 10, 30, 0)
perso_2 = Personnage(window, 100, 10, 1700, 770, 'gauche', 10, 30, 1)
group_personnages.add(perso_1)
group_personnages.add(perso_2)

bar_pv_perso_1 = pygame.Rect(20, 30, perso_1.pv, 30)
bar_pv_perso_1_background = pygame.Rect(20, 30, perso_1.pv, 30)

bar_pv_perso_2 = pygame.Rect(1700, 30, perso_2.pv, 30)
bar_pv_perso_2_background = pygame.Rect(1700, 30, perso_2.pv, 30)

# +--------+--------+--------+ Musiques et sons +-------+--------+--------+

music = pygame.mixer.Sound('./art/musique.mp3')
music.set_volume(0.1)
music.play(-1)

# +--------+--------+-------+ Boucle principale +-------+--------+--------+

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.blit(background, (0, 0))

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
