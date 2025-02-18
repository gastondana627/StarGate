document.addEventListener('DOMContentLoaded', function() {
    let username = "";
    let robotPosition = [0, 0];
    let carryingRock = false;
    let moonrocks = [];
    let score = 0;
    let gameStarted = false;

    const introScreen = document.getElementById('intro-screen');
    const gameScreen = document.getElementById('game-screen');
    const leaderboardScreen = document.getElementById('leaderboard-screen');
    const usernameInput = document.getElementById('usernameInput');
    const scoreDisplay = document.getElementById('score');
    const moonrocksContainer = document.getElementById('moonrocks-container');

    // Ensure elements exist before using them
    if (!introScreen || !gameScreen || !leaderboardScreen || !usernameInput || !scoreDisplay || !moonrocksContainer) {
        console.error("One or more required elements not found.  Check your HTML.");
        return; // Stop execution if elements are missing
    }

    function updateUI() {
        const robotElement = document.getElementById('robot');
        if(robotElement) {
            robotElement.style.transform = `translate(${robotPosition[0] * 100}px, ${robotPosition[1] * 100}px)`;
        }

        moonrocksContainer.innerHTML = '';
        moonrocks.forEach(rock => {
            const rockElement = document.createElement('div');
            rockElement.classList.add('moonrock');
            rockElement.style.transform = `translate(${rock[0] * 100}px, ${rock[1] * 100}px)`;
            moonrocksContainer.appendChild(rockElement);
        });

        scoreDisplay.innerText = `Score: ${score}`;
    }
    function fetchLeaderboard() {
        fetch('/leaderboard.json')  // Fetch leaderboard.json directly
            .then(response => response.json())
            .then(leaderboardData => {
                const leaderboardList = document.getElementById('leaderboard-list');
                leaderboardList.innerHTML = ''; // Clear existing entries

                leaderboardData.forEach(entry => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${entry.username}: ${entry.time}s`;
                    leaderboardList.appendChild(listItem);
                });

                gameScreen.style.display = 'none';
                leaderboardScreen.style.display = 'flex';
            })
            .catch(error => console.error('Error fetching leaderboard:', error));
    }

    function fetchGameState() {
        console.log("fetchGameState function called!");
        fetch('/api/state')
            .then(response => {
                console.log("fetchGameState: Response received", response);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);  // Handle non-200 responses
                }
                return response.json();
            })
            .then(data => {
                console.log("fetchGameState: Data received", data);
                robotPosition = data.robot_position;
                carryingRock = data.carrying_rock;
                moonrocks = data.moonrocks;
                score = data.score;
                updateUI();
            })
            .catch(error => console.error('Error fetching game state:', error));
    }

    function startGame() {
        console.log("startGame function called!"); // Add this line
        username = usernameInput.value.trim();
        if (username === "") {
            alert("Please enter a username!");
            return;
        }
        introScreen.style.display = 'none';
        gameScreen.style.display = 'flex';
        gameStarted = true;
        fetchGameState();
    }

    const startButton = document.getElementById('start-btn'); // Get button here
    if (startButton) {  // Check if the element exists
         console.log("Start button exists", startButton)
        startButton.addEventListener('click', startGame); // Attach listener
    } else {
        console.error("Start button not found!");  // Log an error if button isn't found
    }


    document.addEventListener('keydown', function(event) {
        if (!gameStarted) return;

        switch (event.key) {
            case 'ArrowUp': moveRobot(0, -1); break;
            case 'ArrowDown': moveRobot(0, 1); break;
            case 'ArrowLeft': moveRobot(-1, 0); break;
            case 'ArrowRight': moveRobot(1, 0); break;
            case 'p': pickUpRock(); break;
            case 'd': dropRock(); break;
        }
    });
    document.getElementById('back-to-intro').addEventListener('click', function() {
        leaderboardScreen.style.display = 'none';
        introScreen.style.display = 'flex';
    });
});
  
  
