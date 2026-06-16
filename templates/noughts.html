class TicTacToe:
    def __init__(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.winner = None

    def make_move(self, position):
        """Move Maker, if no one has won then other player make move"""
        if self.board[position] == "" and self.winner is None:
            self.board[position] = self.current_player

            if self.check_winner():
                """Draw! *Blam*"""
                self.winner = self.current_player
            elif "" not in self.board:
                self.winner = "Draw"
            else:
                self.switch_player()

    def switch_player(self):
        """If its X's go then it will be O's go next. Else it's X's go"""
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def check_winner(self):
        """Checks for each win state after each turn"""
        winning_lines = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]

        for a, b, c in winning_lines:
            if (
                self.board[a] != "" and
                self.board[a] == self.board[b] == self.board[c] #youtube assist
            ):
                return True

        return False

    def reset(self): 
        """resets board when told by check_winner"""
        self.board = [""] * 9
        self.current_player = "X"
        self.winner = None