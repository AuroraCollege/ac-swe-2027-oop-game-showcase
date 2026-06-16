from flask import Response
import time
import base64
import io
import random
from math import ceil, floor
from PIL import Image, ImageDraw, ImageFont

BOARD_WIDTH = 10
BOARD_HEIGHT = 24
RENDER_MULTI = 30
SQUARE_BORDER_WIDTH = 1
BOARD_TETRO_STARTING = floor(BOARD_WIDTH / 2)

GRAY = (3, 7, 7)
LIGHT_GRAY = (48, 53, 53)
RED = (219, 15, 15)
LIGHT_AQUA = (98, 190, 229)
BLUE = (13, 67, 173)
YELLOW = (229, 192, 57)
PINK = (242, 67, 184)
PURPLE = (164, 31, 221)
GREEN = (59, 221, 31)

class Tetromino:
    """object representing a tetromino"""
    def __init__(self, pos:(int, int), list, colour:(int, int, int)):
        """
        - takes a center block position as a int,int tuple (row, col)
        - takes a list of offsets as a list of values like ((-1, 0), (-2,0))
        - takes a triple int tuple as a colour
        """
        self.pos = pos
        self.offsets = list
        self.colour = colour

    def check_collision(self, attempt_offset:(int,int), board_array:list):
        """given a board_array and a offset, check if a tetromino can move into that area"""
        # bounds checking
        for offset in self.offsets:
            if self.pos[0] + offset[0] + attempt_offset[0] > BOARD_WIDTH-1:
                return False
            if self.pos[1] + offset[1] + attempt_offset[1] > BOARD_HEIGHT-1:
                return False
            if self.pos[0] + offset[0] + attempt_offset[0] < 0:
                return False
            if self.pos[1] + offset[1] + attempt_offset[1] < 0:
                return False
        # check if theres a static block there
        for pos in self.board_pos(attempt_offset):
            if board_array[pos] != None:
                return False
        return True
    
    def place(self, board_array:list):
        """given a board_array, turns the tetro into a staic index on the board_array"""
        for pos in self.board_pos():
            board_array[pos] = self.colour

    def board_pos(self, pos_offset=(0,0)):
        """turns the list of offsets into indexs into the board array, optionally takes a offset"""
        row = self.pos[0] + pos_offset[0]
        col = self.pos[1] + pos_offset[1]
        pos_list = []
        pos_list.append(row + (col * BOARD_WIDTH))
        for offset in self.offsets:
            pos_list.append(row + offset[0] + ((col + offset[1]) * BOARD_WIDTH))
        return pos_list

    def rotate(self, board_array):
        """rotates the tetromino"""
        # creates a new tetro, checks collision, if good, returns that tetro, else returns None
        to_be_offsets = []
        for i in range(len(self.offsets)):
            to_be_offsets.append((-self.offsets[i][1], self.offsets[i][0]))
        rotated_self = Tetromino(self.pos, to_be_offsets, self.colour)
        if rotated_self.check_collision((0,0), board_array):
            return rotated_self


def random_tetro():
    """returns a random tetromino"""
    return random.choice((
        Tetromino((BOARD_TETRO_STARTING, 0), [(-2,0), (-1,0), (1,0)], LIGHT_AQUA),
        Tetromino((BOARD_TETRO_STARTING, 1), [(-1,-1), (-1,0), (1,0)], BLUE),
        Tetromino((BOARD_TETRO_STARTING, 1), [(-1,0), (1,0), (1,-1)], YELLOW),
        Tetromino((BOARD_TETRO_STARTING, 1), [(-1,-1), (-1,0), (0,-1)], PINK),
        Tetromino((BOARD_TETRO_STARTING, 1), [(-1,0), (0,-1), (1,0)], PURPLE),
        Tetromino((BOARD_TETRO_STARTING, 1), [(-1,0), (0,-1), (1,-1)], GREEN),
        Tetromino((BOARD_TETRO_STARTING, 1), [(1,-1), (0,-1), (-1,0)], RED),
    ))

