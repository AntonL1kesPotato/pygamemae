import pygame
class Background(pygame.sprite.Sprite):
      def __init__(self):
          
            super().__init__()
            self.backindex = 0
            self.list =  [pygame.image.load("Texture\\Backgrounds\\City2.png").convert_alpha(), pygame.image.load("Texture\\Backgrounds\\City1.png").convert_alpha()]
            self.image = self.list[self.backindex] 
            self.rect = self.image.get_rect(topleft = (0,0))
            self.resize()
      def resize(self):
           self.height = self.image.get_height() ; self.width = self.image.get_width() 
           self.image = pygame.transform.scale(self.image, (self.width, self.height))
      def position(self, i):
            if self.backindex == 0: self.multi = 4
            else: self.multi = 8
            
            self.image = self.list[self.backindex]
            self.height = self.image.get_height() * (self.TILE_S / 8); self.width = self.image.get_width() * (self.TILE_S / 8)
            self.rect = self.image.get_rect(center = ((self.width * i)-self.ScrollX/(self.TILE_S/self.multi),0-self.ScrollY/(self.TILE_S/self.multi)))
            
      def update(self, ScrollX, ScrollY, TILE_S, idx):
            self.ScrollX = ScrollX
            self.ScrollY = ScrollY
            self.TILE_S = TILE_S
            self.backindex = idx % 2
            self.position(idx)