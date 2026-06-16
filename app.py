from flask import Flask, render_template, request
from wumpus import HuntTheWumpus
from ScissorsPaperRock import ScissorsPaperRock

from minesweeper import MinesweeperGame # Import MrKelly's Game

wumpus_game = HuntTheWumpus()
scissors_paper_rock = ScissorsPaperRock()

ms = MinesweeperGame() # Instantiate Mr Kell's Game

from tetris import TetrisGame
wumpus_game = HuntTheWumpus()
scissors_paper_rock = ScissorsPaperRock()
tetris_game = TetrisGame()
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run()