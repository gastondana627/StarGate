async function fetchGameState() {
    const response = await fetch('/api/state');
    const gameState = await response.json();
    document.getElementById('game-status').innerText = `Game Status: ${gameState.carrying_rock ? "Carrying Rock" : "Idle"}`;
    document.getElementById('score').innerText = `Score: ${gameState.score}`;
    document.getElementById('game-state').innerText = `Robot Position: ${gameState.robot_position}, Moonrocks: ${JSON.stringify(gameState.moonrocks)}`;
}

async function moveRobot(dx, dy) {
    await fetch(`/api/move?dx=${dx}&dy=${dy}`);
    fetchGameState();
}

async function pickUpRock() {
    const response = await fetch('/api/pickup');
    const result = await response.json();
    alert(result.message);
    fetchGameState();
}

async function dropRock() {
    const response = await fetch('/api/drop');
    const result = await response.json();
    alert(result.message);
    fetchGameState();
}

fetchGameState();
