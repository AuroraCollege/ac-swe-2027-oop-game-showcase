from flask import Flask, render_template, request, redirect
from wumpus import HuntTheWumpus
from ScissorsPaperRock import ScissorsPaperRock
from snake import SnakeGame
from NumberGuessingGame import NumberGuessingGame
from tetris import TetrisGame

from minesweeper import MinesweeperGame # Import MrKelly's Game

wumpus_game = HuntTheWumpus()
scissors_paper_rock = ScissorsPaperRock()
guessing_game = NumberGuessingGame() 
snake_game = SnakeGame()
tetris_game = TetrisGame()
wumpus_game = HuntTheWumpus()
scissors_paper_rock = ScissorsPaperRock()
ms = MinesweeperGame() # Instantiate Mr Kell's Game

app = Flask(__name__)

direction = "Right"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wumpus', methods=['POST', 'GET'])
def wumpus():
    if request.method == 'POST':
        message = wumpus_game.play(request.form)
    else:
        message = wumpus_game.new_game()
    return render_template('wumpus.html', message=message, game=wumpus_game)

#Will N's Game
@app.route('/ScissorsPaperRock', methods=["POST", "GET"])
def scissorsPaperRock():
    if request.method == 'POST':
        message = scissors_paper_rock.run(request.form)
    else:
        message = ""
    return render_template('ScissorsPaperRock.html', game=scissors_paper_rock, choices=scissors_paper_rock.choices, scores=scissors_paper_rock.scores, message=message)

@app.route('/snake')
def snake():
    '''Displays current snake game board'''
    message = "Welcome to Snake! Press the button to start and use WASD to move"
    return render_template('snake.html', message=message, game=snake_game)

@app.route('/snake/start')
def start(): 
    '''Resets snake game and redirects to main game page'''
    snake_game.new_game()
    return redirect('/snake')

@app.route('/snake/update')
def update(): 
    '''Moves snake one cell in selected direction, and sends status to webpage'''

    if snake_game.game_Won: 
        return "Game Won"

    if not snake_game.game_On: 
        return "Game Over"
    
    snake_game.move(direction) 

    if snake_game.game_Won: 
        return "Game Won"

    if not snake_game.game_On: 
        return "Game Over"
    
    return "OK"

@app.route('/snake/board')
def board(): 
    return render_template('snake_board.html', game=snake_game)

@app.route('/snake/direction/<new_direction>')
def change_direction(new_direction):
    '''Changes direction to selected key input'''
    global direction 

    if new_direction == "Right": 
        if direction == "Left": 
            print("invalid direction")
            return  
    if new_direction == "Left": 
        if direction == "Right": 
            print("invalid direction")
            return  
    if new_direction == "Up": 
        if direction == "Down": 
            print("invalid direction")
            return  
    if new_direction == "Down": 
        if direction == "Up": 
            print("invalid direction")
            return 
    direction = new_direction 
    return "Direction changed"

@app.route('/snake/reset') 
def reset(): 
    snake_game.new_game()
    return "New game started"

# Mr Kelly's Game
@app.route('/minesweeper', methods=['POST', 'GET'])
def minesweeper():
    if request.method == 'POST':
        size = int(request.form['size'])
        mines = int(request.form['mines'] )
        ms.newGame(size, mines)
    else:
        id = request.args.get('id')
        if id:
            ms.click(id)
    return render_template('minesweeper.html', game=ms)
# uses an iframe to render time based content
@app.route('/tetris')
def tetris():
    # init a new game when the tetris is clicked
    tetris_game.clear()
    return render_template('tetris.html', game=tetris_game)

@app.route('/tetris_internal', methods=['POST', 'GET'])
def tetris_internal():
    return tetris_game.frame()

@app.route('/tetris_input/<input>', methods=['POST', 'GET'])
def tetris_input(input):
    # input validation
    if tetris_game.falling_object != None:
        if tetris_game.falling_object.check_collision((-1,0), tetris_game.board_array) and input == 'left':
            tetris_game.falling_object.pos = (tetris_game.falling_object.pos[0] - 1, tetris_game.falling_object.pos[1])
        if tetris_game.falling_object.check_collision((1,0), tetris_game.board_array) and input == 'right':
            tetris_game.falling_object.pos = (tetris_game.falling_object.pos[0] + 1, tetris_game.falling_object.pos[1])
        if input == 'rotate':
            maybe_rotated = tetris_game.falling_object.rotate(tetris_game.board_array)
            if maybe_rotated != None:
                tetris_game.falling_object = maybe_rotated
        if input == 'hard_drop':
            tetris_game.hard_drop()
    return ''

# Declan G's Game:
@app.route('/guess', methods=['POST', 'GET'])
def guess():
    if request.method == 'POST':
        message = guessing_game.play_turn(request.form)
    else:
        message = guessing_game.new_game()
    return render_template('NumberGuessingGame.html', message=message, game=guessing_game)

if __name__ == "__main__":
    app.run()