import pygame
pygame.init()


from pygame_logic import checkLoseCondition, displayWordProgress, getUserGuess, initializeGameState, processGuess, displayResult, checkWinCondition


info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# WIN =  pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Hangman Game")

clock = pygame.time.Clock()

game_state = "menu"

font_big = pygame.font.SysFont('Arial', 80)
font_medium = pygame.font.SysFont('Arial', 46)
font_small = pygame.font.SysFont('Arial', 34)


selected_word = ''
attempts_left = 0
guessed_letters = set()
wrong_letters = set()

WordsList = ["apple", "banana", "grapes", "orange", "mango"]

selected_word = ''
user_guess = ''
initialize_message = ''
validation_message = ''
message_processedGuess = ''
current_guess_char = ''

print(f"Window Size: {WIDTH}x{HEIGHT}")

wrong_letters = set()

def draw_menu():
    WIN.fill((25, 25, 40))

    title   = font_big.render("HANGMAN", True, (255, 215, 0))
    welcome = font_medium.render("Welcome to the Game!", True, (200, 220, 255))
    prompt  = font_small.render("Press Y to Start or N to Quit", True, (150, 170, 200))

    WIN.blit(title,   (WIDTH//2 - title.get_width()//2, 240))  
    WIN.blit(welcome, (WIDTH//2 - welcome.get_width()//2, 360)) 
    WIN.blit(prompt,  (WIDTH//2 - prompt.get_width()//2, 456)) 

def draw_rules():
    WIN.fill((25, 25, 40))

    title = font_big.render("HANGMAN", True, (255, 215, 0))
    rules = [
        "Rules:",
        "1. Enter only one letter (a-z) each turn.",
        "2. Correct letter -> revealed in all positions.",
        "3. Wrong letter -> attempts decrease by 1.",
        "4. Repeated guess -> warning, no attempt loss.",
        "5. You win if all letters are revealed.",
        "6. You lose if attempts reach 0."
    ]

    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    for i in rules:
        rule_text = font_small.render(i, True, (200, 215, 240))
        WIN.blit(rule_text, (WIDTH//2 - rule_text.get_width()//2, 180 + rules.index(i) * 60 ))



def draw_game():
    WIN.fill((25, 25, 40))
    displayWordProgress(WIN, selected_word, guessed_letters, attempts_left)

    display_initialization_text = font_small.render(initialize_message, True, (140, 160, 190))
    WIN.blit(display_initialization_text, (WIDTH//2 - display_initialization_text.get_width()//2, 240))

    validation_text = font_small.render(validation_message, True, (255, 180, 30))
    WIN.blit(validation_text, (WIDTH//2 - validation_text.get_width()//2, 360))

    if message_processedGuess == "Correct Guess!":
        processedGuess_color = (50, 230, 100)
    elif message_processedGuess == "Wrong Guess!":
        processedGuess_color = (255, 80, 80)
    else:
        processedGuess_color = (80, 220, 120)
    processedGuess_text = font_small.render(message_processedGuess, True, processedGuess_color)
    WIN.blit(processedGuess_text, (WIDTH//2 - processedGuess_text.get_width()//2, 480))

    if current_guess_char:
        guess_display = font_small.render(f"Your guess: {current_guess_char}", True, (180, 200, 230))
        WIN.blit(guess_display, (WIDTH//2 - guess_display.get_width()//2, 530))


def draw_result():

    WIN.fill((25, 25, 40))

    displayResult(WIN, isWin, selected_word)



running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    game_state = "rules"
                elif event.key == pygame.K_n:
                    running = False


        elif game_state == "rules":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    selected_word, attempts_left, guessed_letters, wrong_letters, initialize_message = initializeGameState(selected_word, WordsList , attempts_left , wrong_letters , guessed_letters)
                    message_processedGuess = ''
                    current_guess_char = ''
                    game_state = "game"
                elif event.key == pygame.K_n:
                    running = False

        elif game_state == "game":
            if event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key)
                current_guess_char = guess.upper()
                print(f"User Guess: {guess}")
                guess , validation_message = getUserGuess(WIN, guessed_letters, wrong_letters , guess)
                print(f"Processed Guess: {guess}")
                if guess == "z":
                    running = False
                if guess != False:
                    guessed_letters, wrong_letters, attempts_left , message_processedGuess = processGuess(WIN, guess, selected_word, guessed_letters, wrong_letters, attempts_left)
                else:
                    message_processedGuess = ""
                    current_guess_char = ''

                if checkWinCondition(guessed_letters, selected_word):
                    isWin = True
                    game_state = "result"
                if checkLoseCondition(attempts_left):
                    isWin = False
                    game_state = "result"
                
        elif game_state == "result":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "menu"
                elif event.key == pygame.K_n:
                    running = False

    if game_state == "menu":
        draw_menu()
    elif game_state == "rules":
        draw_rules()
    if game_state == "game":
        draw_game()
    if game_state == "result":
        draw_result()
    pygame.display.update()
pygame.quit()
