import random
import time
import pygame
from pygame.locals import *
SIZE =40
BACKGROUND_COLOR=(10, 30, 50)
class Snake:
    def __init__(self, parent_screen, length):
        self.length=length
        self.parent_screen=parent_screen
        self.block = pygame.image.load("static/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction ='up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction == 'up':
            self.y[0] -=SIZE
        if self.direction == 'down':
            self.y[0] +=SIZE
        if self.direction == 'left':
            self.x[0] -=SIZE
        if self.direction == 'right':
            self.x[0] +=SIZE
        self.draw()

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("static/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24) * SIZE
        self.y = random.randint(1,18) * SIZE

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and apple")
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake=Snake(self.surface, 1)
        self.snake.draw()
        self.app=Apple(self.surface)
        self.app.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def exit1(self):
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            return True
        return False

    def play_sound(self):
        print("sound played")
        ding = pygame.mixer.Sound("static/Ding-sound-effect.mp3")
        pygame.mixer.Sound.play(ding)


    def display_score(self):
        font= pygame.font.SysFont('arial',30)
        score= font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score,(800,10))

    def play(self):
        self.snake.walk()
        self.app.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.app.x, self.app.y):
            self.snake.increase_length()
            self.app.move()


        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                raise "game over"

        if self.exit1():
            raise "game over"


    def game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (300, 300))
        line= font.render(f" To play game again ENTER" , True, (255, 255, 255))
        self.surface.blit(line, (300, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.app = Apple(self.surface)

    def run(self):
        r = True
        pause =False
        while r:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        r = False
                    if event.key == K_RETURN:
                        pause =False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    r = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause =True
                self.reset()
            time.sleep(0.5)

            if self.snake.length >= 3:
                time.sleep(0.1)


if __name__ == "__main__":
    game=Game()
    game.run()


