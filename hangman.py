import random
from typing import Self
def Fruit_word_list():
    Fruit_word_list = ('Blackberry', 'Blueberry', 'Cranberry', 'Raspberry', 'Strawberry', 'Lychee', 'Mulberries', 'pineapple','apple','grape','gooseberry','lemon','lime','orange','watermelon','Cantaloupe','dragonfruit')
    return Fruit_word_list
'''dictionary that makes the hangman drawing, 0-6 is how many incorrect guesses we've made'''
def hangman_drawing(): 
    hangman_drawing = {0: (
                       '  ________    ',
                       ' |        |   ',
                       ' |            ',
                       ' |            ',
                       ' |            ',
                       ' |            ',
                       ' |___________ '),

                    
                   1: ( 
                       '  ________    ',
                       ' |        |   ',
                       ' |        O    ',
                       ' |            ',
                       ' |            ',
                       ' |            ',
                       ' |___________ '),
                   2: ( 
                       '  ________    ',
                       ' |        |   ',
                       ' |        O    ',
                       ' |        |    ',
                       ' |            ',
                       ' |            ',
                       ' |___________ '),
                   3: ( 
                       '  ________    ',
                       ' |        |   ',
                       ' |        O    ',
                       ' |       /|    ',
                       ' |            ',
                       ' |            ',
                       ' |___________ '),
                   4: ( 
                       '  ________    ',
                       ' |        |   ',
                       ' |        O   ',
                       ' |       /|\\ ',
                       ' |            ',
                       ' |            ',
                       ' |___________ '),
                   5: ( 
                       '  ________    ',
                       ' |        |   ',
                       ' |        O   ',
                       ' |       /|\\ ',
                       ' |       /    ',
                       ' |            ',
                       ' |___________ '),
                   6: ( 
                       '  ________    ',
                       ' |        |   ',
                       ' |        O   ',
                       ' |       /|\\ ',
                       ' |       / \\  ',
                       ' |            ',
                       ' |___________ ')}
    return hangman_drawing

class Hangman:
    def __init__(self, Fruit_word_list, drawings):
        self.Fruit_word_list = Fruit_word_list
        self.Hangman_drawing = drawings
        self.__answer = random.choice(self.Fruit_word_list)
        self.__wrong_guesses = 0
        self.__guessed_letters = []
        self.__welcome_message = 'Welcome to level 1'
        
       
        self.hint = []
        for letter in self.answer:
            self.hint.append('_')

    def whatever(self):
        return self.__welcome_message 

    '''This is what the player sees when they start the game'''
    def display_man(self):
        display_man = {'====================',
                f'{self.Hangman_drawing[self.__wrong_guesses]}',
                '===================='}
        
        return display_man

    '''This makes the UI for the secret word, look more pretty'''
    def display_hint(self):
        for char in self.__hint:
            print(char, end=' ')
        print()

    
    '''this shows the answer at the end in a pretty way, as welll'''
    def display_answer(self):
        for char in self.hint:
            print(char, end=' ')
        print()

    '''this is the main logic of the game :D'''  
    def play(self):
        def is_running():
             is_running = True
       
        
    '''this starts the game and asks the user for a letter to begin'''
    while is_running():
            Self.display_man()
            Self.display_hint()
            guess = input('Enter a letter: ').lower()
            '''This verification procces stops the user from inputing a number or a word'''
            if len(guess) != 1 or not guess.isalpha():
                print(' You can only guess with letters and one at a time, try again!')
                continue 
            '''this lets the user know that they have used the same letter more than once'''
            if guess in Self.guessed_letters:
                print(f'{guess} has already been guessed, try a different letter!')
                continue
            '''this keeps track of the users guesses'''
            Self.__guessed_letters.append(guess)
            '''this is swapping the underscore for the letter if its the correct one'''
            if guess in Self.answer:
                position = 0
                #looping through each letter in the randomly chosen secret word, and swaps the underscore for the letter, if they got it right
                for letter in self.answer:
                    if letter == guess:
                        Self.__hint[position] = guess

                    position = position + 1
            else:
                Self.__wrong_guesses += 1
#this is what is shown when you have beaten the game
            has_won = True
            for char in self.hint:
                if char == '_':
                    has_won = False


            if has_won == True:
                self.display_man()
                self.display_answer()
                print("Well done, You've won!")
                is_running = False
                continue
#this is what happens when you lose the game
            if self.__wrong_guess >= 6:
                self.display_man()
                self.display_answer()
                print('HAHAH LOLLING YOU LOSE!')
                is_running = False


medium_word_list = ('Barbecue', 'Bolognese', 'Brownie', 'Bruschetta', 'Casserole', 'Cheeseburger', 'Chowder', 'Croissant', 'Doughnut', 'Enchilada', 'Guacamole', 'Hummus', 'Lasagna', 'Macaroni', 'Mayonnaise', 'Nuggets', 'Omelette', 'Pretzels', 'Sandwich', 'Spaghetti')


class MediumHangman(Hangman):
     def __init__(self, word_list, drawings):
         super().__init__(word_list, drawings)
         self.medium_word_list = medium_word_list
         self.welcome_message = 'Welcome to level 2 (medium difficulty) Good luck!'
         return self.welcome_message

   
   

if __name__ == '__main__':
     game = Hangman(Fruit_word_list, hangman_drawing)
     game.play()
        