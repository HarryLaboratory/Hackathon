import random

class HangmanGame:
    def __init__(self):
        self.categories = ['animals', 'food', 'inspirational']
        self.current_word = ''
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 3
        self.win_count = 0

    def choose_word(self, category):
        """Choose a word based on the category."""
        if category == 'animals':
            words = ['lion', 'elephant', 'panther']
        elif category == 'food':
            words = ['pizza', 'burger', 'pasta']
        elif category == 'inspirational':
            words = ['hope', 'love', 'believe']

        self.current_word = random.choice(words)

    def display_word(self):
        """Show current state of the word (hidden letters and guesses)."""
        return ''.join([letter if letter in self.guessed_letters else '_' for letter in self.current_word])

    def guess(self, letter):
        """Handle a guess. Return True if the game is won, False if the game is over."""
        if letter in self.current_word:
            self.guessed_letters.add(letter)
            if all(letter in self.guessed_letters for letter in self.current_word):
                return True  # Game win
        else:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.max_wrong_guesses:
                return False  # Game over
        return None  # Continue game

    def print_jigsaw_face(self):
        """Print the Jigsaw face when the player loses."""
        jigsaw_face = '''
         ___
        | O O |
        |  ~  |
         \\___/
        '''
        print(jigsaw_face)


