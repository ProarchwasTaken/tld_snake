import pygame
from random import randint as rint

tile_size = 40 # Size of all tile sized objects

class Grid:
    objs = [] # Store every instance of grid
    
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect(x+1, y+1, tile_size-2, tile_size-2)
        
        Grid.objs.append(self) # Adds self to objs list.
    
    @classmethod
    def Update(cls, color):
        from main import screen # Imports screen variable from main
        
        for obj in cls.objs:
            # Draws every tile instance
            pygame.draw.rect(screen, color, obj)

class Snake:
    objs = [] # Store every instance of snake. The snake head will always be at the beginning of the list
    head_direction = "right"
    movedelay = 0.2 * 1000 # How much seconds between each snake movement
    
    
    def __init__(self, tile_x, tile_y):
        self.rect = pygame.Rect(tile_x * 40, tile_y * 40, tile_size-1, tile_size-1)
        self.lastpos = self.rect.x, self.rect.y
        
        self.last_moved = pygame.time.get_ticks() # Saves the last time the snake last moved
        
    
    @classmethod
    def Update(cls, snk_color):
        # Only the snake head will be able to trigger this for loop and update - Which is the first item in the list
        for obj in cls.objs[:1]:
            obj.update_head(snk_color)
        # Pretty much every other instance will trigger this for loop. Except the first item in objs
        for obj in cls.objs[1:]:
            obj.update_tail(snk_color)
    
    # This updates the head of the snake
    def update_head(self, color):
        from main import screen, screenW, screenH
        
        # Moves the snake head
        self.headAnimation()
        
        # Checks if the head of the snake has colided with it's tail. Ends the game if it is.
        if Snake.snakeCollide(self.rect.center):
            print("The head has touched the body")
            Gameover()
        
        # Ends the game if snake head is outside the screen.
        if self.rect.left < 0 or self.rect.right > screenW or self.rect.top < 0 or self.rect.bottom > screenH:
            print("The head is outside the play area.")
            Gameover()
        
        # Draws the snake head
        pygame.draw.rect(screen, color, self)
            
    # This updates the rest of the snake body.
    def update_tail(self, color):
        from main import screen
        # Follows the path of snake head  
        self.taleAnimation()
        
        # Draws the tail instance
        pygame.draw.rect(screen, color, self)
    
            
    def headAnimation(self):
        from main import cur_ticks
        
        if cur_ticks - self.last_moved >= Snake.movedelay:
            self.getlastPosition() # Grabs the position of instance before moving.
            # Automatically moves the snake in a direction based on the string of head_direction
            if Snake.head_direction == "right":
                self.rect.x += tile_size
            if Snake.head_direction == "left":
                self.rect.x -= tile_size
            if Snake.head_direction == "down":
                self.rect.y += tile_size
            if Snake.head_direction == "up":
                self.rect.y -= tile_size
            
            self.last_moved = cur_ticks
    
    def taleAnimation(self):
        from main import cur_ticks
        self.index = Snake.objs.index(self) # Stores index number of instance after it got added to objs. This will be useful later ;)
        
        if cur_ticks - self.last_moved >= Snake.movedelay:
            self.getlastPosition() # Grabs the position of instance before moving.

            self_prevInstance = Snake.objs[self.index - 1] # Gets the instance older than self for use.
            
            self.rect.topleft = self_prevInstance.lastpos # Set self position to preInstance last position
            
            self.last_moved = cur_ticks
                
    def getlastPosition(self):
        self.lastpos = self.rect.x, self.rect.y
        self.lastpos_x = self.rect.x
        self.lastpos_y = self.rect.y
    
    @classmethod
    def growTail(cls):
        from main import cur_ticks
        # Grows tail
        for obj in cls.objs[-1:]:
            if not cur_ticks - obj.last_moved >= Snake.movedelay:
                cls.objs.append(Snake(obj.lastpos_x, obj.lastpos_y))
    
    @classmethod
    def snakeCollide(cls, head):
        for obj in cls.objs[1:]:
            # Checks if snake head is coliding with the it's body. Return True if it is.
            if obj.rect.collidepoint(head):
                return True
    
    @classmethod
    def appleCollide(cls):
        from main import apple
        for obj in cls.objs:
            # Checks if apple is touching the snake. return True if it is
            if apple.rect.colliderect(obj):
                return True
            
        
class Apple:
    
    grace_delay = 0.1 * 1000 # How much time before apple is eatable.
    
    def __init__(self, tile_x, tile_y):
        self.rect = pygame.Rect(tile_x * tile_size, tile_y * tile_size, tile_size-1, tile_size-1)
        
        self.last_collected = pygame.time.get_ticks()
        
    
    def update(self, color):
        from main import cur_ticks, moveApple
        
        
        if Snake.appleCollide(): # Checks if apple has collided with snake. Activates code inside if true
            if cur_ticks - self.last_collected >= Apple.grace_delay: # Grows snake if grace_delay is over
                
                moveApple() # Moves apple to a random tile on the screen
                
                Snake.growTail()
                
                print(f"Snake Length: {len(Snake.objs)}")
                
                # Starts the grace delay again.
                self.last_collected = cur_ticks
                
            else: # Else the apple will just move the apple to a random spot on the screen.
                # This is to make sure the apple doesn't move to a location inside the snake and instantly growing it's tail.
                
                moveApple() # Moves apple to a random tile on the screen
                
                # Starts the grace delay again.
                self.last_collected = cur_ticks
        
        # Draws the apple.
        self.draw(color)
        
    def draw(self, color):
        from main import screen
        pygame.draw.rect(screen, color, self)

# When called, resets everything and switch the gamestate back to the Title Screen
# Thanks to how I wrote the code, writing something like this is very easy.       
def Gameover():
    from main import switch_gameState
    print("Game Over")
    
    Snake.objs.clear()
    
    switch_gameState("title")