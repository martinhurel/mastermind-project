import pygame
from pygame.locals import *
import random
from utils import draw_text
import time
import csv
from datetime import datetime
import pandas as pd

class RGB(Color):
    def hex_format(self):
        return '#{:02X}{:02X}{:02X}'.format(self.red,self.green,self.blue)

COLORS = ['blue', 'red', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'black', 'lightblue', 'darkgreen', 'darkblue']

class Game:
    def __init__(self, difficulty, name):
        # Create all the 10 line
        self.line = [[RGB('grey')]*4]*10
        self.answerClue = [[(17,65,0)]*4]*10
        # Create the line wich the player will modify
        self.linePlayer = [RGB('grey')]*4
        # Element in linePlayer that the player will modify
        self.elementPlayerPosition = 0
        # Line number that has been validate
        self.linePlayerPosition = 0
        self.answer = self.create_answer()
        self.finish = False
        self.winning = False
        self.screen = ''
        self.choices_pos = []
        self.name = name
        self.difficulty = difficulty
        self.COLORS = COLORS[:(4+int(difficulty))]

    def update(self):
        # Create button validation
        pygame.init()
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',45)
        self.screen.fill((0, 9, 30))
        image = pygame.image.load("bg-wood.png")
        self.screen.blit(image, (0,0))
        image = pygame.image.load("backspace.png")
        self.screen.blit(image, (530,710))
        self.createLine()
        self.createColor()
        self.text_validate = (55, 730)
        draw_text('MASTERMIND', game_font, (255, 255, 255), self.screen, (800/4)+50, 20)
        text_validate = smallfont.render('Valider' , True , RGB('white'))
        self.screen.blit(text_validate, self.text_validate)
        
        self.choices_pos = []
        
        y = 475
        for i in range(len(COLORS)):
            if i == 0:
                y = 475
                x = 690
            elif i % 2 :
                x += 50
            else:
                x = 690
                y += 50
            pygame.draw.circle(self.screen, RGB(COLORS[i]), (x,y),15)

            self.choices_pos.append((x,y))
        pygame.display.update()

    def handleGameEvent(self, mouse_pos, event):

        matching_delete_x = (520 <= mouse_pos[0] <= 520 + 70)
        matching_delete_y = (720 <= mouse_pos[1] <= 720 + 70)
        if matching_delete_x & matching_delete_y:
            if self.elementPlayerPosition >= 1:
                self.linePlayer[self.elementPlayerPosition - 1] = RGB('grey')
                self.elementPlayerPosition -= 1
        for position in self.choices_pos:
            matching_round_x = (position[0] - 20 <= mouse_pos[0] <= position[0] + 20)
            matching_round_y = (position[1] - 20 <= mouse_pos[1] <= position[1] + 20)

            if matching_round_x & matching_round_y:
                index = self.choices_pos.index(position)
                self.changeLinePlayer(COLORS[index])

            matching_text_x = (self.text_validate[0] <= mouse_pos[0] <= self.text_validate[0] + 100)
            matching_text_y = (self.text_validate[1] <= mouse_pos[1] <= self.text_validate[1] + 60)
            if matching_text_x & matching_text_y:
                self.validate()

    def create_answer(self):
        # Pick 4 random number between 0 and 3 (compris)
        answer = []

        for i in range(0,4):
            rand = random.randint(0, len(COLORS) - 1)	
            answer.append(RGB(COLORS[rand]))

        return answer

    def changeLinePlayer(self, color):
        if self.elementPlayerPosition < 4:
            self.linePlayer[self.elementPlayerPosition] = RGB(color)
            self.createColor()
            self.elementPlayerPosition += 1

    def createColor(self):
        for idx, y in enumerate(range(1,5)):
            x = 212 + (77*(y-1))
            y = 740
            pygame.draw.circle(self.screen, self.linePlayer[idx], (x,y), 13)

    def createLine(self):
        if self.linePlayerPosition <= 9:
            for i, val in enumerate(self.line):
                length = 300
                #rect = pygame.Surface((length,40))
                rectAnswer = pygame.Surface((length,40))
                
                # Clue rectangle
                pygame.draw.rect(rectAnswer, RGB('white'), rectAnswer.get_rect())

                for y, valArray in enumerate(val):
                    # Answer Space
                    self.createCircle(self.screen, valArray, 'white', 35, 35, 203+(75*y),(165+(53*i)))
                    # Clue Space
                    if y == 0 or y == 1:
                        self.createCircle(self.screen, self.answerClue[len(self.answerClue) - (i+1)][y], 'white', 14, 14, 540+(20*y),(165+(53*i)))
                    else:
                        self.createCircle(self.screen, self.answerClue[len(self.answerClue) - (i+1)][y], 'white', 14, 14, 540+(20*(y-2)),(185+(53*i)))
    def createCircle(self, container, color, fillColor, width, height, x, y):
        circle = pygame.Surface((width,height))
        circle.fill(RGB(fillColor))
        pygame.draw.circle(circle, color, (circle.get_width()/2,circle.get_height()/2), 15)
        container.blit(circle, (x,y))


    def validate(self):
        if self.linePlayer != [RGB('grey')]*4:
            self.line[(len(self.line)-1) - self.linePlayerPosition] = self.linePlayer
            self.linePlayerPosition += 1
            self.elementPlayerPosition = 0
            self.checkLineValidation()
            self.linePlayer = [RGB('grey')]*4
        if self.linePlayerPosition >= 8:
            self.endGame(False)

    
    def checkLineValidation(self):    
        clue = []
        for idx, el in enumerate(self.linePlayer):
            if self.answer[idx] == el:
                clue.append(RGB('red'))
            elif el in self.answer:
                clue.append(RGB('black'))
            else:
                clue.append(RGB('white'))

        self.answerClue[self.linePlayerPosition - 1] = clue

        if clue == [RGB('red')]*4:
            self.endGame(True)

    def endGame(self, winning):
        self.winning = winning
        time.sleep(0.5)
        self.finish = True

