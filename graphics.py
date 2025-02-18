import pygame
from game_logic import move_robot, pick_up_rock, drop_rock, get_game_state, GRID_SIZE
import time
import json  # Import the json module for saving data
import os  # Import the os module

pygame.init()

# Screen and grid settings
CELL_SIZE = 80
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moonrock Collection Game")

# Load and scale images
try:
    robot_img = pygame.image.load("robot.png")
    robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))

    moonrock_img = pygame.image.load("moonrock.png")
    moonrock_img = pygame.transform.scale(moonrock_img, (CELL_SIZE, CELL_SIZE))

    stargate_img = pygame.image.load("stargate.png")
    stargate_img = pygame.transform.scale(stargate_img, (CELL_SIZE * 2, CELL_SIZE * 2))
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)
LIGHT_BLUE = (135, 206, 235)  # For leaderboard background

# Font setup
FONT_FILENAME = "Phantomonia.ttf"  # Just the filename
FONTS_DIR = "fonts"  # Directory where fonts are stored
FONT_PATH = os.path.join(FONTS_DIR, FONT_FILENAME)  # Full path to the font

print(f"Attempting to load font from: {FONT_PATH}")  # DEBUG: Print the font path

font = None  # Initialize font outside the try block
large_font = None
title_font = None
instruction_font = None
leaderboard_font = None

try:
    # Ensure the fonts directory exists
    if not os.path.exists(FONTS_DIR):
        print(f"Creating fonts directory: {FONTS_DIR}")
        os.makedirs(FONTS_DIR)  # Create the directory

    # Attempt to load the font
    font = pygame.font.Font(FONT_PATH, 36)
    large_font = pygame.font.Font(FONT_PATH, 72)
    title_font = pygame.font.Font(FONT_PATH, 60)
    instruction_font = pygame.font.Font(FONT_PATH, 30)
    leaderboard_font = pygame.font.Font(FONT_PATH, 28)

    print(f"Successfully loaded font from: {FONT_PATH}")  # Debug: Success message

except FileNotFoundError:
    print(f"Error: Font file not found! Please ensure '{FONT_FILENAME}' is in the '{FONTS_DIR}' directory.")
    print(f"The full path being checked is: {FONT_PATH}")
    print("Falling back to default font.")
    font = pygame.font.Font(None, 36)  # Fallback to default
    large_font = pygame.font.Font(None, 72)
    title_font = pygame.font.Font(None, 60)
    instruction_font = pygame.font.Font(None, 30)
    leaderboard_font = pygame.font.Font(None, 28)

except pygame.error as e:
    print(f"Error loading font '{FONT_FILENAME}' from '{FONT_PATH}': {e}")
    print("This could indicate a corrupted font file or a Pygame issue.")
    print("Falling back to default font.")
    font = pygame.font.Font(None, 36)  # Fallback to default
    large_font = pygame.font.Font(None, 72)
    title_font = pygame.font.Font(None, 60)
    instruction_font = pygame.font.Font(None, 30)
    leaderboard_font = pygame.font.Font(None, 28)

# Load Sounds
try:
    pickup_sound = pygame.mixer.Sound("a_robot_beeping.wav")
    drop_sound = pygame.mixer.Sound("a_robot_beeping-2.wav")
except pygame.error as e:
    print(f"Error loading sound: {e}")
    pickup_sound = None
    drop_sound = None

# Game state
game_won = False
TOTAL_ROCKS = 5
start_time = 0
end_time = 0
game_started = False
instructions_displayed = False
username_entered = False  # Username has been entered?
username = ""  # Initialize username

# Load Leaderboard data
LEADERBOARD_FILE = "leaderboard.json"  # Added path
leaderboard_data = []

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return empty list if file not found
    except json.JSONDecodeError:
        print("Error decoding leaderboard.json. Using an empty leaderboard.")
        return []

def save_leaderboard():
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard_data, f)

