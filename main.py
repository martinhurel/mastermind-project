import pygame
from controller import EventManager

def main():
   
    controller = EventManager()
    
    while controller.running:
        view = controller.view
        view.handleClick()
        view.update()
                
    pygame.quit()
    
main()