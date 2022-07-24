from classes import *
from random import randint as rint

def titlescreen():
    from main import (
        black, white, red, screen, switch_gameState, moveApple,
        title_text, title_rect, # Imports title text and rect
        cred_text, cred_rect, # Imports credits text and rect
        pb_font ,pb_text, pb_rect # Imports Play Button font, text and rect
    ) 
    mousePos = pygame.mouse.get_pos()
    
    # Checks if cursor is hovering over button.
    if pb_rect.collidepoint(mousePos): 
        # If so, change the text color to red
        pb_text = pb_font.render("  Play  ", True, red, black)
        
        if pygame.mouse.get_pressed()[0] == 1: # Checks if player clicks the button
            
            # Starts the game
            print("The game has started.")
            switch_gameState("game")
            
            # Creates the snake.
            # To be honest, I have no idea how moving these 3 lines from main to this file make it work.
            # Before, I planned for the starting snake instances to be created in main.py but for some
            # Reason the program keeps making 2 of each instance and one part of the snake just froze and
            # wouldn't move. I spend an hour trying to figure out a fix. But apparently all I gotta do is this.
            # That's just.. great.
            
            Snake.objs.append(Snake(7,7))
            Snake.objs.append(Snake(6,7))
            Snake.objs.append(Snake(5,7))
            
            # Places the apple at a random tile on the screen
            moveApple()
            
    else: # If not, keep it white
        pb_text = pb_font.render("  Play  ", True, white, black)
    
    screen.blits( # Draws everything onto the screen
        blit_sequence=(
            (title_text, title_rect),
            (cred_text, cred_rect),
            (pb_text, pb_rect)
        )  
    )


def gamescreen():
    from main import green, red, apple

    # Updates all the game elements.
    apple.update(red)
    Snake.Update(green)