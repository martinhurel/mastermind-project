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
        self.screen = pygame.display.set_mode((800,800))
        self.clock = pygame.time.Clock()
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
        

        img = pygame.image.load('backspace.png')
        img.convert()
        delete_button = img.get_rect()
        delete_button.center = 0, 0

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

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if delete_button.collidepoint( pygame.mouse.get_pos()):
                    if self.elementPlayerPosition >= 1:
                        self.linePlayer[self.elementPlayerPosition - 1] = RGB('grey')
                        self.elementPlayerPosition -= 1

                for position in self.choices_pos:
                    matching_round_x = (position[0] - 20 <= pygame.mouse.get_pos()[0] <= position[0] + 20)
                    matching_round_y = (position[1] - 20 <= pygame.mouse.get_pos()[1] <= position[1] + 20)

                    if matching_round_x & matching_round_y:
                        index = self.choices_pos.index(position)
                        self.changeLinePlayer(COLORS[index])

                    matching_text_x = (self.text_validate[0] <= pygame.mouse.get_pos()[0] <= self.text_validate[0] + 100)
                    matching_text_y = (self.text_validate[1] <= pygame.mouse.get_pos()[1] <= self.text_validate[1] + 60)
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

    def run(self):
        while self.finish == False:
            self.update()
            self.clock.tick(60)

        pygame.display.flip()
