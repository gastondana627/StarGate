import unittest
from game_logic import GameState, STARGATE_ZONE, TOTAL_ROCKS
import time

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game = GameState()
        self.game.reset()

    def test_initial_state(self):
        self.assertEqual(self.game.robot_position, [0, 0])
        self.assertFalse(self.game.carrying_rock)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.moonrocks), TOTAL_ROCKS)

    def test_movement(self):
        self.game.move_robot(1, 0)
        self.assertEqual(self.game.robot_position, [1, 0])
        self.game.move_robot(0, 1)
        self.assertEqual(self.game.robot_position, [1, 1])
        # Test bounds
        self.game.robot_position = [0, 0]
        self.game.move_robot(-1, 0)
        self.assertEqual(self.game.robot_position, [0, 0])

    def test_pickup_and_drop(self):
        # Find a rock
        rock_pos = list(self.game.moonrocks)[0]
        self.game.robot_position = list(rock_pos)

        # Pick up
        res = self.game.pick_up_rock()
        self.assertEqual(res["status"], "success")
        self.assertTrue(self.game.carrying_rock)
        self.assertNotIn(tuple(self.game.robot_position), self.game.moonrocks)

        # Try to drop outside stargate
        self.game.robot_position = [0, 0]
        res = self.game.drop_rock()
        self.assertEqual(res["status"], "error")
        self.assertTrue(self.game.carrying_rock)

        # Drop at stargate
        stargate_pos = list(STARGATE_ZONE)[0]
        self.game.robot_position = list(stargate_pos)
        res = self.game.drop_rock()
        self.assertEqual(res["status"], "success")
        self.assertFalse(self.game.carrying_rock)
        self.assertEqual(self.game.score, 1)

    def test_timer(self):
        self.game.start_time = time.time() - 61 # Force time up
        self.assertTrue(self.game.is_time_up())

        self.game.move_robot(1, 0)
        self.assertTrue(self.game.game_over)

if __name__ == "__main__":
    unittest.main()
