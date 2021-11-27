import random

colors = ['blue', 'red', 'green', 'yellow', 'purple', 'white', 'orange']
class Game():

    def __init__(self, difficulty = 2):
        self.difficulty = difficulty
        self.solution = random.sample(colors,4)
        self.guesses = 0
        self.right_places = 0

    def play(self):
        while self.guesses <= 10 and self.right_places != 4:
            player_input = random.sample(colors,4)
            guess = Guess(player_input)
            print('Guess number',self.guesses,':',guess.guess)
            self.right_places = guess.compare(self)[0]
        print(self.solution)

class Guess():
    
    def __init__(self, guess):
        self.guess = guess

    def compare(self, game):
        right_place = 0
        right_color = 0
        game.guesses += 1
        for i in self.guess:
            if i == game.solution[self.guess.index(i)]:
                right_place += 1
            elif i in game.solution:
                right_color += 1
        return right_place, right_color
        

game = Game()
game.play()
