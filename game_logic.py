## GasMan
## February 10, 2025

import random
import time
from typing import List, Tuple, Dict, Set, Union
from config import GRID_SIZE, STARGATE_ZONE, TOTAL_ROCKS, GAME_DURATION

class GameState:
    """Encapsulates all game mechanics and state."""

    def __init__(self):
        self.robot_position: List[int] = [0, 0]
        self.carrying_rock: bool = False
        self.score: int = 0
        self.moonrocks: Set[Tuple[int, int]] = set()
        self.start_time: float = 0
        self.game_won: bool = False
        self.game_over: bool = False
        self.reset()

    def reset(self) -> None:
        """Reset the game state to its initial conditions."""
        self.robot_position = [0, 0]
        self.carrying_rock = False
        self.score = 0
        self.game_won = False
        self.game_over = False
        self.moonrocks = set()
        self.start_time = time.time()

        while len(self.moonrocks) < TOTAL_ROCKS:
            new_rock = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if new_rock not in STARGATE_ZONE and new_rock != (0, 0):
                self.moonrocks.add(new_rock)

    def move_robot(self, dx: int, dy: int) -> None:
        """Update robot position within grid bounds."""
        if self.is_time_up():
            self.game_over = True
            return

        new_x = self.robot_position[0] + dx
        new_y = self.robot_position[1] + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.robot_position = [new_x, new_y]

    def pick_up_rock(self) -> Dict[str, str]:
        """Attempt to pick up a moonrock at current position."""
        if self.is_time_up():
            self.game_over = True
            return {"status": "error", "message": "Time's up!"}

        if self.carrying_rock:
            return {"status": "error", "message": "You can only carry one rock at a time!"}

        pos_tuple = tuple(self.robot_position)
        if pos_tuple in self.moonrocks:
            self.moonrocks.remove(pos_tuple)
            self.carrying_rock = True
            return {"status": "success", "message": f"Moonrock picked up at {self.robot_position}"}

        return {"status": "error", "message": "No moonrock at this position!"}

    def drop_rock(self) -> Dict[str, str]:
        """Attempt to drop the moonrock at the Stargate zone."""
        if self.is_time_up():
            self.game_over = True
            return {"status": "error", "message": "Time's up!"}

        if not self.carrying_rock:
            return {"status": "error", "message": "No rock to drop!"}

        if tuple(self.robot_position) in STARGATE_ZONE:
            self.carrying_rock = False
            self.score += 1
            if self.score == TOTAL_ROCKS:
                self.game_won = True
                self.game_over = True
            return {"status": "success", "message": f"Moonrock delivered! Score: {self.score}"}

        return {"status": "error", "message": "You must drop the rock at the Stargate!"}

    def is_time_up(self) -> bool:
        """Check if the game timer has expired."""
        return (time.time() - self.start_time) > GAME_DURATION

    def get_remaining_time(self) -> int:
        """Calculate remaining time in seconds."""
        elapsed = time.time() - self.start_time
        remaining = max(0, int(GAME_DURATION - elapsed))
        return remaining

    def to_dict(self) -> Dict[str, Union[List[int], List[Tuple[int, int]], int, bool]]:
        """Return a dictionary representation of current game state."""
        return {
            "robot_position": self.robot_position,
            "moonrocks": list(self.moonrocks),
            "score": self.score,
            "carrying_rock": self.carrying_rock,
            "remaining_time": self.get_remaining_time(),
            "game_won": self.game_won,
            "game_over": self.game_over or self.is_time_up()
        }

# Singleton instance for shared state across modules
_shared_state = GameState()

def move_robot(dx: int, dy: int) -> None:
    _shared_state.move_robot(dx, dy)

def pick_up_rock() -> Dict[str, str]:
    return _shared_state.pick_up_rock()

def drop_rock() -> Dict[str, str]:
    return _shared_state.drop_rock()

def get_game_state() -> Dict[str, Union[List[int], List[Tuple[int, int]], int, bool]]:
    return _shared_state.to_dict()

def reset_game() -> None:
    _shared_state.reset()
