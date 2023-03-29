import pygame

class Personnage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.posebaseversdroite = []
        im1 = pygame.image.load('images/posebaseversdroite1.png')
        im2 = pygame.image.load('images/posebaseversdroite2.png')
        self.posebaseversdroite.append(pygame.transform.scale(im1, (im1.get_rect().width*2, im1.get_rect().height*2)))
        self.posebaseversdroite.append(pygame.transform.scale(im2, (im2.get_rect().width*2, im2.get_rect().height*2)))
        
        self.curseur = 0
        self.image = self.posebaseversdroite[self.curseur]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        
    def update(self):
        '''
        C'est une méthode de la classe mère Sprite qui ne fait rien de base
        et qu'on décide donc de surcharger
        '''
        self.curseur += 0.1
        if self.curseur >= len(self.posebaseversdroite):
            self.curseur = 0
        
        self.image = self.posebaseversdroite[int(self.curseur)]
        
# Initialisation
pygame.init()
clock = pygame.time.Clock()

# Fenêtre
screen = pygame.display.set_mode((1920, 1080))
running = True
background = pygame.image.load('images/terrain.jpg')

# Importation des sprites
group_personnages = pygame.sprite.Group()
perso1 = Personnage(10, 770)
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
