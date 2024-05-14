import pygame
global user_text,textlist
global do_aninamation
global player_sprites
import random
window_width, window_height = 1280, 720
global player_Sprites,selected_box_index,ft_font,input_box_text,battle_state,player_animation_index,player_animation_speed,player_animation_timer,dt,selected_box_index
cyan = (0, 255, 255)
black = (0, 0, 0)
white = (255, 255, 255)

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, image, level, hp, attack, defense, Type, name):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 256
        self.rect.y = 300
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.type = Type
        self.name = name

# Enemy Pokemon class (inherits from Pokemon)
class EnemyPokemon(Pokemon):
    def __init__(self, image, level, hp, attack, defense, Type, name):
        super().__init__(image, level, hp, attack, defense, Type, name)
        self.rect.topright = (window_width - 20, 20)  # Position the image in the top-right corner
        self.rect.y=200
        self.rect.x =850



def attack(attacker, defender):
    damage = attacker.attack - defender.defense
    if damage < 0:
        damage = 0
    defender.hp -= damage
    print(f"{attacker.name} attacked {defender.name} for {damage} damage!")
    textlist.append(f"{attacker.name} attacked {defender.name} for {damage} damage!")


def swap_pokemon():
    global poke_object
    # Code to swap player's Pokemon goes here
    pass

def use_healing_item(pokemon):
    
    pokemon.hp += 10
    if pokemon.hp > 100:
        pokemon.hp = 100
    print(f"{pokemon.name} recovered 10 HP!")
    textlist.append(f"{pokemon.name} recovered 10 HP!")

def draw_pokemon_properties(window,pokemon,enemy_pokemon):
    
    # Draw Pokemon properties
    propdict={"name": pokemon.name, "level": pokemon.level, "attack": pokemon.attack, "defense": pokemon.defense, "hp": pokemon.hp, "type": pokemon.type}
    eneny_dict={"name": enemy_pokemon.name, "level": enemy_pokemon.level, "attack": enemy_pokemon.attack, "defense": enemy_pokemon.defense, "hp": enemy_pokemon.hp, "type": enemy_pokemon.type}
    k=32
    for i in propdict.keys():  
        property_text = f"{i}: {propdict[i]}"
        property_surface = ft_font.render(property_text, True, white)
        enemy_property_text = f"{i}: {eneny_dict[i]}"
        enemy_property_surface = ft_font.render(enemy_property_text, True, white)
        window.blit(property_surface, (10, k))
        window.blit(enemy_property_surface, (window_width - 200, k))
        k+=32

def construct_player_sprites():
    player_sprite_sheet = pygame.image.load("playersheet.png").convert_alpha()
    player_sprite_width, player_sprite_height = 164, 192
    player_sprites = []
    for i in range(5):
        x = i * player_sprite_width
        player_sprite = pygame.Surface((player_sprite_width, player_sprite_height), pygame.SRCALPHA)
        player_sprite.blit(player_sprite_sheet, (0, 0), (x, 0, player_sprite_width, player_sprite_height))
        player_sprites.append(player_sprite)
    return player_sprites


def check_if_fainted(pokemon,enemy_pokemon,textlist):
    global current_player_pokemon,current_enemy_pokemon
    if pokemon.hp <= 0:
        print("Your Pokemon has fainted!")
        textlist.append("Your Pokemon has fainted!")
        current_player_pokemon+=1

    # Code to handle player's Pokemon fainting goes here
        return True
    
    elif enemy_pokemon.hp <= 0:
        print("Enemy Pokemon has fainted!")
        textlist.append("Enemy Pokemon has fainted!")
        current_enemy_pokemon+=1
        return True
    # Code to handle enemy Pokemon fainting goes here
    return False

def draw_boxes(window,font=""):
    font = pygame.font.Font(None, 32)
    # Define input box dimensions and positions
    input_box_width, input_box_height = 200, 60
    input_box_margin = 10
    input_box_y = window_height - input_box_height - 100
    input_box_x = (window_width - (4 * input_box_width + 3 * input_box_margin)) // 2 - 40
    # Draw the input boxes

    for i in range(4):
        input_box_rect = pygame.Rect(input_box_x + (input_box_width + input_box_margin) * i, input_box_y, input_box_width, input_box_height)
        pygame.draw.rect(window, cyan, input_box_rect)

        # Draw a black outline on the selected input box
        if i == selected_box_index:
            pygame.draw.rect(window, black, input_box_rect, 2)

        # Render and draw the input box text
        text_surface = font.render(input_box_text[i], True, white)
        text_rect = text_surface.get_rect(center=input_box_rect.center)
        window.blit(text_surface, text_rect)





def print_msg_to_screen(window,msg, cords, fromm="",tft_font=""):
    global user_text
    tft_fontf= pygame.font.Font(None, 32)
    textsurface = tft_fontf.render(fromm + msg, True, (255, 255, 255))
    window.blit(textsurface, cords)

def draw_messages_to_screen(window):
    global textlist
    global count
    maxim = max(0, len(textlist) - 5)
    print_msg_to_screen(window,"player moves :", (500, 20))
    count = 1
    var = 32
    for i in range(maxim, 5 + maxim):
        # print(i)
        try:
            print_msg_to_screen(window,textlist[i], (500, var  + count * 15),tft_font=pygame.font.Font(None, 20) )
        except:
            pass
        count += 1

