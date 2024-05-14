

import sys
from pytmx import load_pygame
import pygame
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(r"E:\final_networking_project\assets\image_24.png").convert_alpha()
        

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surface,groups):
        super().__init__(groups)
        self.image=surface
        self.rect=self.image.get_rect(topleft=pos)

class Game:

    def __init__(self):
        pygame.init()
        self.screen_width = 620
        self.screen_hight=620
        self.display_surface = pygame.display.set_mode((self.screen_width, self.screen_hight))

        pygame.display.set_caption("Pokemon Battlegrounds")
        path_of_map=r"E:\final_networking_project\beta_map.tmx"
        self.tmx_data=load_pygame(path_of_map)

        self.map_width=self.tmx_data.width
        self.map_height=self.tmx_data.height
        #height and width of map 

        self.layer=self.tmx_data.get_layer_by_name("layer1_beta")
        #print(dir(layer))
        self.sprite_groups=pygame.sprite.Group()

        self.upscale_factor = 2

        upscaled_map_height=self.map_height*self.upscale_factor
        upscaled_map_width=self.map_width*self.upscale_factor
        

    

    def run(self):
        while True:
            #event loop logic 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #game logic
            #game display
            self.sprite_groups.draw(self.display_surface)
            pygame.display.update()
    def draw_map(self):
        for layer in self.tmx_data.visible_layers:
            if "beta" in layer.name:
                print("slay")
                for x,y, image in layer.tiles():
                    position=(x*16,y*16)
                    Tile(position,image,groups=game.sprite_groups)



game=Game()
game.draw_map()
game.run()