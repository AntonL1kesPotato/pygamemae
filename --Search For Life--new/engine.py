import pygame, sys, json, math, random, os, subprocess
from init import * 
from map_handle import *
from os import listdir
from background import Background
from os.path import isfile, join


def RenderTiles(WIDTH, HEIGHT, sprite):
     global collidingtiles
     collidingtiles = []
     for x in range(WIDTH):
        for y in range(HEIGHT):
             sprite.update(x, y)

def GetInput():      
    global ScrollX, ScrollY, TILE_S, movex, movey ; SPEED = 2
    
    if keys[pygame.K_l]:
     ScrollX += 10 ; movex = -1 
    elif keys[pygame.K_j]:
     ScrollX -= 10 ; movex = 1
    if keys[pygame.K_i]:
         ScrollY -= 10 ; movey = 1
    if keys[pygame.K_k]: 
         ScrollY += 10 ; movey = -1
    if keys[pygame.K_w]:wheel = wheel + 1
         
    if keys[pygame.K_RIGHT]: 
        if player.sprite.PlayerSpdX < SPEED: 
              player.sprite.PlayerSpdX += (player.sprite.PlayerSpdX + 2) * 1.2
        else: player.sprite.PlayerSpdX = SPEED
        movex = 1

    if keys[pygame.K_LEFT]:
         if player.sprite.PlayerSpdX < SPEED * -1: 
              player.sprite.PlayerSpdX -= (player.sprite.PlayerSpdX + 2) * 1.2
         else: player.sprite.PlayerSpdX = SPEED*-1
         movex = -1

    if keys[pygame.K_UP]: 
         player.sprite.PlayerSpdY = 5
         movey = 1
    if keys[pygame.K_DOWN]:
         if player.sprite.PlayerSpdY < SPEED*-1: 
              player.sprite.PlayerSpdY -= (player.sprite.PlayerSpdY + 2) * 1.2
         else: player.sprite.PlayerSpdY = SPEED*-1
         movey = -1
def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("white")) 
	return fps_text
class Player(pygame.sprite.Sprite):
     
     def __init__(self):
          super().__init__()
          self.origin = pygame.image.load("Texture\\Player\\Prototype.png").convert_alpha()
          self.rect = self.origin.get_rect(topleft = (0,0))
          self.image = self.origin
          self.Resize()
          self.gravity = -0.5
          self.PlayerX = 0 ; self.PlayerY = 130
          self.PlayerSpdX = 0 ; self.PlayerSpdY = 0
     def Resize(self):
          self.width, self.height = self.image.get_width(), self.image.get_height()
          self.image = pygame.transform.scale(self.origin,(self.width, self.height))
     def Reposition(self):
          self.rect = self.image.get_rect(topleft = (self.PlayerX, self.PlayerY))
          
     def moveX(self):
          self.PlayerSpdX = self.PlayerSpdX * 0.9
          self.PlayerX += self.PlayerSpdX 
     def moveY(self):


          self.PlayerY -= self.PlayerSpdY

     def CheckCollisionX(self):
       if len(collidingtiles) != 2:
          for tile in collidingtiles:
               while self.rect.colliderect(tile):
                    if self.PlayerSpdX > 0: self.PlayerX += -1
                    else: self.PlayerX += 1
                    self.rect.x = self.PlayerX
                    self.Reposition()
                    self.PlayerSpdX = 0

     def CheckCollisionY(self):
       if len(collidingtiles) != 2:
          for tile in collidingtiles:
               while self.rect.colliderect(tile):
                    if self.PlayerSpdY > 0: self.PlayerY += -1
                    else: self.PlayerY += 1
                    self.rect.y = self.PlayerY
                    self.Reposition()
                    self.PlayerSpdY = 0

     def update(self):
          global collidingtiles, playrect
          self.moveX()
          # collidingtiles = []
          # RenderTiles(WIDTH, HEIGHT, tile)
          
          # self.Reposition()
          # self.CheckCollisionX()


          self.moveY()
          collidingtiles = []
          RenderTiles(WIDTH, HEIGHT, tile)
          self.Reposition()
          self.CheckCollisionY()
          self.rect = self.image.get_rect(topleft = (self.PlayerX, self.PlayerY))
          # if not len(collidingtiles) == 2:
          print(collidingtiles)
          playrect = self.rect

                 
                   
          #         collidingtiles.remove(tile)   
