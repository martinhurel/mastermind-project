import pygame

class Pion(pygame.sprite.Sprite) :

    def __init__(self, couleur, pos) :
        
        #Attribut de la couleur du pion
        self.couleur = couleur
               
        super().__init__()
        
        #Charger l'image du pion
        pion_img = pygame.image.load(f'color/{couleur}.png')
        #On redimensionne le sprite
        self.surface = pygame.transform.scale(pion_img, (30, 30))
        
        self.rect = self.surface.get_rect(topleft=pos)
                       

class Button(pygame.sprite.Sprite) :

    def __init__(self, pos, button_type) :
               
        super().__init__()
        
        #Charger l'image
        if button_type == 'color' :
            path = 'color_button.png'
        elif button_type == 'submit' :
            path = 'submit_button.jpg'
            
        button_img = pygame.image.load(path)
        
        #On redimensionne le sprite
        if button_type == 'color' :
            self.surface = pygame.transform.scale(button_img, (80, 80))
        elif button_type == 'submit' :
            self.surface = pygame.transform.scale(button_img, (160, 80))
            
        self.rect = self.surface.get_rect(topleft=pos)