def player_animation(window):
    global player_Sprites
    global player_animation_timer, player_animation_index,do_aninamation
    #Update player animation
    if do_aninamation:
        player_animation_timer += dt
        if player_animation_timer >= player_animation_speed:
            if player_animation_index == 4:
                do_aninamation=False
            player_animation_index = (player_animation_index + 1) % len(player_sprites)
            player_animation_timer = 0
            
    player_rect = player_sprites[player_animation_index].get_rect()
    player_rect.y = 300
    window.blit(player_sprites[player_animation_index], player_rect)
    
def handle_boxes_input():
    selected_action = input_box_text[selected_box_index]
    if selected_action == "attack":
        attack(player_pokemon[current_player_pokemon], enemy_pokemon[current_enemy_pokemon])
    elif selected_action == "heal":
        use_healing_item(player_pokemon[current_player_pokemon])
    elif selected_action == "raise attack":
        raise_attack(player_pokemon[current_player_pokemon])
    elif selected_action == "quit":
        running = False
    

def construct_player_pokemon():
    global player_pokemon
    player_pokemon = []
    for i in range(6):
        pokemon_image = pygame.image.load(f"charizardex1.png").convert_alpha()
        pokemon_image = pygame.transform.scale(pokemon_image, (256, 256))
        player_pokemon.append(Pokemon(pokemon_image, 10, 100, 50, 30, "fire", f"pokemon{i+1}"))
    return player_pokemon

def construct_enemy_pokemon():
    global enemy_pokemon
    enemy_pokemon = []
    for i in range(6):
        enemy_pokemon_image = pygame.image.load(f"blast1.png").convert_alpha()
        enemy_pokemon_image = pygame.transform.scale(enemy_pokemon_image, (192, 192))
        enemy_pokemon.append(EnemyPokemon(enemy_pokemon_image, 12, 120, 60, 40, "water", f"enemy{i+1}"))
    return enemy_pokemon

def draw_pokemon(window,pokemon):
    
    window.blit(pokemon.image, pokemon.rect)

def check_if_all_fainted(pokemon_list, textlist):
    for pokemon in pokemon_list:
        if pokemon.hp > 0:
            return False
    if pokemon_list == player_pokemon:
        print("All your Pokemon have fainted!")
        textlist.append("All your Pokemon have fainted!")
    else:
        print("You have defeated all enemy Pokemon!")
        textlist.append("You have defeated all enemy Pokemon!")
    return True



def raise_attack(pokemon):
    chance = random.randint(1, 100)
    if chance <= 50:
        pokemon.attack +=20
        print(f"{pokemon.name}'s attack has been raised!")
        textlist.append(f"{pokemon.name}'s attack has been raised!")
    else:
        print(f"Failed to raise {pokemon.name}'s attack.")
        textlist.append(f"Failed to raise {pokemon.name}'s attack.")




def mainfunc(window):
    pygame.init()
    global ft_font, active, textlist
    ft_font = pygame.font.Font(None, 32)
    do_aninamation=True

    # Set up the window
    window_width, window_height = 1280, 720
    #window = pygame.display.set_mode((window_width, window_height))
    #pygame.display.set_caption("Pokemon Game")

    # Load the background image
    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

    # Load the player sprite sheet

    player_sprites= construct_player_sprites()
    print("nigggagag")

    # Define colors


    # Initialize the selected input box index
    global selected_box_index, battle_state
    selected_box_index = 0
    battle_state = False

    # Initialize input box text
    global input_box_text
    input_box_text = ["attack", "heal", "raise attack", "quit"]

    # Initialize font


    # Initialize player animation
    player_animation_index = 0
    player_animation_speed = 0.2
    player_animation_timer = 0

    active = False
    textlist = [""]


    # Game loop
    running = True
    do_aninamation=True

    player_pokemon = construct_player_pokemon()
    enemy_pokemon = construct_enemy_pokemon()
    global current_player_pokemon, current_enemy_pokemon
    current_player_pokemon = 0
    current_enemy_pokemon = 0
    
    while running:
        dt = pygame.time.Clock().tick(60) / 1000

        # Draw the background image
        window.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selected_box_index = (selected_box_index + 1) % 4
                elif event.key == pygame.K_LEFT:
                    selected_box_index = (selected_box_index - 1) % 4
                elif event.key == pygame.K_RETURN:
                    if not battle_state:
                        battle_state = True
                    else:
                        handle_boxes_input()
                elif event.key == pygame.K_BACKSPACE:
                    input_box_text[selected_box_index] = input_box_text[selected_box_index][:-1]
                else:
                    input_box_text[selected_box_index] += event.unicode

        # Draw the player Pokemon
        draw_pokemon(window,player_pokemon[current_player_pokemon])

        # Draw the enemy Pokemon
        draw_pokemon(window ,enemy_pokemon[current_enemy_pokemon])

        # Draw Pokemon properties
        draw_pokemon_properties(window,player_pokemon[current_player_pokemon], enemy_pokemon[current_enemy_pokemon])

        # Draw the input boxes
        draw_boxes(window)

        # Draw battle log
        draw_messages_to_screen(window)

        # Check if either Pokemon has fainted
        if check_if_fainted(player_pokemon[current_player_pokemon], enemy_pokemon[current_enemy_pokemon], textlist):
            if check_if_all_fainted(player_pokemon, textlist):
                running = False
            elif check_if_all_fainted(enemy_pokemon, textlist):
                running = False
            else:
                current_player_pokemon %=  len(player_pokemon)
                current_enemy_pokemon %=  len(enemy_pokemon)

        pygame.display.update()

# Quit Pygame
