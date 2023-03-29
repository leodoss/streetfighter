import pygame

class Personnage(pygame.sprite.Sprite):
    def __init__(self, x, y, sens_base):
        super().__init__()
        self.sens_base = sens_base
        
        self.posebaseversdroite = []
        imd1 = pygame.image.load('images/posebaseversdroite1.png')
        imd2 = pygame.image.load('images/posebaseversdroite2.png')
        self.posebaseversdroite.append(pygame.transform.scale(imd1, (imd1.get_rect().width*2, imd1.get_rect().height*2)))
        self.posebaseversdroite.append(pygame.transform.scale(imd2, (imd2.get_rect().width*2, imd2.get_rect().height*2)))
        
        self.posebaseversgauche = []
        img1 = pygame.image.load('images/posebaseversgauche1.png')
        img2 = pygame.image.load('images/posebaseversgauche2.png')
        self.posebaseversgauche.append(pygame.transform.scale(img1, (img1.get_rect().width*2, img1.get_rect().height*2)))
        self.posebaseversgauche.append(pygame.transform.scale(img2, (img2.get_rect().width*2, img2.get_rect().height*2)))
        
        self.curseur = 0
        if self.sens_base == "droite":
            self.image = self.posebaseversdroite[self.curseur]
        else:
            self.image = self.posebaseversgauche[self.curseur]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        
    def update(self):
        '''
        C'est une méthode de la classe mère Sprite qui ne fait rien de base
        et qu'on décide donc de surcharger
        '''
        self.curseur += 0.1
        
        if self.sens_base == "droite":
            if self.curseur >= len(self.posebaseversdroite):
                self.curseur = 0
            
            self.image = self.posebaseversdroite[int(self.curseur)]
            
        else:
            if self.curseur >= len(self.posebaseversgauche):
                self.curseur = 0
            
            self.image = self.posebaseversgauche[int(self.curseur)]
        
# Initialisation
pygame.init()
clock = pygame.time.Clock()

# Fenêtre
screen = pygame.display.set_mode((1920, 1080))
running = True
background = pygame.image.load('images/terrain.jpg')

# Importation des sprites
group_personnages = pygame.sprite.Group()
perso1 = Personnage(10, 770, "droite")
group_personnages.add(perso1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.blit(background, (0,0))
    group_personnages.draw(screen)
    group_personnages.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
