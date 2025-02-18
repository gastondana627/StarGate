// Constants for grid size, stargate zone, and sounds
const GRID_SIZE = 8;
const STARGATE_ZONE = new Set(["6,6", "6,7", "7,6", "7,7"]);
let robotPosition = [0, 0];
let carryingRock = false;
let score = 0;
const moonrocks = new Set([
  "1,1", "2,3", "4,4", "5,5", "6,2"
]);

// Create grid
const grid = document.getElementById('grid');
for (let y = 0; y < GRID_SIZE; y++) {
  for (let x = 0; x < GRID_SIZE; x++) {
    const cell = document.createElement('div');
    cell.classList.add('grid-cell');
    cell.dataset.coords = `${x},${y}`;
    grid.appendChild(cell);
  }
}

// Sound effects
const beepSound = new Audio('/a_robot_beeping.wav');
const beepSound2 = new Audio('/a_robot_beeping-2.wav');

// Game update function
function updateGameState() {
  const robotCell = document.querySelector(`[data-coords="${robotPosition.join(',')}"]`);
  const positionDisplay = document.getElementById('position');
  const scoreDisplay = document.getElementById('score');
  const messageDisplay = document.getElementById('message');
  
  positionDisplay.textContent = `Position: (${robotPosition.join(',')})`;
  scoreDisplay.textContent = `Score: ${score}`;
  
  // Show robot image
  const robotImg = document.createElement('img');
  robotImg.src = '/robot.png';
  robotImg.style.width = '50px';
  robotImg.style.height = '50px';
  robotCell.appendChild(robotImg);

  // Check if there's a moonrock at the current position
  if (moonrocks.has(robotPosition.join(','))) {
    messageDisplay.textContent = 'You found a moonrock!';
  } else {
    messageDisplay.textContent = '';
  }
}

// Movement function
function move(direction) {
  let newPosition = [...robotPosition];

  if (direction === 'up' && newPosition[1] > 0) newPosition[1]--;
  if (direction === 'down' && newPosition[1] < GRID_SIZE - 1) newPosition[1]++;
  if (direction === 'left' && newPosition[0] > 0) newPosition[0]--;
  if (direction === 'right' && newPosition[0] < GRID_SIZE - 1) newPosition[0]++;

  robotPosition = newPosition;
  updateGameState();
}

// Pick up moonrock
function pickup() {
  if (carryingRock) {
    alert("You're already carrying a moonrock!");
    return;
  }
  
  const positionStr = robotPosition.join(',');
  if (moonrocks.has(positionStr)) {
    moonrocks.delete(positionStr);
    carryingRock = true;
    beepSound.play();
    alert("Moonrock picked up!");
  } else {
    alert("No moonrock at this position.");
  }
}

// Drop moonrock at Stargate
function drop() {
  if (!carryingRock) {
    alert("You're not carrying any moonrock.");
    return;
  }
  
  const positionStr = robotPosition.join(',');
  if (STARGATE_ZONE.has(positionStr)) {
    carryingRock = false;
    score++;
    beepSound2.play();
    alert("Moonrock delivered to Stargate! Score: " + score);
  } else {
    alert("You need to be at the Stargate to drop the moonrock.");
  }
}

// Initial game setup
updateGameState();
