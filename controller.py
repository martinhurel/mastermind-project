from model import Game
from views import Menu, Board, HighScores
from datetime import datetime
import time
import csv

class EventManager:
    def __init__(self):
        self.running = True
        self.playing = False
        self.view = Menu(self)
        pass
    
    def newGame(self):
        self.game = Game()
        self.view = Board(self)
        self.playing = True

    def newHighScore(self, name):
        if name != '':
            with open('high_scores.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow([name, self.score, datetime.now()])
        self.showHS()
    
    def showHS(self):
        high_scores = []
        try :
            with open('high_scores.csv', 'r', encoding='UTF8') as f:
                for row in f:
                    high_scores.append((row.strip()).split(','))
        except : 
            high_scores = []
        high_scores.sort(key= lambda x: x[2], reverse=True)
        high_scores.sort(key= lambda x: int(x[1]), reverse=True) # Sorts high_scores by second element -> Score
        self.view = HighScores(self, high_scores)
        
    def backToMenu(self):
        self.view = Menu(self)
        
    def submit(self, guess):
        self.game.appendGuess(guess)
        self.view.displayTriesAndClues(self.game.tries, self.game.clues)
        if self.game.win:
            self.view.displayEndScreen('You win !')
            self.playing = False
        elif self.game.game_over:
            self.view.displayEndScreen('Game Over')
            self.playing = False

    def getTimer(self):
        timer = time.time() - float(self.game.start_time)
        return timer

    def getScore(self):
        score = str(int(self.game.score / (self.getTimer()/1200)))
        self.score = score
        return score