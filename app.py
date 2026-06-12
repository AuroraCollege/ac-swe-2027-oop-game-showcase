from flask import Flask, render_template, request
from wumpus import HuntTheWumpus
from ScissorsPaperRock import ScissorsPaperRock
wumpus_game = HuntTheWumpus()
scissors_paper_rock = ScissorsPaperRock()
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

@app.route('/ScissorsPaperRock', methods=["POST", "GET"])
def scissorsPaperRock():
    if request.method == 'POST':
        message = scissors_paper_rock.run(request.form)
    else:
        message = ""
    return render_template('ScissorsPaperRock.html', game=scissors_paper_rock, choices=scissors_paper_rock.choices, scores=scissors_paper_rock.scores, message=message)

if __name__ == "__main__":
    app.run()