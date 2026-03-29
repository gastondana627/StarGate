# Game Constants
GRID_SIZE = 8
CELL_SIZE = 80

# Stargate Zone (Top-left corner of 2x2 area)
STARGATE_X = 6
STARGATE_Y = 6
STARGATE_ZONE = {
    (STARGATE_X, STARGATE_Y),
    (STARGATE_X, STARGATE_Y + 1),
    (STARGATE_X + 1, STARGATE_Y),
    (STARGATE_X + 1, STARGATE_Y + 1)
}

TOTAL_ROCKS = 5
GAME_DURATION = 60  # seconds
