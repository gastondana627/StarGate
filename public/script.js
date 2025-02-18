async function fetchGameState() {
    // Fetch current game state from backend API
    const response = await fetch('/api/state');
    const gameState = await response.json();
    
    // Update UI with the game status
    document.getElementById('game-status').innerText = `Game Status: ${gameState.carrying_rock ? "Carrying Rock" : "Idle"}`;
    document.getElementById('score').innerText = `Score: ${gameState.score}`;
    document.getElementById('game-state').innerText = `Robot Position: ${gameState.robot_position}, Moonrocks: ${JSON.stringify(gameState.moonrocks)}`;
}

// Function to move the robot on the grid
async function moveRobot(dx, dy) {
    // Call API to move the robot
    await fetch(`/api/move?dx=${dx}&dy=${dy}`);
    fetchGameState(); // Update the game state
}

// Function to pick up a moonrock
async function pickUpRock() {
    const response = await fetch('/api/pickup');
    const result = await response.json();
    alert(result.message); // Show a message for pickup action
    fetchGameState(); // Update the game state after the pickup
}

// Function to drop a moonrock at the Stargate
async function dropRock() {
    const response = await fetch('/api/drop');
    const result = await response.json();
    alert(result.message); // Show a message for drop action
    fetchGameState(); // Update the game state after the drop
}

// Event listeners for buttons to trigger actions
document.getElementById('move-up').addEventListener('click', () => moveRobot(0, -1));
document.getElementById('move-down').addEventListener('click', () => moveRobot(0, 1));
document.getElementById('move-left').addEventListener('click', () => moveRobot(-1, 0));
document.getElementById('move-right').addEventListener('click', () => moveRobot(1, 0));
document.getElementById('pickup').addEventListener('click', pickUpRock);
document.getElementById('drop').addEventListener('click', dropRock);

// Initial fetch of game state on page load
fetchGameState();

