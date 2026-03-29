# StarGate Game

A simple 2D game where you control a robot to collect moonrocks and deliver them to a Stargate. This project features both a web interface and a Pygame desktop interface, sharing the same core game logic.

## Project Structure

- `api/`: Vercel serverless functions for the web game state and actions.
- `assets/`: Unified directory for images, sounds, and fonts.
- `game_logic.py`: Core game mechanics shared between web and desktop versions.
- `graphics.py`: Pygame-based desktop implementation.
- `index.html`, `script.js`, `styles.css`: Frontend for the web-based version.
- `leaderboard.json`: Persistent storage for high scores.

## Requirements

- Python 3.8+
- Pygame (for the desktop version)
- A modern web browser (for the web version)

## How to Run (Web)

The web version is designed to be deployed as a Vercel project. To run it locally:

1. Install the Vercel CLI: `npm i -g vercel`
2. Run `vercel dev` in the root directory.
3. Open `http://localhost:3000` in your browser.

## How to Run (Pygame)

1. Install dependencies: `pip install -r requirements.txt`
2. Run the game: `python graphics.py`

## Controls

- **Movement:** Arrow keys or WASD
- **Pick up Moonrock:** Spacebar
- **Drop Moonrock at Stargate:** Enter
