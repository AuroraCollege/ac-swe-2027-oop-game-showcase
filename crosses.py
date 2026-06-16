from flask import Flask, render_template, redirect, url_for
import TicTacToe
import webbrowser

app = Flask(__name__)

game = TicTacToe()

@app.route("/")
def noughts():
    return render_template("noughts.html", game=game)

@app.route("/move/<int:position>")
def move(position):
    game.make_move(position)
    return redirect(url_for("noughts"))

@app.route("/reset")
def reset():
    game.reset()
    return redirect(url_for("noughts"))

if __name__ == "__main__":
    app.run(debug=True)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")
