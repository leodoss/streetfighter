import pygame

class Personnage:
    def __init__(self, nom, pv, atk, vit, image) :
        self.nom = nom
        self.pv = pv
        self.atk = atk
        self.vit = vit
        self.pos = (0,0)
        self.image = image
        
    def attack(self, Perso2) :
        if Perso2.pv > 0:
            Perso2.pv -= self.atk
            if Perso2.pv <= 0 :
                Perso2.pv = 0
    
    def crouch(self):
        tab_images = self.image["crouch"]
        
        
        
                
    
            
        
        