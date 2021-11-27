import pygame

colors = ['red', 'yellow', 'blue', 'green', 'purple', 'pink', 'orange', 'gray']
colorbox_x, colorbox_y = 354, 378
color_offset_x, color_offeset_y = 24, 18
white = pygame.Color('white')
brown = (89,62,37)
center = 300

class Window:
    def __init__(self, controller):
        pygame.init()
        self.controller = controller
        self.window = pygame.display.set_mode((600, 600))
        self.clock = clock = pygame.time.Clock()
        pygame.display.set_caption('Mastermind')
        self.display('ressources/background.png')
        
    def display(self, file, coord = (0,0)):
        image = pygame.image.load(file)
        return self.window.blit(image, coord)
    
    def drawText(self, text, size, color, x, y, centered = True):
        font = pygame.font.Font("ressources/upheavtt.ttf", size)
        textobj = font.render(text, 1, color)
        if centered:
            x = x - textobj.get_width()/2
        self.window.blit(textobj, (x, y))
        return pygame.Rect(x, y, textobj.get_width(), textobj.get_height())
    
    def handleInputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.controller.running = False
                return 
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return event
            self.update()
            
    def update(self):
        self.clock.tick(60)
        pygame.display.update()

class Menu(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        center = 300
        self.drawText('Mastermind', 90, white, center,20)
        self.drawText('Main Menu', 60, white, center, 150)
        self.play = self.drawText('Play', 50, white, center, 280)
        self.high_scores = self.drawText('High Scores', 50, white, center, 380)
        self.exit = self.drawText('Exit', 50, white, center, 480)
        
    def handleClick(self):
        event = super().handleInputs()
        if event != None and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()      
            if self.play.collidepoint(mouse_pos):
                self.controller.playing = True
                self.controller.newGame()
            if self.high_scores.collidepoint(mouse_pos):
                self.controller.showHS()
            if self.exit.collidepoint(mouse_pos):
                self.controller.running = False

class Board(Window):
    def __init__(self, controller):
        Window.__init__(self, controller)
        self.board = self.display('ressources/board.png', (17,30))
        self.color_box = self.display('ressources/color_box.png', (colorbox_x, colorbox_y)) # à changer
        self.color_sprites = self.displayColorChoices()
        self.guess_box = pygame.Rect(61, 528, 174, 33)
        self.guess_slots = ['empty']*4
        self.submit_button = self.display('ressources/submit.png', (360,522))
        self.display('ressources/score_board.png', (354, 30))

    def displayColorChoices(self):
        color_sprites = []
        for i in range(len(colors)):
            file = 'ressources/'+colors[i]+'.png'
            x, y = colorbox_x + color_offset_x, colorbox_y + color_offeset_y
            if i < 4:
                color_sprites.append(self.display(file, (x + 48*(i%4), y)))
            else:
                color_sprites.append(self.display(file, (x + 48*(i%4), y + 48)))
        return color_sprites
        
    def handleClick(self):
        event = super().handleInputs()
        self.displayTimer()
        if event != None and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()    
            if self.color_box.collidepoint(mouse_pos):
                self.colorSelected(mouse_pos)
            if self.guess_box.collidepoint(mouse_pos):
                self.removeColor(mouse_pos)
            if self.submit_button.collidepoint(mouse_pos):
                if not 'empty' in self.guess_slots : 
                    self.controller.submit(self.guess_slots)
                    self.guess_slots = ['empty']*4
            if self.controller.playing == True:
                self.displayGuess()
        
        
    def colorSelected(self, mouse_pos):
        for index, color_rect in enumerate(self.color_sprites):
            if color_rect.collidepoint(mouse_pos) and 'empty' in self.guess_slots :
                for idx, slot in enumerate(self.guess_slots):
                    if slot == 'empty': 
                        self.guess_slots[idx] = colors[index]
                        break
                
    def removeColor(self, mouse_pos):
        for i in range(4):
            x, y = 60, 528
            if pygame.Rect(x + 48*i, y, 30, 30).collidepoint(mouse_pos):
                self.guess_slots[i] = 'empty'
    
    def displayGuess(self):
        for index, color in enumerate(self.guess_slots):
            x, y = 60, 528
            file = 'ressources/'+color+'.png'
            self.display(file, (x + 48*index, y))
            
    def displayTriesAndClues(self, tries, clues):
        for i, clue in enumerate(reversed(clues)):
            right_color, all_right = clue[0], clue[1]
            x, y = 180, 474 - 42*i
            self.display('ressources/right_color.png', (x + 19 * right_color, y))
            self.display('ressources/all_right.png', (x + 19 * all_right, y))

        self.display('ressources/board.png', (17,30))

        for i, row in enumerate(reversed(tries)) :
            for index, color in enumerate(row) :
                x, y = 60, 474 - 42*i
                file = 'ressources/'+color+'.png'
                self.display(file, (x + 48*index, y))

    def displaySolution(self):
        for index, color in enumerate(self.controller.game.solution):
            x, y = 60, 43
            file = 'ressources/'+color+'.png'
            self.display(file, (x + 48*index, y))

    def displayEndScreen(self, result):
        self.displaySolution()
        subitting_name = True
        name = ''
        score = self.controller.getScore()
        while subitting_name:
            self.display('ressources/score_board.png', (354, 30))
            self.drawText(result, 35, brown, 465, 50)
            self.drawText('Score', 28, brown, 470, 130)
            self.drawText(score, 35, brown, 470, 160)
            self.drawText('Enter name :', 28, brown, 470, 210)
            self.drawText('Then press ENTER', 13, brown, 470, 235)
            textrect = self.drawText(name, 35, brown, 470, 255)
            self.update()
            event = super().handleInputs()
            if event != None and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    subitting_name = False
                    self.controller.newHighScore(name)
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10:
                    name += event.unicode

    def displayTimer(self):
        self.display('ressources/score_board.png', (354, 30))
        timer = self.controller.getTimer()
        minutes = 0 if timer < 60 else int(timer/60)
        seconds = int(timer)%60
        timer_formatted = str(minutes) + ' : ' + str(seconds)
        self.drawText(timer_formatted, 35, brown, 465, 50)
                    
class HighScores(Window):
    def __init__(self, controller, high_scores):
        Window.__init__(self, controller)
        self.drawText('Mastermind', 90, white, center, 20)
        self.drawText('High Scores', 60, white, center, 150)
        self.menu_button = self.drawText('Return to menu', 40, white, center, 530)
        self.high_scores = high_scores
        self.displayHS()
        
    def handleClick(self):
        event = super().handleInputs()
        if event != None and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.menu_button.collidepoint(mouse_pos):
                self.controller.backToMenu()

    def displayHS(self):
        for index, row in enumerate(self.high_scores[:5]):
            self.drawText(row[2][:11], 30, white, 50, 250 + 50*index, centered=False)
            self.drawText(row[0], 30, white, 250, 250 + 50*index, centered=False)
            self.drawText(row[1], 30, white, 460, 250 + 50*index, centered=False)