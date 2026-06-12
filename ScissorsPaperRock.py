import random
choices = ["rock", "paper", "scissors", "spock", "lizard"]
class ScissorsPaperRock():
    def __init__(self):
        self.player = Player()
        self.computer = Computer()
        self.choices = choices
        self.scores = [0, 0]
        self.message = "Scissors Paper Rock"
        self.lastPlayerChoice = "lizard"
    def run(self, form):
        '''Computes the full round. Should be called by app with the request.form.'''
        self.playerChoice = form["choice"]
        self.computerChoice = self.computer.choose(self.lastPlayerChoice)
        self.message = self.award_winner(self.calc_winner())
        self.message += " The computer picked " + self.computerChoice + "." + " You picked: " + self.playerChoice
        self.lastPlayerChoice = self.playerChoice
        self.assemble_scores()
        return self.message
    def assemble_scores(self):
        '''Creates a list of both player scores.'''
        self.scores = [self.player.score, self.computer.score]
    def calc_winner(self):
       '''True == Player wins and False == computer win, None means tie. Runs the choices and decides winner.'''
       if self.playerChoice == self.computerChoice:
           return None
       elif self.playerChoice == "rock":
           if self.computerChoice == "paper" or self.computerChoice == "spock":
               return False
           else:
               return True
       elif self.playerChoice == "scissors":
           if self.computerChoice == "rock" or self.computerChoice == "spock":
               return False
           else:
               return True
       elif self.playerChoice == "paper":
           if self.computerChoice == "scissors" or self.computerChoice == "lizard":
               return False
           else:
               return True
       elif self.playerChoice == "spock":
           if self.computerChoice == "paper" or self.computerChoice == "lizard":
               return False
           else:
               return True
       elif self.playerChoice == "lizard":
           if self.computerChoice == "rock" or self.computerChoice == "scissors":
               return False
           else:
               return True
    def award_winner(self, winner):
        '''Tells which object to add score and updates the message being sent to the app.py.'''
        if winner == True:
            self.player.updt_score()
            self.message = "YOU won."
            return "YOU won."
        elif winner == False:
            self.computer.updt_score()
            self.message = "Computer won."
            return "Computer won."
        else:
            return "It was a tie!"
class Player():
    '''The human player'''
    def __init__(self):
        self.score = 0
    def updt_score(self):
        '''Adds one to score.'''
        self.score += 1
    def display_score(self):
        '''Prints the score.'''
        print(self.score)
    def choose(self):
        '''Prompts user for an input'''
        return input("Scissors, paper, rock: ")

       
class Computer(Player):
    '''The computer player'''
    def choose(self, lastPlayerChoice):
        '''Picks a random choice 50% of the time. The other 50% of the time picks one of the winning picks for the players last pick.'''
        if random.randint(0, 1) == 1:
            if lastPlayerChoice == "rock":
                if random.randint(0, 1) == 1:
                    return "paper"
                else:
                    return "spock"
            elif lastPlayerChoice == "paper":
                if random.randint(0, 1) == 1:
                    return "scissors"
                else:
                    return "lizard"
            elif lastPlayerChoice == "scissors":
                if random.randint(0, 1) == 1:
                    return "rock"
                else:
                    return "spock"
            elif lastPlayerChoice == "lizard":
                if random.randint(0, 1) == 1:
                    return "scissors"
                else:
                    return "rock"            
            elif lastPlayerChoice == "spock":
                if random.randint(0, 1) == 1:
                    return "lizard"
                else:
                    return "paper"
        else:
            return choices[random.randint(0, 4)]
        

if __name__ == "__main__":
    game = ScissorsPaperRock()