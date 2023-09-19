from pandas import read_csv  #for the creation of the dictionary
import random as rand  # to use a random number to pick the wordle
# Creating the dictionary
diction = list(
    read_csv("https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt")
    ["which"])
diction.append('which')

# Called at the beginning, makes the 'wordle'
def pick_word():
    global wordle
    wordle_i = rand.randint(0, len(diction))
    wordle = diction[wordle_i]


# How the user is asked for their guess
def guess():
    user_choice = input("Enter your guess: ").lower(
    )  # I converted it to .lower() to deal with different formatting that the user may use
    while user_choice not in diction:  #handles improper guesses
        if (user_choice.lower() == "reveal"):
            stop = True
            break
        if len(user_choice) > 5:
            user_choice = input(
                "Guessed word is too long, it needs to be 5 letters long. Enter your guess: "
            )
        else:
            user_choice = input("Not a word. Enter your guess: ")
    return user_choice


def convert_guess(user_choice):
  global counter
  global repC
  global rep1C
  ret = []
  wordleL = [i for i in wordle.upper()]
  repW = ""
  rep1W = ""
  for i in range(5):
    if wordleL.count(wordle[i]):
      if repW == wordleL[i]:
        rep1W = wordleL[i]
      else:
        repW = wordleL[i]
      
  
  choiceL = [i for i in user_choice.upper()]
  
  for i in range(5):
# Right letter, right place
    if choiceL[i] == wordleL[i]:
      ret.append("  " + choiceL[i] + "  ")
      wordleL[i]="0"
          
# Right letter, wrong place
    elif choiceL[i] in wordleL:

      if (repW == choiceL[i]) or (rep1W == choiceL[i]):
        if choiceL.count(choiceL[i]) == 2:
          if counter > 2:
            ret.append(" [" + choiceL[i] + "] ")
          else: 
            ret.append(" (" + choiceL[i] + ") ")
            counter += 1
        else:
          ret.append(" (" + choiceL[i] + ") ")
      elif (repC == choiceL[i]) or (rep1C == choiceL[i]):
        if repC == repW:
          if choiceL.count(choiceL[i]) == 2:
            if counter > 2:
              ret.append(" [" + choiceL[i] + "] ")
            else: 
              ret.append(" (" + choiceL[i] + ") ")
              counter += 1
          else:
            ret.append(" [" + choiceL[i] + "] ")
        else:
          ret.append(" [" + choiceL[i] + "] ")
      
      elif choiceL.count(choiceL[i]) > 1:
        to_add = True
        
        if repC == choiceL[i]:
          rep1C = choiceL[i]
        else:
          repC = choiceL[i]
          
        for j in range(5):
          # Searches through the rest of the word to see if the letter matches anywhere
          if (choiceL[j] == wordleL[j]) and (j > i):
            to_add = False
            
        if to_add:  # If the letter doesn't match
          ret += " (" + choiceL[i] + ") "
          wordleL[i]="0"
        else:
          ret += " [" + choiceL[i] + "] "
      else:
        ret += " (" + choiceL[i] + ") "
        wordleL[i]="0"
      

# Wrong letter
    else:
        ret.append(" [" + choiceL[i] + "] ")

  print(''.join(ret))  # Making the list into a string that can be printed


def gameplay():
  global counter
  global repC
  global rep1C
  global stop
  global user_choice
  print("""Rules of the game:
  Try to guess the 'Wordle', a random 5-letter word, in as few guesses as possible
  After every guess, your word will be evaluated 
    if a letter is in [brackets] it is completely incorrect
    if a letter is in (parantheses) then it is in the word but the wrong place
    if a letter is alone it is in the right place
  If you wish to forfeit, type 'reveal', and your session will end and the word will be revealed
  Good Luck!
""" + "-" * 70 + "\n")
  pick_word()
  counter = 0
  repC = ""
  rep1C = ""
  stop = False
  user_choice = guess()
  if stop:  # When 'reveal' is inputted, the game will end
    print("The correct word was " + wordle.upper())
  else:
    convert_guess(user_choice)
    while user_choice != wordle:  # The game will continue until the user guesses correctly
      print("")
      user_choice = guess()
      if stop:
        print("The correct word was " + wordle.upper())
        break
      else:
        convert_guess(user_choice)
  if (user_choice.lower() != "reveal"):
    print("\nYou guessed correctly, good job!")
    print(repC)  


gameplay()

