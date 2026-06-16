from flask import Flask, render_template, request
from wumpus import HuntTheWumpus
from ScissorsPaperRock import ScissorsPaperRock

from minesweeper import MinesweeperGame # Import MrKelly's Game

wumpus_game = HuntTheWumpus()
scissors_paper_rock = ScissorsPaperRock()

ms = MinesweeperGame() # Instantiate Mr Kell's Game

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

if __name__ == "__main__":
    app.run()