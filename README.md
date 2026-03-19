# Rock Paper Scissors — Pygame

A feature-rich Rock Paper Scissors desktop game built with Python and Pygame. Play against an AI bot with adaptive difficulty powered by machine learning, or challenge a friend online in real-time multiplayer.

## Features

- **Single Player** — Play against a bot with three difficulty levels
- **Multiplayer** — Online head-to-head play via a room-based networking system (create or join a room)
- **AI Bot (Machine Learning)** — The hard difficulty bot learns from your move history using Decision Tree and Random Forest classifiers
- **Animated UI** — Pygame-powered animations for rock, paper, and scissors selections
- **Sound Effects** — Win, lose, and button click audio feedback with background music
- **Settings** — Adjustable screen size (small, medium, large, fullscreen) and difficulty selection
- **Internet Detection** — Automatically falls back to offline mode if no network is available

## Requirements

- Python 3.x
- `pygame`
- `requests`
- `pandas`
- `scikit-learn`

Install all dependencies at once:

```bash
pip install pygame requests pandas scikit-learn
```

## Download & Installation

### Option 1: Clone with Git

```bash
git clone https://github.com/daoduylam2008/RockPaperScissorPygame.git
cd RockPaperScissorPygame
```

### Option 2: Download ZIP

1. Go to the [repository page](https://github.com/daoduylam2008/RockPaperScissorPygame).
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the ZIP to a folder of your choice.

## Running the Game

```bash
python main.py
```

## How to Play

### Single Player
1. Enter your name in the input box on the main menu.
2. Click **Single Player**.
3. Choose **Rock**, **Paper**, or **Scissors** — the bot will respond instantly.
4. The result (Win / Lose / Draw) is displayed on screen.

### Multiplayer
1. Make sure you have an active internet connection.
2. Enter your name on the main menu.
3. Click **MultiPlayer**.
4. **Create Room** to host a game and share your Room ID with a friend, or **Join Room** by entering their Room ID.
5. Both players choose their move — the result is shown in real time.

### Difficulty Levels (Single Player)

| Level | Behaviour |
|-------|-----------|
| Easy | Completely random bot moves |
| Medium | Bot reacts based on your last move and result |
| Hard | Bot trains a ML model (Decision Tree + Random Forest) on your full move history to predict and counter your next choice |

### Settings
Access **Settings** from the main menu to:
- Resize the window (Small / Medium / Large / Fullscreen) — requires a restart to apply
- Change the bot difficulty

## Project Structure

```
RockPaperScissorPygame/
├── main.py                 # Main entry point and game loop
├── MachineLearning.py      # AI bot logic (Easy / Medium / Hard)
├── networking.py           # Online multiplayer (connected mode)
├── non_network.py          # Offline fallback networking stub
├── uix/                    # Custom UI widget library (buttons, text, animations)
├── data/
│   ├── history.txt         # Player move history (used by ML bot)
│   ├── history1.txt        # Game outcome history (used by ML bot)
│   ├── difficulty.txt      # Stored difficulty setting
│   ├── size.txt            # Stored window size setting
│   ├── soundeffect/        # Audio files (win, lose, button, background)
│   ├── *_animation/        # Frame-by-frame animation assets
│   ├── menu.png            # Menu background image
│   └── background.png      # Game background image
├── MachineLearning.ipynb   # Jupyter notebook for ML experimentation
└── scripts/                # Utility scripts
```

## Authors

- **Dao Duy Lam** — daoduylam2020@gmail.com
- **Pham Minh Khoi** — phamminhkhoi10122008@gmail.com
- **Le Cong Tien** — ltien9505@gmail.com
