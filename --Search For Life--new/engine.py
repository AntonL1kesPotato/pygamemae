import pygame, sys, json, math, random, os, subprocess
pygame.init() 
win = pygame.display.set_mode((602, 448), pygame.RESIZABLE, vsync=1) ; pygame.display.set_caption('Search For Life')
clock = pygame.time.Clock() ; tick = pygame.time.get_ticks() ; w, h = pygame.display.get_surface().get_size()
map_width = 1000
map_height = 1000
backindex = 0
wheel = 0 ; output = 0
game_type = "edit"
PlayerRect = pygame.image.load("Texture\\Player\\Prototype.png").convert_alpha().get_rect(center = (0,0))
font = pygame.font.SysFont("System" , 18 , bold = True)
TILE_S = 32 ; ScrollX, ScrollY = TILE_S, TILE_S 
StartX = 0 ; StartY = 0
KEY_PRESSED = 0

#if game_type == "edit":
def collision_test(rect, tiles):
     collisions = []
     for tile in tiles: 
          if pygame.rect.colliderect(tile):
               collisions.append(tile)
     return collisions

def move(rect, movex, movey, tiles):
     rect.x += movex
     collisions = collision_test(rect, tiles)
     for tile in collisions:
          if movex > 0:
           rect.right = tile.left
           if movex < 0:
                rect.left = tile.right
          if movey > 0:
           rect.bottom = tile.top
           if movey < 0:
                rect.top = tile.bottom
     return rect
def MakeMap():
         global data
         data = [[]]
         for x in range(map_width):
            data.append([])
            for y in range(map_height) : 
               data[x].append(str(0))       
def LoadMap():
          global data

          with open('map.json') as score_file:
             data = json.load(score_file) 
def GetInput():      
    global ScrollX, ScrollY, TILE_S ; SPEED = 2
    if keys[pygame.K_l]:ScrollX += 10 
    if keys[pygame.K_j]:ScrollX -= 10 
    if keys[pygame.K_i]:ScrollY -= 10 
    if keys[pygame.K_k]: ScrollY += 10
    if keys[pygame.K_w]:wheel = wheel + 1
    # if keys[pygame.K_UP]:TILE_S += 1
    # if keys[pygame.K_DOWN]:TILE_S -= 1
         
    if keys[pygame.K_RIGHT]: 
        if player.sprite.PlayerSpdX < SPEED: 
              player.sprite.PlayerSpdX += (player.sprite.PlayerSpdX + 2) * 1.2
        else: player.sprite.PlayerSpdX = SPEED
        KEY_PRESSED = "RIGHT"

    if keys[pygame.K_LEFT]:
         if player.sprite.PlayerSpdX < SPEED * -1: 
              player.sprite.PlayerSpdX -= (player.sprite.PlayerSpdX + 2) * 1.2
         else: player.sprite.PlayerSpdX = SPEED*-1
         KEY_PRESSED = "LEFT"

#     if keys[pygame.K_UP]: 
#         if player.sprite.PlayerSpdY < SPEED: 
#               player.sprite.PlayerSpdY += (player.sprite.PlayerSpdY + 2) * 1.2
#         else: player.sprite.PlayerSpdY = SPEED
    if keys[pygame.K_UP]: 
         player.sprite.PlayerSpdY = 5
         KEY_PRESSED = "UP"
    if keys[pygame.K_DOWN]:
         if player.sprite.PlayerSpdY < SPEED*-1: 
              player.sprite.PlayerSpdY -= (player.sprite.PlayerSpdY + 2) * 1.2
         else: player.sprite.PlayerSpdY = SPEED*-1
         KEY_PRESSED = "DOWN"
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
     def Movement(self):
          global ScrollX, ScrollY 
          
     def moveX(self):
          self.PlayerSpdX = self.PlayerSpdX * 0.9
          self.PlayerX += self.PlayerSpdX 
     def moveY(self):
          self.PlayerY -= self.PlayerSpdY
          self.PlayerSpdY += self.gravity

     def update(self, type):
          self.rect = self.image.get_rect(topleft = (self.PlayerX, self.PlayerY))
          if type == "x": self.moveX()
          elif type == "y": self.moveY()
          

          self.Movement()
