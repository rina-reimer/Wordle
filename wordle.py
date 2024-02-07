from pandas import read_csv  # for the creation of the dictionary
import random as rand  # to use a random number to pick the wordle


class Wordle:
    # Constructor -> creates new Wordle object
    def __init__(self) -> None:
        self.diction = list(read_csv("https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt")["which"])
        self.diction.append('which')
        wordle_i = rand.randint(0, len(self.diction))
        self.wordle = self.diction[wordle_i]
        self.word_dict = {}
        for s in self.wordle:
            if s in self.word_dict.keys():
                self.word_dict[s.upper()] = self.word_dict.get(s)
            else:
                self.word_dict[s.upper()] = 1
        self.user_choice = ""     # changes at every guess
        self.stop = False

    # How the user is asked for their guess
    def guess(self):
        self.user_choice = input("Enter your guess: ").lower()    # Deal with different formatting that the user may use
        while self.user_choice not in self.diction:     # handles improper guesses
            if (self.user_choice.lower() == "reveal"):
                self.stop = True
                break
            if len(self.user_choice) > 5:
                self.user_choice = input("Guessed word is too long, it needs to be 5 letters long. Enter your guess: ")
            else:
                self.user_choice = input("Not a word. Enter your guess: ")

    def convert_guess(self):
        ret = ["_", "_", "_", "_", "_"]
        wordleL = [i for i in self.wordle.upper()]
        choiceL = [i for i in self.user_choice.upper()]
        for i in range(5):    # Right letter, right place
            if choiceL[i] == wordleL[i]:
                ret[i] = "  " + choiceL[i] + "  "
                self.word_dict[wordleL[i]] = self.word_dict.get(wordleL[i]) - 1
                wordleL[i] = "-"
        for i in range(5):
            if choiceL[i] in wordleL:   # Right letter, wrong place
                if self.word_dict.get(choiceL[i]) != 0:
                    ret[i] = " (" + choiceL[i] + ") "
                    self.word_dict[wordleL[i]] = self.word_dict.get(wordleL[i]) - 1
                else:
                    ret[i] = " [" + choiceL[i] + "] "
            elif wordleL[i] != "-":   # Wrong letter
                ret[i] = " [" + choiceL[i] + "] "
        print(''.join(ret))  # Making the list into a string that can be printed

    def gameplay(self):
        print("""Rules of the game:
                  Try to guess the 'Wordle', a random 5-letter word, in as few guesses as possible
                  After every guess, your word will be evaluated
                    if a letter is in [brackets] it is completely incorrect
                    if a letter is in (parantheses) then it is in the word but the wrong place
                    if a letter is alone it is in the right place
                  If you wish to forfeit, type 'reveal', and your session will end and the word will be revealed
                  Good Luck!
                """ + "-" * 70 + "\n")
        self.guess()
        if self.stop:  # When 'reveal' is inputted, the game will end
            print("The correct word was " + self.wordle.upper())
        else:
            self.convert_guess()
            while self.user_choice != self.wordle:  # The game will continue until the user guesses correctly
                self.guess()
                if self.stop:
                    print("The correct word was " + self.wordle.upper())
                    break
                else:
                    self.convert_guess()
        if (self.user_choice.lower() != "reveal"):
            print("\nYou guessed correctly, good job!")

Wordle.gameplay(Wordle())
