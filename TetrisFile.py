import pygame
import random
import ActualAi
import numpy as np

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:
    x = 0
    y = 0
    

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
        #print("NEW THING")

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
    def get_cord(self):
        return [self.x,self.y]


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    reward = 0
    game_over = False

    def __init__(self, height, width,n=0,score=0,record=0):
        #print('Game', n,'Score',score,'Record:',record)
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.figure = Figure(3,0)
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
        #print("Field",self.field)
    def getField(self):
        return game.field
        
    def new_figure(self):
        self.figure = Figure(3, 0)
        #print(self.figure.x)
        #print(self.field)
        return Figure(3,0)
    
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
                        self.reward -= 20
        return intersection
    def getReward(self):
        return self.reward
    def break_lines(self,flag=True):
        if flag:
            lines = 0
            for i in range(1, self.height):
                zeros = 0
                for j in range(self.width):
                    if self.field[i][j] == 0:
                        zeros += 1
                if zeros == 0:
                    lines += 1
                    for i1 in range(i, 1, -1):
                        for j in range(self.width):
                            self.field[i1][j] = self.field[i1 - 1][j]
            self.score += lines ** 2
        #print("BREAK SCORE",self.score)
        score = self.score
        self.reward += 15
        return score
        
        
       

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        #self.reward -= 1
        self.freeze()

    def go_down(self):
        
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.reward += 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
                    #print("Color")
        
        self.new_figure()
        #print(self.field)
        
        self.break_lines()
        self.state = None
        if self.intersects():
            self.state = "gameover"
            #self.reward -= 5

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation
        
    def _update_ui(self):
        screen.fill(WHITE)
        
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                        [game.x + game.zoom * (j + game.figure.x) + 1,
                                        game.y + game.zoom * (i + game.figure.y) + 1,
                                        game.zoom - 2, game.zoom - 2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

        screen.blit(text, [0, 0])
        #if game.state == "gameover":
            
         #   game.__init__(20,10)

        pygame.display.flip()
        clock.tick(fps)
    def getScore(self):
        return game.score
    def play_step(self, action):
        
        # 1. collect user input
        #move = None
        move = "pp"
        flag = False
        if flag:
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.rotate()
                        move = "rot"
                    if event.key == pygame.K_DOWN:
                        pressing_down = True
                        move = "down"
                    if event.key == pygame.K_LEFT:
                        game.go_side(-1)
                        move = "left"
                    if event.key == pygame.K_RIGHT:
                        game.go_side(1)
                        move = "right"
                    if event.key == pygame.K_SPACE:
                        game.go_space()
                    if event.key == pygame.K_ESCAPE:
                        game.__init__(20, 10)
            #print(move)
        
        # 2. move
        game.go_down()
        #score = self.break_lines(False)
        movement = self._move(action) # update the head
        #print(move,movement)
        if flag:
            if move == movement and move:
                self.reward += 5
                print("correct")
            else:
               self.reward -= 0.3
        #print("reward:", self.reward)
        #print("GETSCORE",self.getScore())
        #print(game.field)
        # 3. check if game over
        self.game_over = False
        self.score = self.getScore()
        if game.state == "gameover":
            reward = self.reward
            self.game_over = True
            reward -= 10
            self.reward -= 10
            reward += 25*self.score
            self.reward += 25*self.score
            
            
            self.reward = 0
            print(self.score)
            variable = self.score
            
            game.state = "start"
            game.__init__(20,10)
            print(self.score)
            return reward, self.game_over, self.score
        
        
        
        # 6. return game over and score
        self._update_ui()
        
        return self.reward, self.game_over, self.score
    def check_done(self):
        if self.state == "gameover":
            self.game_over = True
        return self.game_over
    def _move(self,action):
        
        if np.array_equal(action,[1,0,0,0]):
            game.rotate()
            move = "rot"
        elif np.array_equal(action,[0,1,0,0]):
            game.go_side(-1)
            move = "left"
        elif np.array_equal(action,[0,0,1,0]):
            game.go_side(1)
            move = "right"
        elif np.array_equal(action,[0,0,0,1]):
            game.go_down()
            move = "down"
        return move
        
        

            
            


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

