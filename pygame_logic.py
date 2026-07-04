import pygame
import random

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

font_big = pygame.font.SysFont('Arial', 80)
font_medium = pygame.font.SysFont('Arial', 46)
font_small = pygame.font.SysFont('Arial', 34)


# ===================================================================
# ===================================================================
# def initializeGameState(selected_word, guessed_letters, WordsList , attempts_left , wrong_letters):
    
#     selected_word = getRandomWord(WordsList)
#     guessed_letters = set()
#     attempts_left = 6
#     wrong_letters = set()

#     # print(f"{Yellow}Game Initialization Done, Random Word Is Selected\n")

#     return selected_word, guessed_letters, attempts_left, wrong_letters

# ===================================================================
# ===================================================================



def initializeGameState(selected_word, WordsList , attempts_left , wrong_letters , guessed_letters):
    
    selected_word = getRandomWord(WordsList)
    attempts_left = 6
    guessed_letters = set()
    wrong_letters = set()

    initialize_message = "Game Initialization Done, Random Word Is Selected"

    return selected_word, attempts_left , guessed_letters, wrong_letters, initialize_message




def getRandomWord(WordsList):
    return random.choice(WordsList)




def displayWordProgress(WIN, word, guessed_letters, attempts_left):
    progress = ""
    for letter in word:
        if letter in guessed_letters:
            progress += " " + letter + " "
        else:
            progress += " x "

    progress = progress.strip()
    display_word = font_small.render(progress , True, (255, 255, 255))
    WIN.blit(display_word, (WIDTH//2 - display_word.get_width()//2, 600))

    attempts_left_str = str(attempts_left)
    attempts_text = font_small.render(attempts_left_str, True, (255, 210, 50))
    WIN.blit(attempts_text, (WIDTH//2 - attempts_text.get_width()//2, 660))






def getUserGuess(WIN, guessed_letters, Wrong_letters , guess):
    
    guess = guess.strip().lower()

    if validateGuess(guess):        
        if isRepeatedGuess(guess, guessed_letters, Wrong_letters):
            validation_message = "You have already guessed that letter. Try a different one."
            return False,  validation_message
        else:
            return guess , ""
    else:
        validation_message = "Invalid input. Please enter a single letter (a-z)."
        return False , validation_message



def validateGuess(guess):
    if len(guess) != 1 or not guess.isalpha():
        return False
    return True

def isRepeatedGuess(guess, guessed_letters, Wrong_letters):
    for letter in guessed_letters.union(Wrong_letters):
        if guess == letter:
            return True
    return False


def processGuess(WIN , guess, secret_word, guessed_letters, wrong_letters, attempts_left):
    for letter in secret_word:
        if guess == letter:
            guessed_letters.add(guess)
            message_processedGuess = "Correct Guess!"
            return guessed_letters, wrong_letters, attempts_left , message_processedGuess
    wrong_letters.add(guess)
    attempts_left -= 1
    message_processedGuess = "Wrong Guess!"
    return guessed_letters, wrong_letters, attempts_left , message_processedGuess

def displayResult(WIN, isWin, word):
    if isWin:
        message = f"Congratulations! You guessed the word: {word}"
        win_message_text = font_small.render(message, True, (50, 230, 100))
        WIN.blit(win_message_text, (WIDTH//2 - win_message_text.get_width()//2, 360))
    else:
        message = f"Game Over! The word was: {word}"
        result_text = font_small.render(message, True, (255, 80, 80))
        WIN.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 360))

    returnMessage = "Press Enter to Return to Menu or N to Exit"
    return_message_text = font_small.render(returnMessage, True, (150, 180, 220))
    WIN.blit(return_message_text, (WIDTH//2 - return_message_text.get_width()//2, 480))

def drawHangman(WIN, attempts_left):
    x = WIDTH // 2
    y = 40

    pygame.draw.line(WIN, (160, 160, 190), (x-50, y+170), (x+50, y+170), 4)
    pygame.draw.line(WIN, (160, 160, 190), (x, y), (x, y+170), 4)
    pygame.draw.line(WIN, (160, 160, 190), (x, y), (x+70, y), 4)
    pygame.draw.line(WIN, (160, 160, 190), (x+70, y), (x+70, y+25), 3)

    wrong = 6 - attempts_left

    if wrong >= 1:
        pygame.draw.circle(WIN, (220, 220, 240), (x+70, y+45), 18, 3)
    if wrong >= 2:
        pygame.draw.line(WIN, (220, 220, 240), (x+70, y+63), (x+70, y+130), 3)
    if wrong >= 3:
        pygame.draw.line(WIN, (220, 220, 240), (x+70, y+75), (x+40, y+100), 3)
    if wrong >= 4:
        pygame.draw.line(WIN, (220, 220, 240), (x+70, y+75), (x+100, y+100), 3)
    if wrong >= 5:
        pygame.draw.line(WIN, (220, 220, 240), (x+70, y+130), (x+45, y+165), 3)
    if wrong >= 6:
        pygame.draw.line(WIN, (220, 220, 240), (x+70, y+130), (x+95, y+165), 3)


def checkWinCondition(guessed_letters, selected_word):
    for letter in selected_word:
        if letter not in guessed_letters:
            return False
    return True

def checkLoseCondition(attempts_left):
    if attempts_left == 0:
        return True
    return False
