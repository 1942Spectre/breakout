import pygame
from pygame.locals import *
import math
from pytmx.util_pygame import load_pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        if surf != None:
            self.image = surf
            self.rect = self.image.get_rect(topleft = pos)


class Brick(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        if surf == None:
           
            self.image = pygame.Surface((64*3, 64))  
            self.image.fill((255, 255, 255))  
            self.rect = self.image.get_rect(topleft=pos)

    def remove(self,game):
        game.brick_group.remove(self)
        game.all_sprites.remove(self)

class Ball(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.speed = 10
        self.direction = math.pi / 4 
        if surf == None:
         
            self.image = pygame.Surface((64, 64)) 
            self.image.fill((255, 255, 255)) 
            self.rect = self.image.get_rect(topleft=pos)

    def update(self, game):

        self.rect.x += self.speed * math.cos(self.direction)
        self.rect.y += self.speed * math.sin(self.direction)


        if abs(self.direction) < 0.1 or abs(self.direction - math.pi) < 0.1:
            self.direction += math.pi / 8 


        if self.rect.left <= 0 or self.rect.right >= game.width:
            self.direction = math.pi - self.direction
        if self.rect.top <= 0:
            self.direction = -self.direction


        collisions = pygame.sprite.spritecollide(self, game.paddle_group, False)
        if collisions:
            paddle = collisions[0]
            paddle_center = paddle.rect.center
            ball_center = self.rect.center


            normal = [ball_center[0] - paddle_center[0], ball_center[1] - paddle_center[1]]
            length = math.sqrt(normal[0]**2 + normal[1]**2)
            normal = [normal[0] / length, normal[1] / length]


            self.direction = math.atan2(normal[1], normal[0])


        collisions = pygame.sprite.spritecollide(self,game.brick_group, False)
        if collisions:
            brick = collisions[0]
            brick_center = brick.rect.center
            ball_center = self.rect.center


            normal = [ball_center[0] - brick_center[0], ball_center[1] - brick_center[1]]
            length = math.sqrt(normal[0]**2 + normal[1]**2)
            normal = [normal[0] / length, normal[1] / length]


            self.direction = math.atan2(normal[1], normal[0])
            brick.remove(game) 



class Paddle(Tile):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        if surf == None:

            self.image = pygame.Surface((64*6, 64)) 
            self.image.fill((255, 255, 255))  
            self.rect = self.image.get_rect(topleft=pos)

    def update(self,game):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10


        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(game.width, self.rect.right)


class Game():
    def __init__(self):
        self.width = 1920
        self.height = 1280
        self.paddle_group = pygame.sprite.Group()
        self.all_sprites  = pygame.sprite.Group()
        self.brick_group = pygame.sprite.Group()
        self.tmx_data = None
    def play(self):
        screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Breakout")
        self.tmx_data = load_pygame("level1.tmx")
        for layer in self.tmx_data.layers:
            if layer.name in ("Background"):
                for x,y,surf in layer.tiles():
                    pos = (x*32,y*32)
                    Tile(pos=pos,surf = surf, groups = self.all_sprites)
            

        for obj in self.tmx_data.objects:
            pos = obj.x,obj.y
            if obj.type == "Brick":
                brick = Brick(pos = pos, surf = obj.image, groups = self.all_sprites)
                self.brick_group.add(brick)

            elif obj.type == "Ball":
                Ball(pos = pos, surf = obj.image, groups = self.all_sprites)
            
            elif obj.type == "Paddle":
                paddle = Paddle(pos = pos, surf = obj.image, groups = self.all_sprites)
                self.paddle_group.add(paddle)



        clock = pygame.time.Clock()


        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.all_sprites.update(game)
            screen.fill((0, 0, 0))
            self.all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(100)
            
        pygame.quit()





game = Game()
game.play()