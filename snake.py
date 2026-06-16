'''Defines cell, player, and game classes in Snake game'''

import random

# // EPIC BOARD CONTROLS!!!!! \\#

width = 11
height = 11

# \\_____________________________//#

class Cell:
    '''Represents a single cell on the game board'''

    def __init__(self, x, y):
        '''Stores cell coordinates'''
        self.x = x
        self.y = y

    @property 
    def position(self):
        #Returns position as a list for easier comparison
        return [self.x, self.y]

class Apple(Cell):
    '''Represents apple cell type on the game board'''

    def __init__(self, x, y):
        '''Stores apple cell coordinates'''
        super().__init__(x, y)

class Wall(Cell):
    '''Represents wall cell type on the game board'''

    def __init__(self, x, y):
        '''Stores wall cell coordinates'''
        super().__init__(x,y) 

class Tail(Cell):
    '''Represents tail cell type on the game board''' 

    def __init__(self, x, y):
        '''Stores tail cell coordinates'''
        super().__init__(x,y) 

class Player:
    '''Represents snake object controlled by user'''

    def __init__(self):
        '''Sets initial movement direction to the right and places player in center of board'''
        self.body = []
        #Ensures player starts with one body in the middle of the board
        self.body.append(Tail(width // 2, height // 2))

    def grow(self): 
        '''Adds tail object to old position''' 
        #Ensures new tails always spawn behind the head
        new_x, new_y = self.old_positions[-1]
        self.body.append(Tail(new_x, new_y))
        #Length needs to be know for debugging
        print(len(self.body))

    def move_to(self, direction): 
        '''Moves head cell in selected direction'''  

        self.old_positions = []

        #Snake must store old positions in order to grow properly
        for tail in self.body: 
            self.old_positions.append((tail.x, tail.y))

        #Head must be specially referenced in order to control snake
        self.head = self.body[0]

        if direction == "Right": 
            self.head.x += 1
        if direction == "Left": 
            self.head.x -= 1
        if direction == "Up": 
            self.head.y -= 1
        if direction == "Down": 
            self.head.y += 1 
        
        #Every tail moves to the position of the tail before it
        for i in range(1, len(self.body)):
           self.body[i].x = self.old_positions[i - 1][0]
           self.body[i].y = self.old_positions[i - 1][1]

class SnakeGame:
    '''Represents game instance'''

    def __init__(self):
        '''Stores initial board dimensions and starts new game'''
        self.new_game()

    def check_for_apple(self): 
        '''Checks if player has touched an apple'''
        #Compare head position to all apples on board
        for apple in self.apples: 
            if self.player.head.position == apple.position: 
                print("Collected apple")
                return True

    def check_for_wall(self): 
        '''Checks if player has touched a wall'''
        #Compare head position to all wall positions on board
        for wall in self.walls: 
            if self.player.head.position == wall.position: 
                print("Hit wall")
                return True
            
    def check_for_snake(self): 
        '''Checks if player has touched itself'''
        #Compare head position to all tail positions on board 
        for i in range(1, len(self.player.body)): 
            if self.player.head.position == self.player.body[i].position:
                print("Hit snake")
                return True
                
    def check_win(self): 
        '''Checks if player has maximum length'''
        #Wins when every possible cell is occupied by the snake
        length = len(self.player.body)
        if length == (width - 2) * (height - 2): 
            return True

    def move(self, direction):
        '''Moves player in selected direction 
           Checks if player has hit a wall or apple'''
        #Don't move when no direction is inputted
        if not direction: 
            return None
        
        self.player.move_to(direction) 

        #Grows snake and creates new apple when eaten
        if self.check_for_apple(): 
            self.player.grow()
            self.spawn_apple()
        
        #Only check self collision when snake has grown past 1 square
        if len(self.player.body) >= 2:
            if self.check_for_snake(): 
               self.game_On = False

        #Trigger game over if player hits wall
        if self.check_for_wall(): 
            self.game_On = False   

        #Checks if player has won in order to communicate to webpage
        if self.check_win(): 
            self.game_Won = True 
            return "You Won!"

        return f"Player moving to the {direction}"

    def construct_walls(self): 
        '''Creates table with initial wall coordinates'''
        self.walls = []

        #Create wall cells on outside edge of board
        for i in range(1, width + 1): 
            for j in range(1, height + 1): 
                if i == 1: 
                    self.walls.append(Wall(i, j)) 
                if i == width: 
                    self.walls.append(Wall(i, j)) 
                if j == 1: 
                    self.walls.append(Wall(i, j))
                if j == height: 
                    self.walls.append(Wall(i, j)) 
    
    def spawn_apple(self):
        '''Spawns new apple with random coordinates'''
        
        self.apples = []
        
        while True:
            #Generate random position inside playable area
            new_x = random.randint(2, width - 1)
            new_y = random.randint(2, height - 1)

            position = [new_x, new_y]

            occupied = False 

            #Prevent apple from spawning on snake
            for tail in self.player.body:
                if position == tail.position:
                   occupied = True
                   break

            #Create apple when free space is found
            if not occupied:
                self.apples.append(Apple(new_x, new_y))
                print(f"Apple spawned at ({new_x}, {new_y})")
                return

    def new_game(self): 
        '''Creates new board and player instance 
           instantiates game_On as true'''
        self.width = width 
        self.height = height

        #Reset game state
        self.game_On = True 
        self.game_Won = False

        #Create new snake
        self.player = Player()
        
        #Create new board with walls and apple
        self.construct_walls()
        self.spawn_apple()

        #Initialise head by moving the snake
        self.move("Right")

        return "Welcome to Snake! Eat apples to grow and use WASD to move."

