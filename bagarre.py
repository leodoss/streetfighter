import pygame
from personnage import *

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
background = pygame.image.load('images/background.jpg')
crouch1 = pygame.image.load('images/_Crouch.png')
crouch2 = pygame.image.load('images/_CrouchTransition.png')
joueur1 = Personnage('Leo', 100, 10, 5, {'crouch' : [crouch1, crouch2]})


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.blit(background, (0,0))
    pygame.display.flip()
    keys = pygame.key.get_pressed()
    
    # if keys[pygame.K_s]:
        # joueur1.crouch()

    clock.tick(60)

pygame.quit()