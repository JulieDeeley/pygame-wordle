import os
import pygame
import random
import sys
import string # to create keyboard colour key/value pairs
import time # used for keybounce pause so user can't input letters too fast

pygame.init()
clock = pygame.time.Clock()

# Constants for screen size, colors, and grid
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 850
BLACK, WHITE, = (0, 0, 0), (255, 255, 255) 
#DARKER_GREEN = (0, 128, 0)
GREEN = (87, 197, 87)
#OLD_MID_BLUE_GREY = (179, 204, 204)
MID_BLUE_GREY = (133, 173, 173)
DARKER_BLUE_GREY = (102, 153, 153)
DARK_GREY = (50, 50, 50)
MID_GREY = (132, 141, 148)
DIRTY_YELLOW = (227, 193, 100)
LIGHT_GREY = (196, 202, 204)

# Create the game window
pygame.display.set_caption("Julie's Wordle")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Constants for word length, allowed guesses 
WORD_LENGTH = 5
TOTAL_GUESSES_ALLOWED = 5

# Keyboard layout coordinates with width (x, y, width)
keyboard_offset_y = SCREEN_HEIGHT // 4  # starts drawing keyboard 1/4 the way down the screen on y axis
keyboard_layout = {
    "Q": (50, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "W": (110, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "E": (170, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "R": (230, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "T": (290, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "Y": (350, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "U": (410, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "I": (470, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "O": (530, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "P": (590, SCREEN_HEIGHT - 150 - keyboard_offset_y, 50),
    "A": (75, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "S": (135, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "D": (195, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "F": (255, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "G": (315, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "H": (375, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "J": (435, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "K": (495, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "L": (555, SCREEN_HEIGHT - 90 - keyboard_offset_y, 50),
    "ENT": (40, SCREEN_HEIGHT - 30 - keyboard_offset_y, 100),  # Wider ENTER key
    "Z": (150, SCREEN_HEIGHT - 30 - keyboard_offset_y, 50),
    "X": (210, SCREEN_HEIGHT - 30 - keyboard_offset_y, 50),
    "C": (270, SCREEN_HEIGHT - 30 - keyboard_offset_y, 50),
    "V": (330, SCREEN_HEIGHT - 30 - keyboard_offset_y, 50),
    "B": (390, SCREEN_HEIGHT - 30 - keyboard_offset_y, 50),
    "N": (450, SCREEN_HEIGHT - 30 - keyboard_offset_y, 50),
    "M": (510, SCREEN_HEIGHT - 30 - keyboard_offset_y, 50),
    "DEL": (570, SCREEN_HEIGHT - 30 - keyboard_offset_y, 100),  # Wider DELETE key
}

# Constants for grid
GRID_ROWS, GRID_COLS = 5, 5
RECT_WIDTH = SCREEN_WIDTH // GRID_COLS // 2
RECT_HEIGHT = (SCREEN_HEIGHT - 150) // GRID_ROWS // 2
PADDING = 5  # space between grid squares
grid_width = GRID_COLS * RECT_WIDTH
offset_x = (SCREEN_WIDTH - grid_width) // 2
grid_offset_y = SCREEN_HEIGHT - 150 - keyboard_offset_y - (GRID_ROWS * RECT_HEIGHT) - PADDING

# Define key height for the keyboard
key_height = 50  # Set a fixed key height

# Helper functions
def pick_a_word():
    # picks a random word from a file to be the answer to the game
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'five_letter_words.txt')
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if lines:
                return random.choice(lines).strip()
            else:
                print("ERROR: Word list is empty.")
                sys.exit()
    except (FileNotFoundError, IOError) as e:
        print(f'ERROR: {e}')
        sys.exit()  # Exit if the word list is missing

def check_guess(answer, current_guess, keyboard_colours):   
    # checks the guess letter by letter against the answer
    # 'feedback' changes the colours of the grid squares to match the status of the guessed letter
    # 'keyboard colour' tracks letter colours to change the key colours on the keyboard by keeping a dictionary
    # of letter indexes to colour values
  
    print(f"DEBUG: The word is {answer}")  # Debugging the word  
    feedback = [WHITE] *GRID_COLS
    remaining_letters = list(answer) # IMPORTANT! a list changed here will change in the main function
    # so use a new list instead! You can also copy the list for a local copy with answer=list(answer)
    
    # First pass to handle correct letters in the correct place which will be added to feedback as green
    # and added to keyboard colours as a letter, colour pair
    for i in range (len(current_guess)):
        if current_guess[i] == answer[i]:
            feedback[i] = GREEN 
            remaining_letters[i] = None # replace the letter in  remaining_letters with None.
            keyboard_colours[current_guess[i].upper()] = GREEN #keyboard key colour changed to green
  
    # Second pass to handle incorrect positions and absent letters.
    # Correct guesses in incorrect positions will be added to feedback as DIRTY_YELLOW
    # Incorrect letters in the guess will result in a LIGHT_GREY
    
    for j in range(len(current_guess)):
        if current_guess[j] in  remaining_letters and feedback[j] == WHITE: #if there is a matching letter left in the word and the spot in feedback is 'WHITE', add string yellow
            feedback[j] = DIRTY_YELLOW # turn the empty slot into yellow string           
            remaining_letters[ remaining_letters.index(current_guess[j])] = None # find the letter in  remaining_letters
            #and replace it with None

            if keyboard_colours[current_guess[j].upper()] != GREEN: # as long as it isn't green
                keyboard_colours[current_guess[j].upper()] = DIRTY_YELLOW # turn the keyboard key into yellow
              
        elif feedback[j] == WHITE: # if the feedback is still white
            feedback[j] = MID_GREY

            if current_guess[j].upper() not in answer\
                and keyboard_colours[current_guess[j].upper()] != GREEN\
                and keyboard_colours[current_guess[j].upper()] != DIRTY_YELLOW: #if the letter is  not  in the answer
                keyboard_colours[current_guess[j].upper()] = MID_GREY # turn the keyboard key into MID_GREY            
    #print(f'feedback: {feedback}') #debug
    return feedback, keyboard_colours

def draw_grid(colour_array):
    # takes the 2-D colour array and displays each guessed letters status by colour

    for row in range(GRID_ROWS):
        outline_width = 3
        for col in range(GRID_COLS):
            # Draw the white rectangle with a black outline
            pygame.draw.rect(
                screen, colour_array[row][col],  # Colour for the fill
                (offset_x + col * RECT_WIDTH + PADDING, grid_offset_y + row * RECT_HEIGHT + PADDING,
                 RECT_WIDTH - 2 * PADDING, RECT_HEIGHT - 2 * PADDING))  # Rectangle dimensions
            
            # Draw the light grey outline around the rectangle
            pygame.draw.rect(
                screen, LIGHT_GREY,  # color for the outline
                (offset_x + col * RECT_WIDTH + PADDING, grid_offset_y + row * RECT_HEIGHT + PADDING,
                 RECT_WIDTH - 2 * PADDING, RECT_HEIGHT - 2 * PADDING), outline_width)  

def draw_keyboard(keyboard_colours):
    #draw the on screen keyboard
    font = pygame.font.Font(None, 30)
    for  key, pos in keyboard_layout.items():
        x, y, width = pos  # Unpack the x, y, and width values

        # Draw the key with the appropriate width, colour from keyboard_colours dict, default LIGHT_GREY for del and enter
        pygame.draw.rect(screen, keyboard_colours.get(key, LIGHT_GREY), (x, y, width, key_height), border_radius=10)
        
        # Render the key text and center it
        text = font.render(key, True, BLACK) # string, antialias, colour
        screen.blit(text, (x + (width - text.get_width()) // 2, y + (key_height - text.get_height()) // 2))

def display_guesses(guess_array):
    # display all guesses so far
    font = pygame.font.Font(None, 50)
    for row_idx, guess in enumerate(guess_array):
        for i, letter in enumerate(guess):   # Loop through each letter in the guess
            display_text = font.render(letter.upper(), True, BLACK)
            screen.blit(display_text, (offset_x + i * RECT_WIDTH + PADDING + 15, grid_offset_y + row_idx * RECT_HEIGHT + PADDING + 15))

def game_over_screen(result, answer):
    # render game over or you win message
    font = pygame.font.Font(None, 50)
    message = "You Win!" if result == "win" else "Game Over!"
    text = font.render(message, True, GREEN if result == "win" else DARK_GREY)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 380))


    # If the result is 'lose', display the correct answer message
    if result == "lose":
        message = "The answer was "+ answer +'.'
        text = font.render(message, True, MID_BLUE_GREY)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT -150))  

    # Display Play Again or Quit option
    play_again_text = font.render("To play again, click here.", True, MID_BLUE_GREY)
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + -340))
    pygame.display.flip()

def await_player_response():
    # Wait for user to click Play Again or Quit
    waiting_for_response = True
    while waiting_for_response:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + -340, 200, 50).collidepoint(mouse_pos):  # Check if "Play Again" is clicked
                    guess_the_word()  # Restart the game
                    waiting_for_response = False

def display_guess_in_progress(current_guess, current_row):
    if current_row < GRID_ROWS:  # Make sure we don't exceed the maximum number of rows
        font = pygame.font.Font(None, 50)
        for i, letter in enumerate(current_guess):
            display_text = font.render(letter.upper(), True, BLACK)
            screen.blit(display_text, (offset_x + i * RECT_WIDTH + PADDING + 15, grid_offset_y + current_row * RECT_HEIGHT + PADDING + 15))  # +15 to move it right and down

def delay_key_bounce(last_key_time, debounce_time):
    # delays key input so no accidental fast keypresses are made
    current_time = time.time() # present time
    if current_time - last_key_time > debounce_time: # has delay time passed?
        last_key_time = current_time # if so update the time

def check_if_won(current_guess, answer, game_over, current_row,result):
    # check to see if player won or lost
    if "".join(current_guess) == answer:
        result = "win"
        game_over = True
    elif current_row + 1 == TOTAL_GUESSES_ALLOWED:
        result = "lose"
        game_over = True
    return result, game_over

def guess_the_word():
    # Main game loop
    running = True
    game_over = False
    selected_key = None
    current_guess = []  # list to store each individual guess
    guess_array = []  # list array to store all guesses
    colour_array =[[WHITE for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]  # list array to store feedback colors, default is white until changed by a guess
    current_row = 0  # Keep track of the row where the current guess is being entered
    result = ''
    keyboard_colours  = {letter: LIGHT_GREY for letter in string.ascii_uppercase} # reset keyboard colours
    last_key_time = 0 # used to delay input
    debounce_time = 0.2  # seconds, used to delay input
    answer = pick_a_word()  # Pick the word at the start of the game
    #print(f"DEBUG: The word is {answer}")  # Debugging the word   
         
    while running:
        screen.fill(WHITE)  # Clear screen
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                delay_key_bounce(last_key_time, debounce_time)
                mouse_pos = event.pos  # mouse_pos records where
                for key, pos in keyboard_layout.items():
                    x, y, width = pos  # Unpack the x, y, and width values
                    rect = pygame.Rect(x, y, width, key_height)  # Use the actual width from the layout

                    if rect.collidepoint(mouse_pos):  # if the rect and mouse pos match
                        selected_key = key
                        #print(f"Selected Key: {selected_key}")  # Debugging the key selection
                        if selected_key == 'DEL' and len(current_guess) > 0:
                            current_guess.pop()  # Remove last character
                        elif selected_key != 'DEL' and selected_key != 'ENT' and len(current_guess) < WORD_LENGTH :
                            current_guess.append(selected_key.lower())  # Add the selected key to current_guess
                            #print(current_guess) #debug current_guess

                        # If "ENTER" is pressed and guess is complete, check the guess
                        if selected_key == 'ENT' and len(current_guess) == WORD_LENGTH: # enter is pushed

                            # add current guess to guess_array
                            guess_array.append(current_guess)
                            #print(guess_array) #debug guess_array
                            colour_array[current_row], keyboard_colours=(check_guess(answer, current_guess,keyboard_colours)) # check current guess against answer, returns colours from feedback var to append to colour_array
                            draw_grid(colour_array) #update the grid colours from the user guess
                            # Check for win/lose
                            result, game_over= check_if_won(current_guess, answer, game_over, current_row, result)
                            current_row += 1  # Increment row for the next guess
                            current_guess = []  # Reset current_guess after pressing Enter
        # Drawing
        draw_grid(colour_array)
        draw_keyboard(keyboard_colours)

        # display all guesses
        display_guesses(guess_array)

        # Display current_guess ongoing
        display_guess_in_progress(current_guess, current_row)

        # monitor game over status
        if game_over:
            game_over_screen(result, answer)
            await_player_response()
       
        pygame.display.flip()  # Update display       
        # Limit FPS to 60
        clock.tick(60)
    pygame.quit()

# Start the game
guess_the_word()