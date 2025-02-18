## GasMan
## February 9, 2025

import json
import random

# Grid dimensions
GRID_SIZE = 8

# Initialize robot position
robot_position = (0, 0)
carrying_rock = False
score = 0

# Define Stargate Zone (2x2)
STARGATE_ZONE = {(6, 6), (6, 7), (7, 6), (7, 7)}

# Score file for persistence
SCORE_FILE = "score.json"

def save_score():
    """Save the score to a file."""
    with open(SCORE_FILE, "w") as f:
        json.dump({"high_score": score}, f)

def load_score():
    """Load the score from a file."""
    global score
    try:
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
            score = data.get("high_score", 0)
    except FileNotFoundError:
        score = 0  # Default score if file not found

# Load score when game starts
load_score()

# Generate random moonrock positions ensuring they don't overlap with the Stargate
moonrocks = set()
while len(moonrocks) < 5:
    new_rock = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    if new_rock not in STARGATE_ZONE:  # Prevent rocks from spawning inside the Stargate
        moonrocks.add(new_rock)

def move_robot(dx, dy):
    """Move the robot within the grid."""
    global robot_position

    # Calculate the potential new position
    new_x = robot_position[0] + dx
    new_y = robot_position[1] + dy

    # Check if the new position is within the grid bounds
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        robot_position = (new_x, new_y)

def pick_up_rock():
    """Pick up a moonrock if the robot is on one."""
    global carrying_rock, moonrocks

    if carrying_rock:
        return {"status": "error", "message": "You can only carry one rock at a time!"}

    if robot_position in moonrocks:
        moonrocks.remove(robot_position)  # Remove rock from grid
        carrying_rock = True
        return {"status": "success", "message": f"Moonrock picked up at {robot_position}"}

    return {"status": "error", "message": "No moonrock at this position!"}

def drop_rock():
    """Drop a moonrock at the Stargate and update the score."""
    global carrying_rock, score

    if not carrying_rock:
        return {"status": "error", "message": "No rock to drop!"}

    if robot_position in STARGATE_ZONE:
        carrying_rock = False
        score += 1  # Increase score when rock is delivered
        save_score()  # Save updated score
        return {"status": "success", "message": f"Moonrock delivered to Stargate! Score: {score}"}

    return {"status": "error", "message": "You must drop the rock at the Stargate!"}

def get_game_state():
    """Returns the current game state for rendering purposes."""
    return {
        "robot_position": robot_position,
        "moonrocks": list(moonrocks),
        "score": score,
        "carrying_rock": carrying_rock
    }

def handler(request):
    """Handle API requests."""
    path = request.path.strip("/")
    
    if path == "move":
        dx, dy = int(request.args.get("dx", 0)), int(request.args.get("dy", 0))
        move_robot(dx, dy)
        return json.dumps(get_game_state())  # ✅ Return updated state
    
    elif path == "pickup":
        return json.dumps(pick_up_rock())
    
    elif path == "drop":
        return json.dumps(drop_rock())
    
    elif path == "state":
        return json.dumps(get_game_state())
    
    else:
        return json.dumps({"status": "error", "message": "Invalid API endpoint"})
