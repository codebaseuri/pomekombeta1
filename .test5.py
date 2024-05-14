from typing import Iterable
import pygame
from pygame.sprite import AbstractGroup
import pytmx
screen_width,screen_height=1280,720

# Player class
class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen=pygame.display.get_surface()
        self.offset=pygame.Vector2(100,100)
    
    def drraw(self,player):
    
        #self.offset.x=player.rect.center[0]
        #self.offset.y=player.rect.center[1]
        for sprite in self:
            self.screen.blit(sprite.image,sprite.rect.topleft+self.offset)
            
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        
#E:\final_networking_project
#"E:\final_networking_project\
        light_blue=(17,219,255)
        self.image = pygame.image.load(r"assets\image_24.png").convert_alpha()
        self.image=pygame.transform.scale_by(self.image,2)
        self.image.set_colorkey(light_blue)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.direction=pygame.Vector2()
        self.upscale_factor=2
       


    def input_from_user(self):
        keys =pygame.key.get_pressed()
        input_vector=pygame.Vector2(0,0)
        spead=2
        if keys[pygame.K_LEFT]:        
            input_vector.x-=spead
               
        if keys[pygame.K_RIGHT]:
            input_vector.x+=spead
        if keys[pygame.K_UP]:
            input_vector.y-=spead
        
        if keys[pygame.K_DOWN]:
            input_vector.y+=spead
            
        self.direction=input_vector
        
    def move(self,):
        
        self.input_from_user()
        self.rect.x += self.direction.x * self.upscale_factor
        self.rect.y += self.direction.y * self.upscale_factor

        
    #"D:/final_networking_project/assets/Game Boy Advance - Pokemon FireRed LeafGreen - Tileset 2.png"    
class Game():
    def __init__(self) -> None:
        
        pygame.init()
        self.clock=pygame.time.Clock()
# Set up the display
        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("pokemon battlegrounds")
        self.upscale_factor = 2 
        self.tmx_data=self.load_assets()
        self.player = Player(500, 500)
        self.sprite_group=Allsprites()
        self.sprite_group.add(self.player)
        
    def load_assets(self):        
        tmx_data = pytmx.load_pygame(r"beta_map.tmx")
        return tmx_data

# Load the tileset
#tileset = pygame.image.load("tileset4.png")
# Render the map
    def render_map(self,offset):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        scaled_tile = pygame.transform.scale(tile, (self.tmx_data.tilewidth * self.upscale_factor, self.tmx_data.tileheight * self.upscale_factor))
                        self.screen.blit(scaled_tile, (x * self.tmx_data.tilewidth * self.upscale_factor-offset[0], y * self.tmx_data.tileheight * self.upscale_factor-offset[1]))
    def mainloop(self):
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            offset=self.player.rect.center

        # Render the map
            self.screen.fill((0, 0, 0))
            self.render_map(offset)
            self.player.move() 
            
            # Draw player
            self.sprite_group.drraw(self.player) 
            
            # Update the display
            #print(game.clock.get_fps())
            pygame.display.flip()
            game.clock.tick(60)

        # Quit Pygame# Quit Pygame
        pygame.quit()

game=Game()
game.mainloop()
