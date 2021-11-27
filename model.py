import random
import time

colors = ['red', 'yellow', 'blue', 'green', 'purple', 'pink', 'orange', 'gray']

class Game:
    def __init__(self):
        self.solution = random.sample(colors,k=4)
        self.tries = [['empty']*4]*10
        self.tries_left = 10
        self.clues = [[0,0]]*10
        self.game_over = False
        self.win = False
        self.start_time = time.time()

    def generateClues(self, guess):
        all_right, right_color = 0, 0

        for index, color in enumerate(guess):
            if color in self.solution:
                right_color += 1
            if self.solution[index] == color:
                all_right += 1
        return [right_color, all_right]

    def appendGuess(self, guess):
        if self.tries_left > 0:
            print(self.solution)
            self.tries[self.tries_left - 1] = guess
            self.clues[self.tries_left - 1] = self.generateClues(guess)
            if guess != self.solution: # can be improved
                self.tries_left -= 1
                if self.tries_left == 0:
                    self.game_over = True
            else : 
                self.win = True
            self.score = int(50 * (self.tries_left+1))
        else :
            self.game_over = True