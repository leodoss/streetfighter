import pygame

class Personnage(pygame.sprite.Sprite):
    def __init__(self, pv, degats, x, y, sens_base, vitesse, id):
        super().__init__()
        self.pv = pv
        self.degats = degats
        self.sens_base = sens_base
        self.vitesse = vitesse
        self.id = id
        
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
            
    def update_input(self, autre_perso) :
        keys = pygame.key.get_pressed()
        if self.id == 1:
            if keys[pygame.K_LEFT]:
                if self.rect.x - 1*self.vitesse < 0:
                    self.rect.x = 0
                else:
                    self.rect.x -= 1 * self.vitesse
                    
                self.sens_base = 'gauche'
                
            elif keys[pygame.K_RIGHT]:
                if self.rect.x + 1*self.vitesse >= 1730:
                    self.rect.x = 1730
                else:
                    self.rect.x += 1 * self.vitesse
                    
                self.sens_base = 'droite'
                
            elif keys[pygame.K_m] :
                self.attaque(autre_perso)
        else:
            if keys[pygame.K_q]:
                if self.rect.x - 1*self.vitesse < 0:
                    self.rect.x = 0
                else:
                    self.rect.x -= 1 * self.vitesse
                    
                self.sens_base = 'gauche'
                
            elif keys[pygame.K_d]:
                if self.rect.x + 1*self.vitesse >= 1730:
                    self.rect.x = 1730
                else:
                    self.rect.x += 1 * self.vitesse
                    
                self.sens_base = 'droite'
                
            elif keys[pygame.K_v]:
                self.attaque(autre_perso)
    
    def attaque(self, autre_perso):
        if self.rect.colliderect(autre_perso.rect):
            if autre_perso.pv - self.degats < 0:
                autre_perso.pv = 0
            else:
                autre_perso.pv -= self.degats
    
            
            
                
            
        
    
# Initialisation
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS',30)

# Fenêtre
screen = pygame.display.set_mode((1920, 1080))
running = True
background = pygame.image.load('images/terrain.jpg')

# Importation des sprites
group_personnages = pygame.sprite.Group()
perso1 = Personnage(1000, 10, 10, 770, "droite", 10, 0)
perso2 = Personnage(1000, 10, 1700, 770, "gauche", 10, 1)
group_personnages.add(perso1)
group_personnages.add(perso2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pvPerso1 = font.render(str(perso1.pv), False, (255,255,255))
    pvPerso2 = font.render(str(perso2.pv), False, (255,255,255))
    
            
    screen.blit(background, (0,0))
    screen.blit(pvPerso1, (20,20))
    screen.blit(pvPerso2, (1700,20))
    perso1.update_input(perso2)
    perso2.update_input(perso1)
    
    group_personnages.draw(screen)
    group_personnages.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()