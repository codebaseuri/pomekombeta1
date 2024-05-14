import pygame

# Initialize Pygame
pygame.init()

# Set up the window
window_width, window_height = 1280, 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pokemon Game")

# Load the background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (window_width, window_height))

# Load the player sprite sheet
player_sprite_sheet = pygame.image.load("playersheet.png").convert_alpha()
player_sprite_width, player_sprite_height = 164, 192
player_sprites = []
for i in range(5):
    x = i * player_sprite_width
    player_sprite = pygame.Surface((player_sprite_width, player_sprite_height), pygame.SRCALPHA)
    player_sprite.blit(player_sprite_sheet, (0, 0), (x, 0, player_sprite_width, player_sprite_height))
    player_sprites.append(player_sprite)

# Load the Pokemon image
pokemon_image = pygame.image.load("charizardex1.png").convert_alpha()
pokemon_image = pygame.transform.scale(pokemon_image, (256, 256))

# Define colors
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

# Define input box dimensions and positions
input_box_width, input_box_height = 200, 60
input_box_margin = 10
input_box_y = window_height - input_box_height - 100
input_box_x = (window_width - (4 * input_box_width + 3 * input_box_margin)) // 2 - 40

# Initialize the selected input box index
selected_box_index = 0

# Initialize input box text
input_box_text = ["attack", "heal", "swap", "quit"]

# Initialize font
font = pygame.font.Font(None, 36)

# Initialize player animation
player_animation_index = 0
player_animation_speed = 0.2
player_animation_timer = 0
player_animation_triggered = False

global user_text, ft_font, textlist
ft_font = pygame.font.Font(None, 32)
active = False
textlist = [""]

def print_msg_to_screen(msg, cords, fromm=""):
    global user_text, ft_font
    textsurface = ft_font.render(fromm + msg, True, (255, 255, 255))
    window.blit(textsurface, cords)

def draw_messages_to_screen():
    global textlist
    global count
    maxim = max(0, len(textlist) - 10)
    print_msg_to_screen("player moves :", (1050, 300))
    count = 1
    var = 300
    for i in range(maxim, 10 + maxim):
        # print(i)
        try:
            print_msg_to_screen(textlist[i], (1050, var + count * 32))
        except:
            pass
        count += 1

# Pokemon class
class Pokemon(pygame.sprite.Sprite):
    def __init__(self, image, level, hp, attack, defense, luck):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        print(self.rect)
        self.rect.x = 256
        self.rect.y = 300
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.luck = luck
        self.name = "Charizard"

# Create a Pokemon instance
poke_object = Pokemon(pokemon_image, 10, 100, 50, 30, 20)

# Game loop
running = True
while running:
    dt = pygame.time.Clock().tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                selected_box_index = (selected_box_index + 1) % 4
            elif event.key == pygame.K_LEFT:
                selected_box_index = (selected_box_index - 1) % 4
            elif event.key == pygame.K_RETURN:
                print(input_box_text[selected_box_index])
                textlist.append(input_box_text[selected_box_index])
                player_animation_triggered = True  # Trigger the player animation

            elif event.key == pygame.K_BACKSPACE:
                input_box_text[selected_box_index] = input_box_text[selected_box_index][:-1]
            else:
                input_box_text[selected_box_index] += event.unicode

    # Update player animation
    if player_animation_triggered:
        player_animation_timer += dt
        if player_animation_timer >= player_animation_speed:
            player_animation_index = (player_animation_index + 1) % len(player_sprites)
            player_animation_timer = 0
        if player_animation_index == 0:  # Reset the animation trigger when the animation cycle completes
            player_animation_triggered = False

    # Draw the background image
    window.blit(background_image, (0, 0))

    # Draw the player sprite
    player_rect = player_sprites[player_animation_index].get_rect()
    player_rect.y = 300
    window.blit(player_sprites[player_animation_index], player_rect)

    # Draw the Pokemon sprite
    window.blit(poke_object.image, poke_object.rect)

    # Draw Pokemon properties
    property_text = f"Level: {poke_object.level}, HP: {poke_object.hp}, Attack: {poke_object.attack}, Defense: {poke_object.defense}, Luck: {poke_object.luck}"
    property_surface = font.render(property_text, True, white)
    window.blit(property_surface, (20, 60))

    # Draw the input boxes
    for i in range(4):
        input_box_rect = pygame.Rect(input_box_x + (input_box_width + input_box_margin) * i, input_box_y, input_box_width, input_box_height)
        pygame.draw.rect(window, blue, input_box_rect)

        # Draw a black outline on the selected input box
        if i == selected_box_index:
            pygame.draw.rect(window, black, input_box_rect, 2)

        # Render and draw the input box text
        text_surface = font.render(input_box_text[i], True, white)
        text_rect = text_surface.get_rect(center=input_box_rect.center)
        window.blit(text_surface, text_rect)

    draw_messages_to_screen()

    pygame.display.update()

# Quit Pygame
pygame.quit()