leaderboard_data = load_leaderboard()

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to display text with word wrapping
def draw_text_with_wrapping(surface, text, font, color, rect):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_rect = font.render(test_line, True, color).get_rect()
        if test_rect.width <= rect.width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))

    y_offset = rect.top
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(rect.centerx, y_offset + text_surface.get_height() // 2))
        surface.blit(text_surface, text_rect)
        y_offset += text_surface.get_height()

# Function to handle the username input screen
def handle_username_input(event):
    global username, username_entered, font # Added variable for the font
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            username_entered = True
            print(f"Username entered: {username}")  # Debug: Verify username
        elif event.key == pygame.K_BACKSPACE:
            username = username[:-1]  # Delete last character
        else:
            username += event.unicode  # Add typed character

# Main game loop
running = True
while running:
    # --- EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not username_entered:
            handle_username_input(event)  # Process events for username input
        else:
            if event.type == pygame.KEYDOWN:
                if not game_started and not instructions_displayed:
                    instructions_displayed = True
                elif not game_started and instructions_displayed:
                    game_started = True
                    start_time = time.time()
                elif game_started and not game_won:
                    if event.key == pygame.K_SPACE:
                        if pick_up_rock() and pickup_sound:
                            pygame.mixer.Sound.play(pickup_sound)
                    elif event.key == pygame.K_RETURN:
                        if drop_rock() and drop_sound:
                            pygame.mixer.Sound.play(drop_sound)

                    # Move robot based on key press
                    if event.key == pygame.K_w:
                        move_robot(0, -1)
                    elif event.key == pygame.K_s:
                        move_robot(0, 1)
                    elif event.key == pygame.K_a:
                        move_robot(-1, 0)
                    elif event.key == pygame.K_d:
                        move_robot(1, 0)

    # --- GAME STATE UPDATE (Get the latest info!)
    if game_started and not game_won and username_entered:
        game_state = get_game_state()
        robot_position = game_state["robot_position"]
        moonrocks = game_state["moonrocks"]
        score = game_state["score"]
        carrying_rock = game_state["carrying_rock"]

        # Debugging information
        print(f"Moonrocks remaining: {len(moonrocks)}, Score: {score}, Carrying: {carrying_rock}, Game Won: {game_won}")

        # Check for win condition (all rocks delivered)
        if len(moonrocks) == 0 and score == TOTAL_ROCKS and not carrying_rock:
            game_won = True
            end_time = time.time()
            total_time = end_time - start_time  # capture game time

            # Store the score and username
            new_score = {"username": username, "time": total_time}
            leaderboard_data.append(new_score)

            # Sort the leaderboard by time (ascending)
            leaderboard_data = sorted(leaderboard_data, key=lambda x: x["time"])

            # Keep only the top 10 scores
            leaderboard_data = leaderboard_data[:10]

            # Save the updated leaderboard
            save_leaderboard()
            print("WINNING CONDITION MET!")

    # --- DRAWING
    screen.fill(BLACK)  # Set background color to black

    if not username_entered:
        # Draw the username input screen
        text_surface = title_font.render("Enter your name:", True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text_surface, text_rect)

        username_surface = font.render(username, True, WHITE)
        username_rect = username_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(username_surface, username_rect)

        instructions_text = "Press ENTER to submit"
        instructions_surface = font.render(instructions_text, True, WHITE)
        instructions_rect = instructions_surface.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))
        screen.blit(instructions_surface, instructions_rect)

    elif not game_started and not instructions_displayed:
        # Draw the start screen
        title_text = title_font.render("Welcome to StarGate!", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        instructions_text = "Press any key to continue to Instructions"
        instructions_rect = pygame.Rect(WIDTH // 6, HEIGHT // 2, WIDTH * 2 // 3, HEIGHT // 2)
        draw_text_with_wrapping(screen, instructions_text, font, WHITE, instructions_rect)

    elif not game_started and instructions_displayed:
        # Draw instructions screen
        instructions_title = font.render("Instructions", True, WHITE)
        instructions_title_rect = instructions_title.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        screen.blit(instructions_title, instructions_title_rect)

        instructions_text = "Can you help Bobot pick up the moon rocks and deliver them safely to Stargate? Use W, A, S, D to move around. Press SPACE to pick up a rock and ENTER to drop it off."
        instructions_rect = pygame.Rect(WIDTH // 6, HEIGHT // 3, WIDTH * 2 // 3, HEIGHT * 2 // 3)
        draw_text_with_wrapping(screen, instructions_text, instruction_font, WHITE, instructions_rect)

        continue_text = font.render("Press any key to start!", True, WHITE)
        continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT * 5 // 6))
        screen.blit(continue_text, continue_rect)

    elif game_started and not game_won and username_entered:
        # Draw the game normally if not won
        # Draw grid lines
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)

        # Draw Stargate zone as a 2x2 area
        stargate_top_left = (6, 6)
        screen.blit(stargate_img, (stargate_top_left[0] * CELL_SIZE, stargate_top_left[1] * CELL_SIZE))

        # Draw moonrocks from the global set
        for rock in moonrocks:
            screen.blit(moonrock_img, (rock[0] * CELL_SIZE, rock[1] * CELL_SIZE))

        # Draw robot (based on robot_position)
        screen.blit(robot_img, (robot_position[0] * CELL_SIZE, robot_position[1] * CELL_SIZE))

        # Display Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display Carrying Status
        carrying_text = font.render(f"Carrying: {'Yes' if carrying_rock else 'No'}", True, WHITE)
        screen.blit(carrying_text, (10, 40))

        # Display Timer
        elapsed_time = time.time() - start_time
        timer_text = font.render(f"Time: {elapsed_time:.1f}s", True, WHITE)
        screen.blit(timer_text, (10, 70))
    else:
        # Draw the winning screen and leaderboard
        screen.fill(GOLD)
        win_text = large_font.render("You Won!", True, BLACK)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))
        screen.blit(win_text, win_rect)

        # Display time taken
        total_time = end_time - start_time
        time_text = font.render(f"Time Taken: {total_time:.1f}s", True, BLACK)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 8))
        screen.blit(time_text, time_rect)

        stay_tuned_text = font.render("Stay tuned for more levels!", True, BLACK)
        stay_tuned_rect = stay_tuned_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 8))
        screen.blit(stay_tuned_text, stay_tuned_rect)

        # Display the Leaderboard
        leaderboard_x = WIDTH // 4  # Start at 1/4 of the screen width
        leaderboard_y = HEIGHT // 2  # Start at the middle of the screen

        # Leaderboard title with background
        leaderboard_title = large_font.render("Leaderboard", True, BLACK)
        leaderboard_title_rect = leaderboard_title.get_rect(center=(WIDTH // 2, leaderboard_y))

        # Draw background for the leaderboard title
        leaderboard_bg_rect = leaderboard_title_rect.inflate(20, 10)  # Add padding
        pygame.draw.rect(screen, LIGHT_BLUE, leaderboard_bg_rect)  # Draw the rectangle
        screen.blit(leaderboard_title, leaderboard_title_rect)  # Then draw the text on top

        # Adjust the starting Y position for the list of scores
        leaderboard_y += leaderboard_title.get_height()

        for i, score_data in enumerate(leaderboard_data):
            # Create the text for the leaderboard entry
            entry_text = f"{i+1}. {score_data['username']}: {score_data['time']:.1f}s"
            entry_surface = leaderboard_font.render(entry_text, True, BLACK)
            entry_rect = entry_surface.get_rect(center=(WIDTH // 2, leaderboard_y + i * entry_surface.get_height()))
            screen.blit(entry_surface, entry_rect)

    pygame.display.flip()  # Update display
    clock.tick(30)  # Control the frame rate

pygame.quit()