document.addEventListener('DOMContentLoaded', function () {
    let username = "";
    let gameStarted = false;
    let pollInterval = null;

    // DOM Elements
    const introScreen = document.getElementById("intro-screen");
    const gameScreen = document.getElementById("game-screen");
    const usernameInput = document.getElementById("usernameInput");
    const scoreDisplay = document.getElementById("score");
    const timerDisplay = document.getElementById("timer");
    const moonrocksContainer = document.getElementById("moonrocks-container");
    const robotElement = document.getElementById("robot");
    const gameOverOverlay = document.getElementById("game-over-overlay");
    const finalScoreDisplay = document.getElementById("final-score");
    const finalResultDisplay = document.getElementById("final-result");

    // Audio
    const pickupSound = new Audio("assets/a_robot_beeping.wav");
    const dropSound = new Audio("assets/a_robot_beeping-2.wav");

    const CELL_SIZE = 80;

    function updateUI(data) {
        // Robot
        const pos = data.robot_position;
        if (robotElement) {
            robotElement.style.transform = `translate(${pos[0] * CELL_SIZE}px, ${pos[1] * CELL_SIZE}px)`;
            // Carrying indicator
            robotElement.style.filter = data.carrying_rock ? "drop-shadow(0 0 5px gold)" : "none";
        }

        // Moonrocks
        if (moonrocksContainer) {
            moonrocksContainer.innerHTML = "";
            data.moonrocks.forEach((rock) => {
                const rockDiv = document.createElement("div");
                rockDiv.classList.add("moonrock");
                rockDiv.style.transform = `translate(${rock[0] * CELL_SIZE}px, ${rock[1] * CELL_SIZE}px)`;
                moonrocksContainer.appendChild(rockDiv);
            });
        }

        // Stats
        if (scoreDisplay) scoreDisplay.innerText = `Score: ${data.score}`;
        if (timerDisplay) timerDisplay.innerText = `Time: ${data.remaining_time}s`;

        // Game Over
        if (data.game_over && gameStarted) {
            gameStarted = false;
            if (pollInterval) clearInterval(pollInterval);
            if (finalScoreDisplay) finalScoreDisplay.innerText = data.score;
            if (finalResultDisplay) finalResultDisplay.innerText = data.game_won ? "VICTORY!" : "GAME OVER";
            if (gameOverOverlay) gameOverOverlay.classList.remove("hidden");
        }
    }

    function fetchGameState() {
        fetch("/api/state")
            .then(res => res.json())
            .then(updateUI)
            .catch(err => console.error("Poll error:", err));
    }

    function startGame() {
        username = usernameInput ? usernameInput.value.trim() : "";
        if (!username && usernameInput) {
            alert("Please enter a username!");
            return;
        }

        fetch("/api/reset")
            .then(() => {
                if (introScreen) introScreen.style.display = "none";
                if (gameScreen) gameScreen.style.display = "flex";
                if (gameOverOverlay) gameOverOverlay.classList.add("hidden");
                gameStarted = true;
                fetchGameState();
                if (pollInterval) clearInterval(pollInterval);
                pollInterval = setInterval(fetchGameState, 500);
            });
    }

    const startBtn = document.getElementById("start-btn");
    if (startBtn) startBtn.addEventListener("click", startGame);

    const restartBtn = document.getElementById("restart-btn");
    if (restartBtn) restartBtn.addEventListener("click", () => {
        if (gameOverOverlay) gameOverOverlay.classList.add("hidden");
        startGame();
    });

    function move(dx, dy) {
        if (!gameStarted) return;
        fetch(`/api/move?dx=${dx}&dy=${dy}`)
            .then(res => res.json())
            .then(updateUI)
            .catch(err => console.error("Move error:", err));
    }

    function pickup() {
        if (!gameStarted) return;
        fetch("/api/pickup")
            .then(res => res.json())
            .then(data => {
                if (data.result.status === "success") pickupSound.play();
                updateUI(data.gameState);
            })
            .catch(err => console.error("Pickup error:", err));
    }

    function drop() {
        if (!gameStarted) return;
        fetch("/api/drop")
            .then(res => res.json())
            .then(data => {
                if (data.result.status === "success") dropSound.play();
                updateUI(data.gameState);
            })
            .catch(err => console.error("Drop error:", err));
    }

    document.addEventListener("keydown", (e) => {
        if (!gameStarted) return;
        const key = e.key.toLowerCase();
        if (key === "arrowup" || key === "w") move(0, -1);
        else if (key === "arrowdown" || key === "s") move(0, 1);
        else if (key === "arrowleft" || key === "a") move(-1, 0);
        else if (key === "arrowright" || key === "d") move(1, 0);
        else if (e.key === " ") pickup();
        else if (e.key === "Enter") drop();
    });
});
