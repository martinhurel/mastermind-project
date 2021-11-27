#%%
import numpy as np
import time 
import pygame
from SpritesMastermind import *

class Game() :

    def __init__(self) :
        5+5

    def initialisation(self) :

        #Listes récupérants les pions
        liste_pion_deviner = []
        liste_pion_choix = []
        liste_pion_initiaux = []

        #Liste des boutons
        liste_bouton = []

        couleurs = ["yellow", "blue", "red", "green", "white", "black"]
        to_guess = [np.random.choice(couleurs) for itr in range(4)]
        print(to_guess)

        #Paramètrage des pions à deviner
        dist_x = 40
        dist_y = 0
        for couleur in to_guess :
            pion = Pion(couleur, (dist_x, dist_y))
            liste_pion_deviner.append(pion)
            dist_x += 100

        # Pion de toutes les couleurs servant pour le choix
        for couleur in couleurs :
            pion = Pion(couleur, (0, 0))
            liste_pion_choix.append(pion)

        # Pion initiaux blanc d'affichage
        for couleur in ['white', 'white', 'white', 'white'] :
            pion = Pion(couleur, (0, 0))
            pion.surface = pygame.transform.scale(pion.surface, (27, 27))
            liste_pion_initiaux.append(pion)

        #Liste des boutons de choix de couleur
        dist_button_x = 40
        for z in range(4) :
            bouton = Button((dist_button_x, 550), 'color')
            liste_bouton.append(bouton)
            dist_button_x += 100
        print(liste_bouton)

        #Bouton submit 
        submit = Button((580, 500), 'submit')
        
        return liste_pion_initiaux, liste_pion_choix, liste_pion_deviner, liste_bouton, submit, to_guess


    def iteration(self, i) :
        i += 1
        if i == 6 :
            i = 0
        return i

    def verification(self, devine, propose) :
        red = 0
        white = 0
        k = 0
        i = 0

        for p in range(4):
            if devine[i] == propose[i] :
                red += 1
                devine.pop(i)
                propose.pop(i)
                i -= 1
            i += 1
        
        i = 0
        for z in range(len(devine)) :
            for elt in devine :
                if propose[i] == elt :
                    white += 1
                    propose.pop(i)
                    devine.remove(elt)
                    i -= 1
            i += 1
                
        return red, white

    def submit_verification(self, liste_submit, liste_pion_choix, idx_submit, to_guess, game) :
    
        list_dest = to_guess.copy()
        verif = [couleur.couleur for couleur in liste_submit[(idx_submit-1)*4:idx_submit*4]]
        red_l, white_l = game.verification(list_dest, verif)

        liste_verif_r = [pygame.transform.scale(liste_pion_choix[2].surface, (10, 10)) for elt in range(red_l)]
        liste_verif_w = [pygame.transform.scale(liste_pion_choix[4].surface, (10, 10)) for elt in range(white_l)]
        liste_verif_r.extend(liste_verif_w)


        return liste_verif_r, red_l, white_l


    def submit_collision(self, idx_submit, liste_total_submit, liste_submit, liste_pion_choix, to_guess, game) :

        for w in range(9) :
            if idx_submit == w + 1 :
                liste_total_submit[w], red_l, white_l = game.submit_verification(liste_submit, liste_pion_choix, idx_submit, to_guess, game)
                return red_l

    def end_game(self, x, cache_y, running, score, red_l, idx_submit, screen) :
        x +=1
        cache_y -= 1

        if red_l == 4 :
            score = 110 - (idx_submit * 10)
            screen.blit(pygame.font.Font('freesansbold.ttf', 30).render(f"Score : {score}", True, (255, 255, 255)), (580, 10))

        if x == 100 :

            time.sleep(3)
            running = False
        
        return running, x, cache_y, score

# %%
