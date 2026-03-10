# NHL Live Scorebug for OBS

A Python automation script that pulls live NHL game data from the NHL public API and generates a formatted text file used to power a scoreboard overlay in streaming software.

The script was built to support live watch streams for the Buffalo Sabres, automatically updating game information such as the clock, shots on goal, and current period every 15 seconds.

The output file is designed to be read by a text source in OBS Studio, enabling a fully automated live scorebug for streams covering games from the National Hockey League.

---

## Features

- Pulls live game data from the NHL public API  
- Automatically detects the relevant Sabres game (live, upcoming, or most recent)  
- Displays:
  - Game clock
  - Shots on goal (home and away)
  - Current period or game status  
- Handles multiple game states:
  - LIVE
  - Intermission
  - Pre-game
  - Final  
- Updates every 15 seconds  
- Writes formatted output to a text file for OBS integration  

---

## Example Output

Example contents of `game_info.txt`:
12:44
21
18
2ND

Output format:
Clock
Home Shots
Away Shots
Period


Example interpretations:

| Output | Meaning |
|------|------|
| `12:44` | Time remaining in the period |
| `21` | Home team shots on goal |
| `18` | Away team shots on goal |
| `2ND` | Current period |

Other possible outputs:
INT
24
19
2ND

32
28
FINAL

---

## How It Works

1. The script calls the NHL scoreboard API.
2. It determines which Sabres game is most relevant:
   - Currently live game
   - Game scheduled for today
   - Next upcoming game
   - Most recently completed game
3. It retrieves the detailed boxscore for that game.
4. Game data is parsed and formatted into a fixed-width layout.
5. The formatted data is written to `game_info.txt`.
6. OBS reads this file and displays the values in a scoreboard overlay.

---

## Installation

Clone the repository:


git clone https://github.com/yourusername/nhl-live-scorebug-overlay.git

cd nhl-live-scorebug-overlay


Install dependencies:


pip install requests


---

## Usage

Run the script:


python scorebug.py


The script will begin pulling game data and updating the output file every 15 seconds.

To stop the script:


CTRL + C
