import pygame,sys
# Imports Classes and functions from other scripts
from gamestates import *
from classes import Grid, Snake, Apple

# General stuff
pygame.init()
clock = pygame.time.Clock()

screenW, screenH = 600, 600 # W = Width, H = Height
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("Tyler's Snake")

# Colors - (r, g, b)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 80)
cred_font = pygame.font.Font(None, 20)
pb_font = pygame.font.Font(None, 40)

# ======Static Text
# Title Text
title_text = title_font.render("       Snake       ", True, white, black)
title_rect = title_text.get_rect()
title_rect.center = 300, 100
# Credits Text
cred_text = cred_font.render("Snake clone made by: Tyler Dillard, 2022", True, white, black)
cred_rect = cred_text.get_rect()
cred_rect.center = 300, 590
# Play Button
pb_text = pb_font.render("  Play  ", True, white, black)
pb_rect = pb_text.get_rect() 
pb_rect.center = 300, 300

# Variables
game_state = "title" # Stores the state the game is in.

grid_tiles = [] # Stores all grid tiles

grid_rows = 15
grid_cols = 15

# Prepares grid for grid class
for row_index in range(grid_cols):
    for col_index in range(grid_rows):
        x = col_index * tile_size
        y = row_index * tile_size
            
        grid_tiles.append(Grid(x, y))

apple = Apple(0,0) # Apple Instance

# Functions
def switch_gameState(new_state): # when called switches gamestate to value of new_state
    global game_state
    game_state = new_state

def moveApple(): # When called, moves the apple to a random tile on the screen
    apple.rect.topleft = rint(0,14) * tile_size, rint(0,14) * tile_size

# Game Loop
while True:
    # Checks for events like player input.
    for event in pygame.event.get():
        # Allows player to close the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Checks for player input
        if event.type == pygame.KEYDOWN:
            # Turns the snake towards a direction as long it's not the opposite of the direction the snake is currently going.
            if event.key == pygame.K_RIGHT and not Snake.head_direction == "left": # Right
                Snake.head_direction = "right"
            if event.key == pygame.K_LEFT and not Snake.head_direction == "right": # Left
                Snake.head_direction = "left"
            if event.key == pygame.K_DOWN and not Snake.head_direction == "up": # Down
                Snake.head_direction = "down"
            if event.key == pygame.K_UP and not Snake.head_direction == "down": # Up
                Snake.head_direction = "up"
    
    # Refreshes the screen and draws the grid.
    screen.fill(white)
    Grid.Update(black)
    
    # This changes what is drawn on the screen based on game_state
    if game_state == "title":
        titlescreen()
    if game_state == "game":
        gamescreen()
    
    # Updates the screen
    clock.tick(60)
    cur_ticks = pygame.time.get_ticks() # Get the current tick count.
    pygame.display.flip()