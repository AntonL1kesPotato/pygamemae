import pygame, os
pygame.init() 
win = pygame.display.set_mode((602, 448), pygame.RESIZABLE, vsync=1) ; pygame.display.set_caption('Search For Life')
clock = pygame.time.Clock() ; tick = pygame.time.get_ticks() ; w, h = pygame.display.get_surface().get_size()
map_width = 200
map_height = 300
backindex = 0
wheel = 0 ; output = 0
game_type = "edit"
PlayerRect = pygame.image.load("Texture\\Player\\Prototype.png").convert_alpha().get_rect(center = (0,0))
font = pygame.font.SysFont("System" , 18 , bold = True)
TILE_S = 32 ; ScrollX, ScrollY = TILE_S, TILE_S 
StartX = 0 ; StartY = 0


def LoadImages(path):
     global images
     images = []
     
     for file in os.listdir("Texture\\Tiles"):
          images.append(pygame.image.load(str(path) + file ).convert_alpha())
     return images
          # answer = input("is" + file + "a background texture? \n 1.Yes 0.No")

          # with open('Texture\\Tiles\\data.json', 'w') as datafile:
          #           json.dump(data, datafile)
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