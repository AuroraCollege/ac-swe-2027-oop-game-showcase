import random

class Game:
    """Base class for all games. Holds shared game behaviour"""

    def __init__(self):
        """Sets up the game and marks it as running"""
        self.game_on = True

    def play_turn(self, form):
        """Placeholder method for child classes to override"""
        return " "

class NumberGuessingGame(Game):
    """A simple number guessing game"""

    def __init__(self):
        """Starts the game and sets default values"""
        super().__init__()
        self.__target = None
        self.attempts = 0
        self.new_game()

    def set_target(self, value):
        """Sets the target number with validation to keep it between 1 and 50"""
        if 1 <= value <= 50:
            self.__target = value
        else:
            return "Target must be between 1 and 50."

    def new_game(self):
        """Starts a new round by picking a random number and resetting attempts"""
        self.set_target(random.randint(1, 50))
        self.attempts = 0
        self.game_on = True
        return "New game started! Guess a number between 1 and 50."

    def guess(self, number):
        """Checks the player's guess and returns a hint or a win message"""
        if not self.game_on:
            return "Game over! Start a new game."

        self.attempts += 1

        if number == self.__target:
            self.game_on = False
            return f"Correct! The number was {self.__target}. You guessed it in {self.attempts} attempts."
        elif number < self.__target:
            return "Too low! Try again."
        else:
            return "Too high! Try again."

    def play_turn(self, form):
        """Handles the form input from Flask and processes the guess"""
        if form.get("number"):
            return self.guess(int(form["number"]))
        return "Please enter a number."
