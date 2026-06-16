from flask import Flask, render_template, request, redirect
from wumpus import HuntTheWumpus
from ScissorsPaperRock import ScissorsPaperRock
from snake import SnakeGame
wumpus_game = HuntTheWumpus()
scissors_paper_rock = ScissorsPaperRock()
snake_game = SnakeGame()
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

if __name__ == "__main__":
    app.run()