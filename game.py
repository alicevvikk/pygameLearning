
import pygame
from sys import exit
import random

pygame.init()

class CLS:
    BLACK = (0,0,0)
    RED = (255,0,0)
    WHITE = (255,255,255)

class DIR:
    STAND = 0
    RIGHT = 1 
    LEFT = 2
    JUMP = 3 
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stand = pygame.image.load('player_stand.png').convert_alpha()
        self.walk1 = pygame.image.load('player_walk_1.png').convert_alpha()
        self.walk2 = pygame.image.load('player_walk_2.png').convert_alpha()
        self.jump_ = pygame.image.load('jump.png').convert_alpha()
        self.movements = [self.stand, self.walk1, self.walk2, self.jump_]
        self.image = self.stand
        self.vel = 3
        self.gravity = 5
        self.rect = self.image.get_rect(midbottom= (50, 300))
        self.current = 0
        self.dir = DIR.RIGHT
        self.health = 5
    
    def incrementCurrent(self):
        if self.dir == DIR.STAND: self.current = 0
        else:
            if self.current >= 3: self.current = 0
            else: self.current += 0.1
        self.image = self.movements[int(self.current)]
    
    def update(self, dir):
        if self.dir != DIR.JUMP:
            if dir != DIR.JUMP:
                self.incrementCurrent()
                self.dir = dir
            else:
                self.dir = dir
                self.jump()
        self.jump()

    def jump(self):
        if self.dir == DIR.JUMP:
            self.rect.y = self.rect.y - self.gravity
            self.gravity -= 0.1
            
            if self.rect.y >= 217:
                self.gravity = 5
                self.rect.y = 217
                self.dir = DIR.STAND
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.current = 0
        self.vel = 3
        self.dir = DIR.LEFT
        self.enemies = []
    
    def update(self):
        if self.enemies:
            if self.current > 1: self.current = 0
            else: self.current += 0.05
            self.image = self.enemies[int(self.current)]    
        self.move()

    def move(self):
        if self.rect.midright[0] < 0: self.rect.x = 800
        else: self.rect.x -= self.vel

class Fly(Enemy):
    def __init__(self):
        super().__init__()
        self.enemy1 = pygame.image.load('fly1.png').convert_alpha()
        self.enemy2 = pygame.image.load('fly2.png').convert_alpha()
        self.enemies = [self.enemy1, self.enemy2]
        self.image = self.enemy1 
        self.rect =self.image.get_rect(midbottom = (1000, 200))
        

class Snail(Enemy):
    def __init__(self):
        super().__init__()
        self.enemy1 = pygame.image.load('snail1.png').convert_alpha()
        self.image = self.enemy1 
        self.rect =self.image.get_rect(midbottom = (1000, 300))

class Background(pygame.sprite.Sprite):
    def __init__(self, obj=None ,path=None, x=0, y=0):
        super().__init__()
        self.obj = obj
        self.path =path
        self.image = obj if obj else pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x,y ))
        self.dir = DIR.RIGHT
    
    def update(self, dir):
        self.dir = dir
        if self.dir == DIR.RIGHT:
            self.move()

    def move(self):
        if self.dir != DIR.STAND and self.dir != DIR.JUMP:
            self.rect.x -= 1
            if self.rect.x < - 790:
                self.rect.x = 800

class Game:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 400
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        
        self.bgs = pygame.sprite.Group()
        self.bgs.add(Background(path="ground.png", x=0, y=300), Background(path="ground.png", x=791,y=300),
                    Background(path="Sky.png"), Background(path="Sky.png", x=800, y=0))

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.enemy = pygame.sprite.Group()
        self.enemy.add(Snail())
        self.score = 0
    
    def handle_update(self, dir):
        self.player.update(dir)
        self.bgs.update(dir)
        self.enemy.update()
        for en in self.enemy:
            if en.rect.x < 0:
                self.enemy.remove(en)
                self.enemy.add(random.choice((Snail(), Fly())))

    
    def show_score(self):
        pass

    def handle_collisions(self):
        lamela = pygame.sprite.spritecollide(self.player.sprite, self.enemy, False)
        if lamela: 
            self.enemy.remove(lam for lam in lamela)
            self.enemy.add(random.choice((Snail(), Fly())))
    

    def run(self):
        dir = DIR.STAND
        active = 1
        IS_PAUSE = 0
        enemy_timer = pygame.USEREVENT + 1
        #pygame.time.set_timer(enemy_timer, 3000)

        while active:
            
            dir = DIR.RIGHT
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        IS_PAUSE = not IS_PAUSE
                #if event.type == enemy_timer:
                    #self.enemy.add(Snail())
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]: dir = DIR.RIGHT
            elif keys[pygame.K_SPACE]: dir = DIR.JUMP
            else: 
                if dir != DIR.JUMP:
                   dir = DIR.STAND
                   
            self.screen.fill(CLS.BLACK)

            self.bgs.draw(self.screen)
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            self.handle_collisions()
            if not IS_PAUSE:
                self.handle_update(dir)
            pygame.display.flip()

game = Game()

if __name__=="__main__":
    game.run()