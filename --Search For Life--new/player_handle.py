import pygame, math
from engine import *

class Player(pygame.sprite.Sprite):
     
     def __init__(self):
          super().__init__()
          self.origin = pygame.image.load("Texture\\Player\\Prototype.png").convert_alpha()
          self.rect = self.origin.get_rect(topleft = (0,0))
          self.image = self.origin
          self.Resize()
          self.gravity = 0
     def Resize(self):
          self.width, self.height = self.image.get_width(), self.image.get_height()
          self.image = pygame.transform.scale(self.origin,(self.width, self.height))
     def Movement(self):
          global PlayerX, PlayerY, PlayerSpdY, PlayerSpdX, ScrollX, ScrollY, PlayerRect
          global PlayerRect
          self.startX = math.floor(ScrollX / TILE_S) ; self.startY = math.floor(ScrollY / TILE_S) 
          self.gravity -= 0

          
          PlayerSpdX = PlayerSpdX * 0.9
          PlayerSpdY += self.gravity

          PlayerX += PlayerSpdX 
          
          PlayerY -= PlayerSpdY
          
          self.rect = self.image.get_rect(topleft = (PlayerX, PlayerY))
          PlayerRect = self.rect
          #self.PosXRounded = math.ceil((self.rect.x - self.width)/TILE_S) ; self.PosYRounded = math.floor((self.rect.y + self.height)/TILE_S)

        #   #---Bordering so no index out of range error---
          
        #   if self.startX > (map_width - WIDTH):  ScrollX = (map_width - WIDTH)*TILE_S 
        #   if self.startX < 0: ScrollX = 0 
        #   if self.startY > (map_height - HEIGHT) : ScrollY = (map_height - HEIGHT)*TILE_S - math.floor(TILE_S/2)
        #   if self.startY < 0: ScrollY = 0 
        #   self.startX = math.floor(ScrollX / TILE_S) ; self.startY = math.floor(ScrollY / TILE_S)
        #   #---Bordering so no index out of range error---
          



          #if not int(data[self.startX + self.PosXRounded][self.startY + self.PosYRounded]) == 0: 
               #PlayerX -= PlayerSpdX 
               #PlayerSpdX = 0
          
          

        #--player collision detection
        #if (not self.chosen == 0 ) and self.rect.colliderect(self.rect, PlayerRect.bottom):
     def update(self):
          self.Movement()

player = pygame.sprite.GroupSingle() ; player.add(Player())
