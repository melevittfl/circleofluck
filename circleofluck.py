import string
from enum import Enum
from rich.console import Console
import getch


console = Console(color_system="auto")


def get_word():
    return input("Please enter a word or phrase for the player to guess: ")


def get_guess():
    print("\n\nPlease guess a letter: ", end="")
    return getch.getch()


def ispunct(ch):
    return ch in string.punctuation


class GuessOutcome(Enum):
    CORRECT = 1
    ALREADY_GUESSED = 2
    INCORRECT = 3


class CircleOfLuck(object):
    def __init__(self, word):
        self.name = "Circle of Luck"
        self.__word = word
        self.__tries = 3
        # self.__state = [' ' if x.isspace() else '*' for x in self.__word]
        self.__guesses = []
        self.__solved = False
        self.__last_correct_guess = None
        self.__state = []
        for x in self.__word:
            if x.isspace():
                self.__state.append(" ")
            elif ispunct(x):
                self.__state.append(x)
            else:
                self.__state.append("*")

    @property
    def state(self):
        return self.__state

    def __set_state(self, guess):
        for i, letter in enumerate(self.__word):
            if letter.casefold() == guess.casefold():
                self.__state[i] = letter

    @property
    def guesses(self):
        return self.__guesses

    @guesses.setter
    def guesses(self, guess):
        self.__guesses.append(guess)

    @property
    def tries(self):
        return self.__tries

    @property
    def solved(self):
        return self.__solved

    @property
    def last_correct_guess(self):
        return self.__last_correct_guess

    def guess(self, letter):
        if letter in self.__guesses:
            return GuessOutcome.ALREADY_GUESSED
        elif letter.casefold() in self.__word.casefold():
            self.__set_state(letter)
            self.__last_correct_guess = letter
            if self.__state == list(self.__word):
                self.__solved = True
            self.guesses = letter
            return GuessOutcome.CORRECT
        else:
            self.guesses = letter
            self.__tries -= 1
            return GuessOutcome.INCORRECT


def underline_print(letter=None):
    if not letter:
        console.print(" ", end="")
    elif ispunct(letter):
        console.print(f"{letter}", end="")
    else:
        console.print(f"{letter}", style="u", end="")
    console.print(" ", end="")


def render(game_state):
    for x in game_state:
        match x:
            case "*":
                underline_print(" ")
            case " ":
                underline_print()
            case _:
                underline_print(x)
    console.print("")
    # console.print(" ".join(output), style='underline')


def article_for_letter(letter):
    an_letters = "aeioumhlnrsx"
    if letter in an_letters:
        return "an"
    else:
        return "a"


def play(game):
    print(f"Welcome to {game.name}\nHere is a word/phrase to guess:")
    render(game.state)
    while not game.solved and (game.tries > 0):
        result = game.guess(get_guess())
        match result:
            case result.CORRECT:
                print(
                    f"There is {article_for_letter(game.last_correct_guess)} {game.last_correct_guess}"
                )
                render(game.state)
            case result.ALREADY_GUESSED:
                print("You tried that letter already...")
                print(",".join(game.guesses))
                render(game.state)
            case result.INCORRECT:
                print(f"Nope, {game.guesses[-1]} isn't part of the phrase")
                render(game.state)
                if game.tries > 0:
                    print(f"You have {game.tries} chances left")
                else:
                    print("Oh dear...you've lost")


if __name__ == "__main__":
    print("Welcome...")
    keep_playing = True

    phrase = get_word()
    console.clear()
    while keep_playing:
        g = CircleOfLuck(phrase)
        play(g)

        if not g.solved:
            answer = input("Do you want to try again? (Y/n) ")
            if answer == "n":
                keep_playing = False
        else:
            print("Well done!")
            keep_playing = False
