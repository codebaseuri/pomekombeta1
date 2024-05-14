from typing import Iterable
import pygame
from pygame.sprite import AbstractGroup
import pytmx
import random
global user_text,textlist
global do_aninamation,player_pokemon ,enemy_pokemon
global player_sprites,selected_box_index,ft_font,input_box_text,battle_state,player_animation_index,player_animation_speed,player_animation_timer,dt
screen_width,screen_height=1280,720
cyan = (0, 255, 255)
black = (0, 0, 0)
white = (255, 255, 255)

# Player class
class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,layerid=0):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(topleft=pos)
        self.layerid=layerid
class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen=pygame.display.get_surface()
        self.offset=pygame.Vector2(0,0)
    
    def draw(self,player):
        
        self.offset.x=-(player.rect.center[0]-screen_width//2)
        self.offset.y=-(player.rect.center[1]-screen_height//2)

        for sprite in self:#sorted(self,key=lambda sprite: sprite.rect.centery):
            if type(sprite)!=Player:
                if not sprite.layerid==0:
                    self.screen.blit(sprite.image,sprite.rect.topleft+self.offset)
            else:
                sprite_x, sprite_y = player.sprite_layout[sprite.player_data.current_direction][sprite.player_data.current_picure]
                sprite_rect = pygame.Rect(sprite_x, sprite_y, 64, 64)
                sprite.image = pygame.transform.scale(player.sprite_sheet.subsurface(sprite_rect), player.PLAYER_SIZE)  
                self.screen.blit(sprite.image,sprite.rect.topleft+self.offset)
            
               # print("printed other players sprite")
               # print(f"cords are {sprite.player_data.x_cord},{sprite.player_data.y_cord}")
        #if p!=None:       
            #self.screen.blit(p.image,sprite.rect.topleft+self.offset)
           # print(f"cords are {sprite.player_data.x_cord},{sprite.player_data.y_cord}")
            
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,player_data=None):
        
        self.player_data=player_data
        super().__init__()
        self.sprite_sheet = pygame.image.load("player_sprites.png")
        self.sprite_layout = {
        "down": [(0, 0), (64, 0), (128, 0), (192, 0)],
        "left": [(0, 64), (64, 64), (128, 64), (192, 64)],
        "right": [(0, 128), (64, 128), (128, 128), (192, 128)],
        "up": [(0, 192), (64, 192), (128, 192), (192, 192)]
}
        self.player_direction = "down"
        self.frame = 0
        self.moving = False
        
        light_blue=(17,219,255)

        self.image = pygame.Surface((64,64))
        #self.image = pygame.image.load(r"assets\image_24.png").convert_alpha()
        #self.image=pygame.transform.scale_by(self.image,2)

        self.image.set_colorkey(light_blue)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.direction=pygame.Vector2()
        self.upscale_factor=2
        self.moved=False
        self.rect.y=y
        self.rect.x=x
        self.player_data.x_cord=x
        self.player_data.y_cord=y
        print(f"player cords are: {self.player_data.x_cord},{self.player_data.y_cord}")
        self.PLAYER_SIZE = (64, 64)

    def update_cords(self,x,y):
        self.player_data.x_cord=x
        self.player_data.y_cord=y
        


    def input_from_user(self):
        keys =pygame.key.get_pressed()
        input_vector=pygame.Vector2(0,0)
        spead=3
        if keys[pygame.K_LEFT]:        
            input_vector.x-=spead
            self.direction=input_vector
            self.player_direction = "left"
            self.moving = True
            
               
        elif keys[pygame.K_RIGHT]:
            input_vector.x+=spead
            self.direction=input_vector
            self.player_direction = "right"
            self.moving = True
           
        elif keys[pygame.K_UP]:
            input_vector.y-=spead
            self.direction=input_vector
            self.player_direction = "up"
            self.moving = True
            
        
        elif keys[pygame.K_DOWN]:
            input_vector.y+=spead
            self.direction=input_vector
            self.player_direction = "down"
            self.moving = True
            
        else:
            self.moving = False
        
        if self.moving:
            self.frame = (self.frame + 1) % len(self.sprite_layout[self.player_direction])
        self.player_data.current_picure=self.frame%4 
        self.player_data.current_direction=self.player_direction
        sprite_x, sprite_y = self.sprite_layout[self.player_direction][self.frame]
        sprite_rect = pygame.Rect(sprite_x, sprite_y, self.PLAYER_SIZE[0], self.PLAYER_SIZE[1])
        self.image = pygame.transform.scale(self.sprite_sheet.subsurface(sprite_rect), self.PLAYER_SIZE)  
        self.direction=input_vector
        return self.moving
        
    def move(self,collision_rects=[]):
        self.moved=self.input_from_user()
        player_cords=(self.rect.x+self.direction.x,self.rect.y+self.direction.y)
        if not self.check_player_collision(player_cords,collision_rects):

            if self.moved:
        #print("hellooooo")

                self.rect.x += self.direction.x * self.upscale_factor
                self.rect.y += self.direction.y * self.upscale_factor
                self.player_data.x_cord+=self.direction.x * self.upscale_factor
                self.player_data.y_cord+=self.direction.y * self.upscale_factor
                #print( f"cords are{self.player_data.x_cord},{self.player_data.y_cord}")   
        

    
    #"D:/final_networking_project/assets/Game Boy Advance - Pokemon FireRed LeafGreen - Tileset 2.png" 
    def check_player_collision(self, player_cords,collision_rects):
        
        player_rect=pygame.Rect(player_cords[0]+self.direction.x, player_cords[1]+self.direction.y, 64, 64)
        for rect in collision_rects:
            #print("niggag")
            #print(self.rect)
            #print(player_rect.colliderect(rect))
            if player_rect.colliderect(rect):
                return True
        
        return False   
    


class Game():
    def __init__(self,player_data,window) -> None:
        
        self.game=pygame.init()
        self.clock=pygame.time.Clock()
        background_image = pygame.image.load("background.jpg")
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        self.screen_width, self.screen_height = 1280, 720
        self.screen = window#pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("pokemon battlegrounds")
        self.upscale_factor = 2 
        #self.screen=None
# Load the player sprite sheet

        
# Set up the display
        

        self.tmx_data=self.load_assets()
        cords=self.set_player_spawn_cords()
        print(f"start cords are {cords}")
        self.player = Player(cords[0],cords[1],player_data[0])
        print(player_data[1])

        # Initialize input box selection    
        selected_box_index = 0
        battle_state = False

        # Initialize input box text
        input_box_text = ["attack", "heal", "raise attack", "quit"]

        # Initialize font


        # Initialize player animation
        global current_player_pokemon, current_enemy_pokemon
        current_player_pokemon = 0
        current_enemy_pokemon = 0
            
            # initalize player in spawn location 
            
        self.sprite_group=Allsprites()
        self.setup(self.tmx_data)
        self.collision_objects=self.load_collision_objects(self.tmx_data)
        print(self.collision_objects)
        self.sprite_group.add(self.player)
        self.other_players={}

    def quit_game(self):
        pygame.quit()
    def set_player_spawn_cords(self):
        for obj in self.tmx_data.get_layer_by_name("objlayer"):
            if obj.name=="spawn_point":
                #self.player.player_data.x_cord=int(obj.x)
                #self.player.player_data.y_cord=int(obj.y)
                #self.player.rect.y=int(obj.y*self.upscale_factor)
                #self.player.rect.x=int(obj.x*self.upscale_factor)
                return obj.x*self.upscale_factor,obj.y*self.upscale_factor
                
                #update the player cords
                break
        
    def setup(self,tmx_data):
       
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    layerid=layer.layername

                    if tile:
                        scaled_tile = pygame.transform.scale(tile, (self.tmx_data.tilewidth * self.upscale_factor, self.tmx_data.tileheight * self.upscale_factor))
                        Sprite((x*16*self.upscale_factor,y*16*self.upscale_factor),scaled_tile,self.sprite_group,layerid)

    
    def load_collision_objects(self,tmx_data):
        collision_rects = []
        
        # Get the object layers
        object_layers = [layer for layer in tmx_data.visible_layers if isinstance(layer, pytmx.TiledObjectGroup)]
        
        # Extract objects from the layers
        for layer in object_layers:
            for obj in layer:
                rect = pygame.Rect(obj.x*self.upscale_factor, obj.y*self.upscale_factor, obj.width*self.upscale_factor, obj.height*self.upscale_factor)
                collision_rects.append(rect)
                
        return collision_rects      
    
    def load_assets(self):        
        tmx_data = pytmx.load_pygame(r"map6.tmx")
        return tmx_data
    
    def update_other_players(self,otherplayers_dict,username,player_data):
        if username!=self.player.player_data.name:
            
            print(self.other_players)
            if username not in self.other_players:
                newp=Player(player_data.x_cord,player_data.y_cord,player_data=player_data)
                self.other_players[username]=newp
                

                self.sprite_group.add(newp) 
                
            else:
                self.other_players[username].rect.x=player_data.x_cord
                self.other_players[username].rect.y=player_data.y_cord
                self.other_players[username].update_cords(player_data.x_cord,player_data.y_cord)
                self.other_players[username].player_data=player_data


    def mainloop(self):
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            offset=self.player.rect.center
            print(offset)

        # Render the map
            self.screen.fill((0, 0, 0))
            #self.render_map(offset)
            self.player.move(self.collision_objects) 

            
            # Draw player
            self.sprite_group.draw(self.screen)
            #self.sprite_group.drraw(self.player) 
            
            # Update the display
            #print(game.clock.get_fps())
            pygame.display.flip()
            game.clock.tick(60)

        # Quit Pygame# Quit Pygame
        pygame.quit()
if __name__ == "__main__":
    game=Game()
    game.mainloop()
