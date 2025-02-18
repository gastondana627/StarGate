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
    # Use os.path.join to load images from the public/images folder
    robot_img = pygame.image.load(os.path.join("public", "images", "robot.png"))
    robot_img = pygame.transform.scale(robot_img, (CELL_SIZE, CELL_SIZE))

    moonrock_img = pygame.image.load(os.path.join("public", "images", "moonrock.png"))
    moonrock_img = pygame.transform.scale(moonrock_img, (CELL_SIZE, CELL_SIZE))

    stargate_img = pygame.image.load(os.path.join("public", "images", "stargate.png"))
    stargate_img = pygame.transform.scale(stargate_img, (CELL_SIZE * 2, CELL_SIZE * 2))

    # Load Stargate1.jpg for the intro screen
    stargate_intro_img = pygame.image.load(os.path.join("public", "images", "Stargate1.jpg"))
    stargate_intro_img = pygame.transform.scale(stargate_intro_img, (WIDTH, HEIGHT))  # Adjust as needed
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

    # --- DRAWING
    screen.fill(WHITE)

    # Display the intro screen if needed
    if not username_entered:
        screen.blit(stargate_intro_img, (0, 0))
        draw_text_with_wrapping(screen, "Enter Your Username:", font, BLACK, pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 60, 300, 50))
        draw_text_with_wrapping(screen, username, font, BLACK, pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50))

    # Render the game state if the game has started
    elif game_started:
        # Draw the robot
        robot_x, robot_y = robot_position
        screen.blit(robot_img, (robot_x * CELL_SIZE, robot_y * CELL_SIZE))

        # Draw the moonrocks
        for rock_x, rock_y in moonrocks:
            screen.blit(moonrock_img, (rock_x * CELL_SIZE, rock_y * CELL_SIZE))

        # Draw the Stargate
        screen.blit(stargate_img, ((GRID_SIZE - 2) * CELL_SIZE, (GRID_SIZE - 2) * CELL_SIZE))

        # Display the score
        score_text = font.render(f"Score: {score}/{TOTAL_ROCKS}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Display the timer
        if game_started and not game_won:
            elapsed_time = int(time.time() - start_time)
            timer_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
            screen.blit(timer_text, (WIDTH - 150, 10))

        # Display win message if the game is won
        if game_won:
            total_time = int(end_time - start_time)
            win_message = large_font.render(f"Congrats {username}!", True, GOLD)
            screen.blit(win_message, (WIDTH // 2 - win_message.get_width() // 2, HEIGHT // 2 - 100))

            time_message = font.render(f"Time: {total_time}s", True, GOLD)
            screen.blit(time_message, (WIDTH // 2 - time_message.get_width() // 2, HEIGHT // 2))

            leaderboard_button = font.render("Press ENTER to view Leaderboard", True, BLACK)
            screen.blit(leaderboard_button, (WIDTH // 2 - leaderboard_button.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