class TetrisGame:
    def __init__(self):
        self.board_array = [None] * BOARD_HEIGHT * BOARD_WIDTH
        self.falling_object = random_tetro()
        self.score = 0

    def clear(self):
        """restarts the game"""
        self.board_array = [None] * BOARD_HEIGHT * BOARD_WIDTH
        self.falling_object = random_tetro()
        self.score = 0


    def frame(self):
        """renders the game and game loop"""
        # this is a generator that frame returns so that we can stream new frames without having to reload the whole page
        def render(self):
            # instead of returning a image every time, return a image the first time then return a javascript function that replaces the src of the function, should stop flashing
            yield f'<img id="gameimg" src="/static/speed.png">'
            counter = 0

            while True:
                # about every 100 ms or 10 fps
                counter += 1
                time.sleep(0.01)

                # check for full lines to clear
                filled_col = self.check_for_filled_line()
                if filled_col != None:
                    del self.board_array[filled_col*BOARD_WIDTH:(filled_col*BOARD_WIDTH)+BOARD_WIDTH]
                    for i in range(BOARD_WIDTH):
                        self.board_array.insert(0, None)
                    self.score += 1

                # checks if the falling block will collide with the bottom, if yes, turn into static
                if self.falling_object != None and counter % 20 == 0:
                    if self.falling_object.check_collision((0,1), self.board_array):
                        self.falling_object.pos = (self.falling_object.pos[0], self.falling_object.pos[1] + 1)
                    else:
                        self.falling_object.place(self.board_array)
                        self.falling_object = None

                if self.falling_object == None and counter % 30 == 0:
                    self.falling_object = random_tetro()

                # if the game is over, render the game over image
                if self.check_for_game_end():
                    im = Image.open("./static/sad_emoji.jpg")
                    draw = ImageDraw.Draw(im)
                    font = ImageFont.load_default(50)
                    draw.text((0,0), text=f"game over :(\nscore = {self.score}", font=font, fill=(0, 0, 0))
                    im_bytes = io.BytesIO()
                    im.save(im_bytes, format='PNG')
                    im_bytes = im_bytes.getvalue()
                else:
                    # saving to bytes workflow
                    im = self.create_image()
                    im_bytes = io.BytesIO()
                    im.save(im_bytes, format='PNG')
                    im_bytes = im_bytes.getvalue()

                # FUCK YEAHHHHH THIS TOOK 6 HOURS
                # sends a body that has a script that clears the previous body then replaces it with a image tag and base 64 encoded image
                final_image = f'<script type="text/javascript">document.getElementById("gameimg").src = "data:image/png;base64,{base64.b64encode(im_bytes).decode()}";</script>'
                yield final_image

        return Response(render(self), mimetype='text/html')

    def create_image(self):
        image = Image.new("RGBA", (BOARD_WIDTH * RENDER_MULTI + SQUARE_BORDER_WIDTH, BOARD_HEIGHT * RENDER_MULTI + SQUARE_BORDER_WIDTH), GRAY)
        drawing = ImageDraw.Draw(image)
        for i in range(0, len(self.board_array)):
            row = i % BOARD_WIDTH
            col = floor(i / BOARD_WIDTH)
            if self.board_array[i] == None:
                self.fill_square(drawing, (row, col))
            else:
                self.fill_square(drawing, (row, col), self.board_array[i])
            # render falling tetromino
            if self.falling_object != None:
                # draw center square
                self.fill_square(drawing, self.falling_object.pos, self.falling_object.colour)
                for i in self.falling_object.offsets:
                    row = self.falling_object.pos[0] + i[0]
                    col = self.falling_object.pos[1] + i[1]
                    self.fill_square(drawing, (row,col), self.falling_object.colour)
        return image

    def fill_square(self, draw:ImageDraw.ImageDraw, rowcol:(int,int), colour:(int, int, int)=GRAY, outline:(int, int, int)=LIGHT_GRAY):
        draw.rectangle(((rowcol[0] * RENDER_MULTI, rowcol[1] * RENDER_MULTI), ((rowcol[0] + 1) * RENDER_MULTI, (rowcol[1] + 1) * RENDER_MULTI)), width=SQUARE_BORDER_WIDTH, outline=outline, fill=colour)

    def check_for_filled_line(self):
        def inner_check(col):
            for row in range(BOARD_WIDTH):
                x = (col*BOARD_WIDTH)+row
                if self.board_array[x] == None:
                    return False
            return True
        for col in range(BOARD_HEIGHT):
            if inner_check(col) == True: return col

    def check_for_game_end(self):
        for block in self.board_array[0:BOARD_WIDTH-1]:
            if block != None:
                return True
        return False

    def hard_drop(self):
        while self.falling_object != None:
            if self.falling_object.check_collision((0,1), self.board_array):
                self.falling_object.pos = (self.falling_object.pos[0], self.falling_object.pos[1] + 1)
            else:
                self.falling_object.place(self.board_array)
                self.falling_object = None
