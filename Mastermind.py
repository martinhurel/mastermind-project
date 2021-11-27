#%%
import pygame

from GameMastermind import Game

game = Game()


def submit_affichage(couleur, x, y, incr) :
    screen.blit(couleur, (x, y))
    x += incr
    return x

def submit_affichage_final2(liste_submit, liste_total_submit, borne, index, distance) :
    dist_x_rep = 65
    for couleur in liste_submit[borne: borne + 4] :
        dist_x_rep = submit_affichage(couleur.surface, dist_x_rep, distance, 100)
    dist_x_verif = 435
    for pion in liste_total_submit[index] :
        dist_x_verif = submit_affichage(pion, dist_x_verif, distance + 12, 25)

score = 0
while True :
    #Initialisation du jeu et de la fenêtre
    liste_pion_initiaux, liste_pion_choix, liste_pion_deviner, liste_bouton, submit, to_guess = game.initialisation()
    pygame.init()
    screen = pygame.display.set_mode((800, 650))

    #Titre de la fenêtre 
    pygame.display.set_caption("Mastermind")

    #Logo de la fenêtre
    icon = pygame.image.load('logo.png')
    pygame.display.set_icon(icon)

    #Police d'écriture
    font = pygame.font.Font('freesansbold.ttf', 14)
    text_x = 0
    text_y = 300

    #Déclaration de variables :
    clicked_sprites = []
    i = j = k = l = -1
    c_pion1 = c_pion2 = c_pion3 = c_pion4 = []

    #variables submit
    m = 525
    red_l = idx_submit = 0
    liste_submit = liste_dest = liste_verif_r = liste_verif_w = []
    liste_verif_1 = liste_verif_2 = liste_verif_3 = liste_verif_4 = liste_verif_5 = liste_verif_6 = liste_verif_7 = liste_verif_8 = liste_verif_9 = []
    liste_total_submit = [liste_verif_1, liste_verif_2, liste_verif_3, liste_verif_4, liste_verif_5, liste_verif_6, liste_verif_7, liste_verif_8, liste_verif_9]
    
    #variables fin de jeu
    x = cache_y = 0

    #Game loop
    running = True
    while running :

        #Couleur de l'écran RGB
        screen.fill((80, 80, 80))

        #Boucle évènement
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
                pygame.display.quit()
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN :
                pos = pygame.mouse.get_pos()
                print(pos)

                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in liste_pion_deviner if s.rect.collidepoint(pos)]

                c_pion1 = [s for s in liste_bouton if liste_bouton[0].rect.collidepoint(pos)]
                c_pion2 = [s for s in liste_bouton if liste_bouton[1].rect.collidepoint(pos)]
                c_pion3 = [s for s in liste_bouton if liste_bouton[2].rect.collidepoint(pos)]
                c_pion4 = [s for s in liste_bouton if liste_bouton[3].rect.collidepoint(pos)]

                #A chaque clic sur sprite, l'index avance, il revient à 0 à la fin de la liste de couleurs
                if c_pion1 :
                    k = game.iteration(k)
                if c_pion2 :
                    l = game.iteration(l)
                if c_pion3 :
                    i = game.iteration(i) 
                if c_pion4 :
                    j = game.iteration(j)

                #Action quand on presse le bouton submit
                if submit.rect.collidepoint(pos) :
                    m -= 50
                    idx_submit += 1
                    liste_submit.extend([liste_pion_choix[k], liste_pion_choix[l], liste_pion_choix[i], liste_pion_choix[j]])
                    
                    red_l = game.submit_collision(idx_submit, liste_total_submit, liste_submit, liste_pion_choix, to_guess, game)
                    print(liste_total_submit)

        #Affichage du tableau de jeu
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(30, 0, 400, 600))
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(430, 0, 100, 600))
        dist_bande_y = 75
        dist_bande_y_2 = 76

        #Affichage des bandelettes
        for p in range(10) :
            pygame.draw.rect(screen, (120, 120, 120), pygame.Rect(30, dist_bande_y, 400, 30))

            #Affichage des pions initiaux
            dist_initiaux_x = 66
            for pion in liste_pion_initiaux :
                screen.blit(pion.surface, (dist_initiaux_x, dist_bande_y_2))
                dist_initiaux_x += 100

            dist_bande_y += 50
            dist_bande_y_2 += 50

            if p == 9 :
                pygame.draw.rect(screen, (150, 0, 150), pygame.Rect(30, 525, 400, 30))

        #Affichage après submit (4 couleurs proposés + pions verification)
        if idx_submit > 0 :
            submit_affichage_final2(liste_submit, liste_total_submit, 0, 0, 475)
        if idx_submit > 1 :
            submit_affichage_final2(liste_submit, liste_total_submit, 4, 1, 425)
        if idx_submit > 2 :
            submit_affichage_final2(liste_submit, liste_total_submit, 8, 2, 375)
        if idx_submit > 3 :
            submit_affichage_final2(liste_submit, liste_total_submit, 12, 3, 325)
        if idx_submit > 4 :
            submit_affichage_final2(liste_submit, liste_total_submit, 16, 4, 275)
        if idx_submit > 5 :
            submit_affichage_final2(liste_submit, liste_total_submit, 20, 5, 225)
        if idx_submit > 6 :
            submit_affichage_final2(liste_submit, liste_total_submit, 24, 6, 175)
        if idx_submit > 7 :
            submit_affichage_final2(liste_submit, liste_total_submit, 28, 7, 125)
        if idx_submit > 8 :
            submit_affichage_final2(liste_submit, liste_total_submit, 32, 8, 75)

        #Affichage des pions de choix de couleur 
        screen.blit(liste_pion_choix[k].surface, (65, 525))
        screen.blit(liste_pion_choix[l].surface, (165, 525))
        screen.blit(liste_pion_choix[i].surface, (265, 525))
        screen.blit(liste_pion_choix[j].surface, (365, 525))

        #Affichage des pions à deviner
        dist_x = 65
        for pion in liste_pion_deviner :
            dist_x = submit_affichage(pion.surface, dist_x, 15, 100)

        #Affichage du rectangle cache réponse:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(30, cache_y, 400, 60))

        #Affichage des triangles de choix :
        dist_choice_x = 40
        for bouton in liste_bouton :
            screen.blit(bouton.surface, (dist_choice_x, 550))
            screen.blit(font.render("color", True, (255, 255, 255)), (dist_choice_x + 23, 600))
            dist_choice_x += 100

        #Affichage bouton submit :
        screen.blit(submit.surface, (580, 500))

        #Affichage Titre Mastermind
        screen.blit(pygame.transform.scale(pygame.image.load('mastermind.jpg'), (175, 175)), (585, 200))
        
        # Actions lorsque la partie est gagnée
        if red_l == 4 :
            screen.blit(pygame.font.Font('freesansbold.ttf', 30).render("You win !", True, (255, 255, 255)), (580, 400))
            running, x, cache_y, score = game.end_game(x, cache_y, running, score, red_l, idx_submit, screen)

        if idx_submit == 9 and red_l < 4 :
            screen.blit(pygame.font.Font('freesansbold.ttf', 30).render("Game Over", True, (255, 255, 255)), (580, 400))
            running, x, cache_y, score = game.end_game(x, cache_y, running, score, red_l, idx_submit, screen)

        #MaJ des données du jeu         
        pygame.display.update()
# %%

# %%
