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

    function updateUI() {
        const robotElement = document.getElementById('robot');
        robotElement.style.transform = `translate(${robotPosition[0] * 100}px, ${robotPosition[1] * 100}px)`;

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
        fetch('/api/state')
            .then(response => response.json())
            .then(data => {
                robotPosition = data.robot_position;
                carryingRock = data.carrying_rock;
                moonrocks = data.moonrocks;
                score = data.score;
                updateUI();
            })
            .catch(error => console.error('Error fetching game state:', error));
    }

    function startGame() {
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

    function moveRobot(dx, dy) {
        fetch(`/api/move?dx=${dx}&dy=${dy}`)
            .then(response => response.json())
            .then(data => {
                robotPosition = data.robot_position;
                carryingRock = data.carrying_rock;
                moonrocks = data.moonrocks;
                score = data.score;
                updateUI();
            })
            .catch(error => console.error('Error moving robot:', error));
    }

    function pickUpRock() {
        fetch('/api/pickup')
            .then(response => response.json())
            .then(data => {
                if (data.result.status === 'success') {
                    carryingRock = true;
                    fetchGameState();
                } else {
                    alert(data.result.message);
                }
            })
            .catch(error => console.error('Error picking up rock:', error));
    }

    function dropRock() {
        fetch('/api/drop')
            .then(response => response.json())
            .then(data => {
                if (data.result.status === 'success') {
                    carryingRock = false;
                    fetchGameState();
                } else {
                    alert(data.result.message);
                }
            })
            .catch(error => console.error('Error dropping rock:', error));
    }

    document.getElementById('start-btn').addEventListener('click', startGame);

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
  
  