class Background(pygame.sprite.Sprite):
      def __init__(self):
          
            super().__init__()
            self.list =  [pygame.image.load("Texture\\Backgrounds\\City2.png").convert_alpha(), pygame.image.load("Texture\\Backgrounds\\City1.png").convert_alpha()]
            self.image = self.list[backindex] 
            self.rect = self.image.get_rect(topleft = (0,0))
            self.resize
      def resize(self):
           self.height = self.image.get_height() ; self.width = self.image.get_width() 
           self.image = pygame.transform.scale(self.image, (self.width * 5, self.height * 5))
           print('did it')
      def position(self, i):
            if backindex == 0: self.multi = 4
            else: self.multi = 8
            
            self.image = self.list[backindex]
            self.height = self.image.get_height() * (TILE_S / 8); self.width = self.image.get_width() * (TILE_S / 8)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

            


            self.rect = self.image.get_rect(center = ((self.width * i)-ScrollX/(TILE_S/self.multi),(w/4)-ScrollY/(TILE_S/self.multi)))
            
      def update(self, i):
            self.position(i)
class Tile(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface([TILE_S, TILE_S])
        self.tiles = [pygame.image.load("Texture\\Tiles\\empty.png").convert_alpha(), pygame.image.load("Texture\\Tiles\\dirt.png").convert_alpha(), pygame.image.load("Texture\\Tiles\\grass.png").convert_alpha(),pygame.image.load("Texture\\Tiles\\selectedtile.png").convert_alpha() ]
        self.chosen = 0 ; self.select = 0 ; self.tilenum = len(self.tiles)
        self.image = self.tiles[self.chosen]
        self.rect = self.image.get_rect(topleft = (0,0))
    
    def move(self):
        global ScrollX, ScrollY,  output
        self.XPos = (x * TILE_S) - (ScrollX % TILE_S) ; self.YPos = (y * TILE_S) - (ScrollY % TILE_S)
        self.rect = self.image.get_rect(topleft = (self.XPos, self.YPos))

        self.chosen = int(data[x+StartX][y+StartY])
     
        if self.rect.colliderect(player.sprite.rect) and (not self.chosen == 0):
            
               if check == "y":
                 while self.rect.colliderect(player.sprite.rect):
                   if   abs(player.sprite.rect.bottom - self.rect.top) < 5: player.sprite.PlayerY -= 1
                   elif abs(player.sprite.rect.top - self.rect.bottom) < 5: player.sprite.PlayerY += 1
                   player.update("")
                   player.sprite.PlayerSpdY = 0
               elif check == "x":
                while self.rect.colliderect(player.sprite.rect):
                   if   abs(player.sprite.rect.left - self.rect.right) < 5: player.sprite.PlayerX -= 1
                   elif abs(player.sprite.rect.right - self.rect.left) < 5: player.sprite.PlayerX += 1
                   player.update("")
                   player.sprite.PlayerSpdX = 0
              
          #     
                
          #      #  if abs(player.sprite.rect.bottom - self.rect.top) < 5: #bottom side
          #       player.sprite.Movement()
          #     


                
                



                
             
        if self.rect.collidepoint(mouse): 
                self.select = wheel % self.tilenum
                self.chosen = self.select
                #self.image.set_alpha(255)
                if pygame.mouse.get_pressed()[0]:
                     data[x+StartX][y+StartY] = self.select
        elif self.chosen == 0 : output = "empty" 
       
        self.rect = (self.XPos, self.YPos)
        self.image = pygame.transform.scale(self.tiles[self.chosen], (TILE_S, TILE_S)) 

        
    def update(self):
        self.move()

tile = pygame.sprite.GroupSingle() ; tile.add(Tile())
background = pygame.sprite.Group() ; background.add(Background())
player = pygame.sprite.GroupSingle() ;  player.add(Player()) 


LoadMap()
while True:
    #--1. Get Input
    mouse = pygame.mouse.get_pos() ; keys = pygame.key.get_pressed()
    GetInput()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
             wheel += event.y
        if event.type == pygame.QUIT:
            with open('map.json', 'w') as score_file:
                json.dump(data, score_file)
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            w, h = pygame.display.get_surface().get_size()
            # for background in background.sprites():
            #     background.sprites()
    tick += 1
    #TILE_S = w/40
    win.fill("sky blue")
    CenterX = w/2 ; CenterY = h/2
    WIDTH, HEIGHT = math.floor(w/TILE_S)+2, math.floor(h/TILE_S)+2
    #--2. Draw and Game Logic


    check = "x"
    player.update(check)
    for x in range(WIDTH): 
         for y in range(HEIGHT): tile.update()  
    check = "y"
    player.update(check)
    for x in range(WIDTH): 
         for y in range(HEIGHT): tile.update()  
        


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
        background.update(i) ; background.draw(win) ; backindex = 1
        background.update(i) ; background.draw(win)

    for x in range(WIDTH):
        for y in range(HEIGHT):
             tile.update()  
             if not output == "empty" : 
                   tile.draw(win)
             else: output = "0"
    output = 0

    win.blit(update_fps(),(0,0))
    player.draw(win)
    
    

    pygame.display.update() ; clock.tick(60)
    
    
