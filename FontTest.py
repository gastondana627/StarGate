import pygame
import os

pygame.init()

# Configuration
WIDTH, HEIGHT = 600, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Font Test")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font Selection - set to absolute path
FONT_PATH = "/Users/gastondana/Desktop/2025 CodeSignal/Robotics Demo/Fourth Workflow GAIS/fonts/Phage Rough.otf"  #  or "Phage Regular.otf"
#FONT_PATH = "/Users/gastondana/Desktop/2025 CodeSignal/Robotics Demo/Fourth Workflow GAIS/fonts/Phage Regular.otf"

print(f"Attempting to load font from: {FONT_PATH}")

font = None  # Initialize font

try:
    font = pygame.font.Font(FONT_PATH, 36)
    print(f"Successfully loaded font from: {FONT_PATH}")

except FileNotFoundError:
    print(f"Error: Font file not found! Please ensure the font file exists at: {FONT_PATH}")

except pygame.error as e:
    print(f"Error loading font from '{FONT_PATH}': {e}")
    print(f"Pygame error: {e}")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    if font:
        text_surface = font.render("The quick brown fox...", True, WHITE)
        screen.blit(text_surface, (50, 50))
    else:
        default_font = pygame.font.Font(None, 36)
        text_surface = default_font.render("Font failed to load!", True, WHITE)
        screen.blit(text_surface, (50, 50))

    pygame.display.flip()

pygame.quit()