class Tile(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        global collidingtiles
        self.surf = pygame.Surface([TILE_S, TILE_S])
        self.chosen = 0 ; self.select = 0 ; self.tilenum = len(images)
        self.image = images[self.chosen]
        self.rect = self.image.get_rect(topleft = (0,0))
        collidingtiles = []
         
    
    def move(self):
        global ScrollX, ScrollY,  output, collidingtiles
        self.XPos = (self.x * TILE_S) - (ScrollX % TILE_S) ; self.YPos = (self.y * TILE_S) - (ScrollY % TILE_S)
        self.rect = self.image.get_rect(topleft = (self.XPos, self.YPos))

        self.chosen = int(data[self.x+StartX][self.y+StartY])
        self.image = pygame.transform.scale(images[self.chosen], (TILE_S, TILE_S))
        if self.rect.colliderect(player.sprite.rect) and (not self.chosen == 0):
     
               collidingtiles.append(self.rect)
               
              


                
                



                
             
        if self.rect.collidepoint(mouse): 
                self.select = wheel % self.tilenum
                self.chosen = self.select
                #self.image.set_alpha(255)
                if pygame.mouse.get_pressed()[0]:
                     data[self.x+StartX][self.y+StartY] = self.select
        elif self.chosen == 0 : output = "empty" 
       
        self.rect = (self.XPos, self.YPos)
        

        
    def update(self, xx, yy):
        self.x = xx
        self.y = yy
        self.move()

images = LoadImages("Texture\\Tiles\\")
tile = pygame.sprite.GroupSingle() ; tile.add(Tile())
background = pygame.sprite.Group() ; background.add(Background())
player = pygame.sprite.GroupSingle() ;  player.add(Player())
name = "main" 

list = str(os.listdir("Maps"))
if len(list)-2 == 0:
      answer = str(input("no file found, why did you mess with the files? put name for new file:"))
      height = int(input("put height:"))
      width = int(input("put width:"))
      MakeMap(answer, width, height)
# else: 

#      answer = str(input("Select a file from:" + list))
#      LoadMap(answer)
#      GetData(answer)
#      name = answer
data, map_height, map_width = LoadMap("main.json")

GetData("main.json")



while True:
    #--1. Get Input
    mouse = pygame.mouse.get_pos() ; keys = pygame.key.get_pressed()
    GetInput()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
             wheel += event.y
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SEMICOLON:
               SaveMap(name, data)
               answer = input("1.New file \n 2.Load file")
               try: 
                 if answer == "1":
                    name = input("say file name")
                    map_height = int(input("height of map?"))
                    map_width = int(input("width of map?"))
                    MakeMap(name, map_width, map_height)
                    SaveMap(name, data)

                 elif answer == "2":
                      list = os.listdir("Maps")
                      print(list)
                      answer = input("Which one? ")
                      if answer in list: LoadMap(answer)
                      else: print("invalid name") 
               except:
                    print("invalid input") 
        if event.type == pygame.QUIT:
            SaveMap(name, data)
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode((event.w,
                                            event.h), pygame.RESIZABLE)
            w, h = pygame.display.get_surface().get_size()
            # for background in background.sprites():
            #     background.sprites()
    tick += 1
    #TILE_S = w/10
    win.fill("sky blue")
    CenterX = w/2 ; CenterY = h/2
    WIDTH, HEIGHT = math.floor(w/TILE_S)+2, math.floor(h/TILE_S)+2
    #--2. Draw and Game Logic
    
    
     
#---Bordering so no index out of range error---
    StartX = math.floor(ScrollX / TILE_S) ; StartY = math.floor(ScrollY / TILE_S) 
    if StartX > (map_width - WIDTH):  ScrollX = (map_width - WIDTH)*TILE_S 
    if StartX < 0: ScrollX = 0 
    if StartY > (map_height - HEIGHT) : ScrollY = (map_height - HEIGHT)*TILE_S - math.floor(TILE_S/2)
    if StartY < 0: ScrollY = 0 ; 
    StartX = math.floor(ScrollX / TILE_S) ; StartY = math.floor(ScrollY / TILE_S)
#---Bordering so no index out of range error---



    for i in range(math.floor(3)):
        backindex = 0
        background.update(ScrollX, ScrollY, TILE_S , i) ; background.draw(win) ; backindex = 1
        background.update(ScrollX, ScrollY, TILE_S , i) ; background.draw(win)
    player.update()
    for x in range(WIDTH):
        for y in range(HEIGHT):
             tile.update(x, y)  
             if not output == "empty" : 
                   tile.draw(win)
             else: output = "0"
    output = 0 

    win.blit(update_fps(),(0,0))
    
    player.draw(win)
    thing = collidingtiles
    for til in thing:
      pygame.draw.rect(win,"red",  til)
    if tick % 2 != 0:
     pygame.draw.rect(win, "blue", playrect)
    pygame.display.update() ; clock.tick(60)
    
    