class Finish:
    def __init__(self, winning):
        self.finish = False
        self.winning = winning
        self.screen = ''
        self.name = ''
        self.score = ''

    def update(self):
        pygame.init()
        image = pygame.image.load("bg-wood.png")
        self.screen.blit(image, (0,0))
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',35)
        self.screen.fill((0, 9, 30))
        draw_text('MASTERMIND', game_font, (255, 255, 255), self.screen, (800/4)+50, 20)
        print('la', self.winning)
        if self.winning == True:
            draw_text('Bravo '+ self.name + ' tu as gagné', smallfont, (255, 255, 255), self.screen, 230, 250)
            draw_text('Ton score est:  '+ str(self.score), smallfont, (255, 255, 255), self.screen, 230, 280)
        else:
            draw_text('Dommage '+ self.name + ' tu as perdu', smallfont, (255, 255, 255), self.screen, 230, 250)
        pygame.display.update()

    def saveScore(self):
        data = [self.name, self.score, datetime.now()]
        with open('scores.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the data
            writer.writerow(data)

class Score:
    def __init__(self):
        self.finish = False
        self.df = pd.read_csv("scores.csv")
        self.df = self.df.sort_values(by=["score"], ascending=False)
        self.df = self.df[:7]
    def update(self):
        pygame.init()
        game_font = pygame.font.Font('mm_font.ttf',100)
        medium_font = pygame.font.SysFont('Corbel',50)
        small_font = pygame.font.SysFont('Corbel',30)
        image = pygame.image.load("bg-score.png")
        self.screen.blit(image, (0,0))
        draw_text('MASTERMIND', game_font, (255, 255, 255), self.screen, 250, 20)
        draw_text('High Score', medium_font, (255, 255, 255), self.screen, 320, 170)
        draw_text('Menu', medium_font, (255, 255, 255), self.screen, 360, 725)
        i = 0
        for idx, row in self.df.iterrows():
            y = 55*i
            if i == 0:
                color = RGB('red')
            elif i == 1:
                color = RGB('orange')
            elif i == 2:
                color = RGB('green')
            else:
                color = RGB('black')
            draw_text('#'+str(i+1), small_font, color, self.screen, 150, 330 + y)
            draw_text(str(row['name']), small_font, color, self.screen, 220, 330 + y)
            draw_text(str(row['score']), small_font, color, self.screen, 470, 330 + y)
            draw_text(str(row['date']), small_font, color, self.screen, 560, 330 + y)
            i += 1
        pygame.display.update()

    def handleGameEvent(self, mouse_pos, event):
        matching_menu_x = (360 <= mouse_pos[0] <= 360 + 100)
        matching_menu_y = (725 <= mouse_pos[1] <= 725 + 50)
        if matching_menu_x & matching_menu_y:
            self.finish = True
        pygame.display.flip()

class Welcome:
    def __init__(self):
        self.finish = False
        self.newScreen = ''

    def update(self):
        pygame.init()
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',35)
        medium_font = pygame.font.SysFont('Corbel',50)
        image = pygame.image.load("bg-1.png")
        self.screen.blit(image, (0,0))
        draw_text('MASTERMIND', game_font, (255, 255, 255), self.screen, 250, 20)
        draw_text('Let\'s play', medium_font, (255, 255, 255), self.screen, 300, 250)
        draw_text('High Scores', medium_font, (255, 255, 255), self.screen, 310, 350)
        pygame.display.update()

    def handleGameEvent(self, mouse_pos, event):
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',35)
        matching_play_x = (300 <= mouse_pos[0] <= 300 + 100)
        matching_play_y = (250 <= mouse_pos[1] <= 250 + 40)

        matching_scores_x = (310 <= mouse_pos[0] <= 310 + 50)
        matching_scores_y = (350<= mouse_pos[1] <= 350 + 40)

        input_active = True
        if matching_play_x & matching_play_y:
            self.newScreen = SecondMenu()
            self.finish = True
        if matching_scores_x & matching_scores_y:
            self.newScreen = Score()
            self.finish = True
        pygame.display.flip()

class SecondMenu:
    def __init__(self):
        self.finish = False
        self.screen = ''
        self.text = ''
        self.difficulty = 1

    def update(self):
        pygame.init()
        game_font = pygame.font.Font('mm_font.ttf',100)
        smallfont = pygame.font.SysFont('Corbel',35)
        medium_font = pygame.font.SysFont('Corbel',50)
        image = pygame.image.load("bg-1.png")
        self.screen.blit(image, (0,0))
        
        # Rectangle Input Name
        rect_text = pygame.Surface((450,40))
        pygame.draw.rect(rect_text, RGB('white'), rect_text.get_rect())
        self.screen.blit(rect_text, (180, 290))

        # Rectangle boutton Lets play
        rect_play = pygame.Surface((200,40))
        pygame.draw.rect(rect_play, RGB('red'), rect_play.get_rect())
        self.screen.blit(rect_play, (300, 500))

        pygame.display.update()      

    def handleGameEvent(self, mouse_pos, event):
        game_font = pygame.font.Font('mm_font.ttf',100)
        medium_font = pygame.font.SysFont('Corbel',50)
        smallfont = pygame.font.SysFont('Corbel',35)
        draw_text('Rentrez votre nom', smallfont, (255, 255, 255), self.screen, 300, 250)
        
        draw_text('Choisissez votre difficulté', smallfont, (255, 255, 255), self.screen, 265, 380)
        
        draw_text(self.text, smallfont, (RGB('black')), self.screen, 340, 300)

        draw_text(str(self.difficulty), smallfont, (255, 255, 255), self.screen, 400, 430)
        
        play_button = pygame.draw.rect(self.screen , RGB('white'),(350, 507, 200,50))
        draw_text('Let\'s play', smallfont, RGB('black'), self.screen, play_button.x, play_button.y)

        menu_button = pygame.draw.rect(self.screen , RGB('white'),(350, 700, 200,50))
        draw_text('Menu', smallfont, RGB('black'), self.screen, menu_button.x, menu_button.y)

        less_button = pygame.draw.rect(self.screen , RGB('white'),(350, 425, 20,50))
        draw_text('-', medium_font,  RGB('black'), self.screen, less_button.x, less_button.y)

        plus_button = pygame.draw.rect(self.screen , RGB('white'),(450, 425, 20,50))
        draw_text('+', medium_font,  RGB('black'), self.screen, plus_button.x, plus_button.y)

        input_active = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text =  self.text[:-1]
            else:
                self.text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if less_button.collidepoint(mouse_pos):
                if self.difficulty >= 1:
                    self.difficulty -= 1

            if plus_button.collidepoint(mouse_pos):
                if self.difficulty < 8:
                    self.difficulty += 1

            if play_button.collidepoint(mouse_pos):
                game = Game(self.difficulty, self.text)
                game.run()
            if menu_button.collidepoint(mouse_pos):
                menu = Welcome()
                menu.run()
        pygame.display.flip()

class Controller:
    def __init__(self, window):
        self.running = True
        self.clock = pygame.time.Clock()
        window.screen = pygame.display.set_mode((800,800))
        self.game = window

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.game.handleGameEvent(pygame.mouse.get_pos(), event)
    
    def run(self):
        while self.game.finish == False:
            self.handling_events()
            self.game.update()
            self.clock.tick(60)


# welcome = Welcome()
# welcomeScreen = Screen(welcome)
# welcomeScreen.run()

# nextPage = welcome.newScreen
# nextPageScreen = Screen(nextPage)
# nextPageScreen.run()


# score = Score()
# screenScore = Screen(score)
# screenScore.run()
menu = SecondMenu()
screenMenuBeforeGame = Screen(menu)
screenMenuBeforeGame.run()
game = Game(2,'martin')
game.name = menu.text
game.difficulty = menu.difficulty
screen = Screen(game)
screen.run()
hasWin = game.winning
finish = Finish(hasWin)
finish.score = (10 - game.linePlayerPosition)
finish.name = menu.text
finish.saveScore()
endGame = Screen(finish)
endGame.run()
