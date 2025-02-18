// Show the game screen and hide the intro screen
document.getElementById('start-btn').addEventListener('click', function() {
    // Hide the intro screen
    document.getElementById('intro-screen').style.display = 'none';
  
    // Show the game screen
    document.getElementById('game-screen').style.display = 'block';
  });
  
  // Add movement functionality
  let robotPosition = { x: 0, y: 0 }; // Initial robot position
  let carryingRock = false;
  const stargateZone = [
    { x: 6, y: 6 },
    { x: 6, y: 7 },
    { x: 7, y: 6 },
    { x: 7, y: 7 }
  ];
  
  const moonrocks = [
    { x: 2, y: 3 },
    { x: 4, y: 5 },
    { x: 6, y: 2 }
  ];
  
  function updateRobotPosition() {
    const robotElement = document.getElementById('robot');
    robotElement.style.transform = `translate(${robotPosition.x * 100}px, ${robotPosition.y * 100}px)`;
  }
  
  function moveRobot(dx, dy) {
    robotPosition.x += dx;
    robotPosition.y += dy;
    updateRobotPosition();
  }
  
  // Move the robot when arrow keys are pressed
  document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowUp') moveRobot(0, -1);
    if (event.key === 'ArrowDown') moveRobot(0, 1);
    if (event.key === 'ArrowLeft') moveRobot(-1, 0);
    if (event.key === 'ArrowRight') moveRobot(1, 0);
  });
  
  // Pick up a moonrock if the robot is on one
  function pickUpRock() {
    const currentRock = moonrocks.find(r => r.x === robotPosition.x && r.y === robotPosition.y);
    if (currentRock && !carryingRock) {
      carryingRock = true;
      moonrocks.splice(moonrocks.indexOf(currentRock), 1); // Remove rock from grid
      alert('Moonrock picked up!');
    } else if (carryingRock) {
      alert('You are already carrying a moonrock!');
    } else {
      alert('No moonrock at this position!');
    }
  }
  
  // Drop the moonrock at the Stargate
  function dropRock() {
    const atStargate = stargateZone.some(r => r.x === robotPosition.x && r.y === robotPosition.y);
    if (atStargate && carryingRock) {
      carryingRock = false;
      alert('Moonrock delivered to Stargate!');
    } else if (!atStargate) {
      alert('You must drop the rock at the Stargate!');
    } else {
      alert('You are not carrying a moonrock!');
    }
  }
  
  // Listen for 'p' to pick up rock and 'd' to drop it
  document.addEventListener('keydown', function(event) {
    if (event.key === 'p') pickUpRock();
    if (event.key === 'd') dropRock();
  });
  
  
