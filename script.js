document.addEventListener('DOMContentLoaded', function () {
    let username = "";
    let robotPosition = [0, 0];
    let carryingRock = false;
    let moonrocks = [];
    let score = 0;
    let gameStarted = false;
  
    // DOM Elements
    const introScreen = document.getElementById("intro-screen");
    const gameScreen = document.getElementById("game-screen");
    const leaderboardScreen = document.getElementById("leaderboard-screen");
    const usernameInput = document.getElementById("usernameInput");
    const scoreDisplay = document.getElementById("score");
    const moonrocksContainer = document.getElementById("moonrocks-container");
  
    // Create Audio objects (using assets folder)
    const pickupSound = new Audio("assets/a_robot_beeping.wav");
    const dropSound = new Audio("assets/a_robot_beeping-2.wav");
  
    // Update UI based on game state
    function updateUI() {
      const robotElement = document.getElementById("robot");
      if (robotElement) {
        robotElement.style.transform = `translate(${robotPosition[0] * 100}px, ${robotPosition[1] * 100}px)`;
      }
  
      // Render moonrocks
      moonrocksContainer.innerHTML = "";
      moonrocks.forEach((rock) => {
        const rockElement = document.createElement("div");
        rockElement.classList.add("moonrock");
        rockElement.style.transform = `translate(${rock[0] * 100}px, ${rock[1] * 100}px)`;
        moonrocksContainer.appendChild(rockElement);
      });
  
      scoreDisplay.innerText = `Score: ${score}`;
    }
  
    // Fetch the game state from the backend API
    function fetchGameState() {
      fetch("/api/state")
        .then((response) => response.json())
        .then((data) => {
          robotPosition = data.robot_position;
          carryingRock = data.carrying_rock;
          moonrocks = data.moonrocks;
          score = data.score;
          updateUI();
        })
        .catch((error) => console.error("Error fetching game state:", error));
    }
  
    // Start the game after username entry
    function startGame() {
      username = usernameInput.value.trim();
      if (username === "") {
        alert("Please enter a username!");
        return;
      }
      introScreen.style.display = "none";
      gameScreen.style.display = "flex";
      gameStarted = true;
      fetchGameState();
    }
  
    // Get the start button and attach event listener
    const startButton = document.getElementById("start-btn");
    if (startButton) {
      console.log("Start button exists", startButton);
      startButton.addEventListener("click", startGame);
    } else {
      console.error("Start button not found!");
    }
  
    // Move the robot via the API
    function moveRobot(dx, dy) {
      fetch(`/api/move?dx=${dx}&dy=${dy}`)
        .then((response) => response.json())
        .then((data) => {
          robotPosition = data.robot_position;
          updateUI();
        })
        .catch((error) => console.error("Error moving robot:", error));
    }
  
    // Keyboard event listener for game controls
    document.addEventListener("keydown", function (event) {
      if (!gameStarted) return;
  
      switch (event.key) {
        case "ArrowUp":
          moveRobot(0, -1);
          break;
        case "ArrowDown":
          moveRobot(0, 1);
          break;
        case "ArrowLeft":
          moveRobot(-1, 0);
          break;
        case "ArrowRight":
          moveRobot(1, 0);
          break;
        case " ":
          // Spacebar: Pick up rock
          fetch("/api/pickup")
            .then((response) => response.json())
            .then((data) => {
              if (data.result.status === "success") {
                carryingRock = true;
                pickupSound.play();
              }
              updateUI();
            })
            .catch((error) => console.error("Error picking up rock:", error));
          break;
        case "Enter":
          // Enter: Drop rock
          fetch("/api/drop")
            .then((response) => response.json())
            .then((data) => {
              if (data.result.status === "success") {
                carryingRock = false;
                // Optionally, update the score from data.gameState.score
                score = data.gameState.score;
                dropSound.play();
              }
              updateUI();
            })
            .catch((error) => console.error("Error dropping rock:", error));
          break;
      }
    });
  
    // (Optional) Leaderboard fetch function, if your game uses it
    function fetchLeaderboard() {
      fetch("/leaderboard.json")
        .then((response) => response.json())
        .then((data) => {
          const leaderboardList = document.getElementById("leaderboard-list");
          leaderboardList.innerHTML = "";
          data.forEach((entry) => {
            const listItem = document.createElement("li");
            listItem.textContent = `${entry.username}: ${entry.time}s`;
            leaderboardList.appendChild(listItem);
          });
          gameScreen.style.display = "none";
          leaderboardScreen.style.display = "flex";
        })
        .catch((error) => console.error("Error fetching leaderboard:", error));
    }
  
    document.getElementById("back-to-intro").addEventListener("click", function () {
      leaderboardScreen.style.display = "none";
      introScreen.style.display = "flex";
    });
  });
  
