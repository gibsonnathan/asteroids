import pygame, random, math
from enum import Enum

class Color(Enum):
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Game:
    
    def __init__(self, title, width, height, fps):
        self.fps = fps
        self.width = width
        self.height = height
        pygame.init()
        pygame.display.set_caption(title)
        self.display = pygame.display.set_mode((self.width, self.height))
        self.exit = False
        self.clock = pygame.time.Clock()
        self.ship = Ship(self, 10)
        self.bullets = []
        self.asteroids = []
        self.kills = 0
        
    def start(self):
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.ship.change_direction(Direction.LEFT)
                    if event.key == pygame.K_RIGHT:
                        self.ship.change_direction(Direction.RIGHT)
                    if event.key == pygame.K_SPACE:
                        self.bullets.append(Bullet(self, self.ship.pos1[0], self.ship.pos1[1], 10))
                        
            self.display.fill(Color.BLACK.value)
            self.ship.draw()
            if random.randint(0, 20) == 2:
                self.asteroids.append(Asteroid(self))
            
            for b in self.bullets:
                if b.pos[1] < 0:
                    self.bullets.remove(b)
                else:
                    b.draw()
                    
            for a in self.asteroids:
                if a.pos1[1] > self.height:
                    self.asteroids.remove(a)
                else:
                    a.draw()
                        
            for a in self.asteroids:
                for b in self.bullets:
                    if pygame.Rect(b.pos[0], b.pos[1], 2, 2).colliderect(pygame.Rect(a.pos1[0], a.pos1[1], 15, 15)):
                        self.asteroids.remove(a)
                        self.bullets.remove(b)
                        self.kills += 1

            font = pygame.font.Font(None,30)
            label = font.render("Kills: " + str(self.kills), 1, (0,255,0))
            self.display.blit(label, (self.width - 100, 0))

            pygame.display.update()  
            self.clock.tick(self.fps)
            
class Asteroid():
    
    LINE_THICKNESS = 1
    
    def __init__(self, game):
        self.game = game
        self.pos1 = [random.randint(0, self.game.width), random.randint(0, self.game.height / 20)]
        self.pos2 = [self.pos1[0], self.pos1[1] + 10]
        self.pos3 = [self.pos1[0] + 10, self.pos1[1]]
        self.pos4 = [self.pos1[0] + 10, self.pos1[1] + 10]
        
    
    def move(self):
        self.pos1 = [self.pos1[0], self.pos1[1] + 1]
        self.pos2 = [self.pos2[0], self.pos2[1] + 1]
        self.pos3 = [self.pos3[0], self.pos3[1] + 1]
        self.pos4 = [self.pos4[0], self.pos4[1] + 1]
  
    
    def draw(self):
        self.move()
        pygame.draw.polygon(self.game.display, Color.GREEN.value,
                            [self.pos1, self.pos2, self.pos3, self.pos4], self.LINE_THICKNESS)

class Ship():
    
    LINE_THICKNESS = 1
    
    def __init__(self, game, speed):
        self.game = game
        self.speed = speed
        self.pos1 = [self.game.width / 2, self.game.height - 50]
        self.pos2 = [self.pos1[0] - 5, self.pos1[1] + 20]
        self.pos3 = [self.pos1[0] + 5, self.pos1[1] + 20]
        self.direction = Direction.LEFT
        
    def change_direction(self, direction):
        self.direction = direction
       
    def move(self, direction):
        if (self.pos1[0] + self.pos2[0] + self.pos3[0]) / 3 > self.game.width:
            self.pos1 = [0, self.game.height - 50]
            self.pos2 = [self.pos1[0] - 5, self.pos1[1] + 20]
            self.pos3 = [self.pos1[0] + 5, self.pos1[1] + 20]
        if (self.pos1[0] + self.pos2[0] + self.pos3[0]) / 3 < 0:
            self.pos1 = [self.game.width, self.game.height - 50]
            self.pos2 = [self.pos1[0] - 5, self.pos1[1] + 20]
            self.pos3 = [self.pos1[0] + 5, self.pos1[1] + 20]
            
        if direction == Direction.LEFT:
            self.pos1[0] = self.pos1[0] - self.speed
            self.pos2[0] = self.pos2[0] - self.speed
            self.pos3[0] = self.pos3[0] - self.speed
        else:
            self.pos1[0] = self.pos1[0] + self.speed
            self.pos2[0] = self.pos2[0] + self.speed
            self.pos3[0] = self.pos3[0] + self.speed
            
    def draw(self):
        self.move(self.direction)
        pygame.draw.polygon(self.game.display, Color.GREEN.value,
                            [self.pos1, self.pos2, self.pos3], self.LINE_THICKNESS)
        
    
class Bullet():
    
    def __init__(self, game, posx, posy, speed):
        self.game = game
        self.pos = [posx, posy]
        self.speed = speed
                
    def move(self):
        self.pos[1] -= self.speed
    
    def draw(self):
        self.move()
        pygame.draw.rect(self.game.display, Color.RED.value, (self.pos[0], self.pos[1], 2, 2))
    
def main():
    
    TITLE = 'HELLLOO'
    X_SIZE = 600
    Y_SIZE = 600
    FPS = 30
    
    g = Game(TITLE, X_SIZE, Y_SIZE, FPS).start()
    
    
main()