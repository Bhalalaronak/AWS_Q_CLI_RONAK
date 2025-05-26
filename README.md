# Snake and Ladder Game

A classic Snake and Ladder board game implemented with Python and Pygame.

![Snake and Ladder Game](https://github.com/username/snake-and-ladder/raw/main/screenshot.png)

## Features

- Interactive graphical user interface built with Pygame
- Support for 1-4 players
- Classic Snake and Ladder gameplay mechanics
- Customizable board with snakes and ladders
- Animated dice rolls
- Player tokens with different colors
- Turn-based gameplay with proper rules

## Game Rules

- Players take turns rolling a dice to move their token
- Players need to roll a 6 to enter the board
- Landing on a ladder bottom allows you to climb up to its top
- Landing on a snake head sends you down to its tail
- Rolling a 6 gives you an extra turn
- First player to reach position 100 wins the game

## Requirements

- Python 3.6+
- Pygame

## Installation

1. Clone this repository:
```
git clone https://github.com/username/snake-and-ladder.git
cd snake-and-ladder
```

2. Install the required dependencies:
```
pip install pygame
```

3. Run the game:
```
python simple_snake_ladder_gui.py
```

## How to Play

1. Start the game and select the number of players (1-4)
2. Click "Start Game" to begin
3. Click "Roll Dice" to roll the dice on your turn
4. Follow the game rules to move your token
5. First player to reach position 100 wins!

## Project Structure

- `simple_snake_ladder_gui.py`: Main game file with GUI implementation
- `snake_and_ladder.py`: Console-based version of the game
- `snake_and_ladder_gui.py`: Advanced GUI version with animations

## Customization

You can customize the game by modifying the following variables in the code:

- `BOARD_SIZE`: Change the size of the game board
- `GRID_SIZE`: Change the number of cells in the grid
- `PLAYER_COLORS`: Modify player token colors
- `snakes` and `ladders` dictionaries: Change the positions of snakes and ladders

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the classic Snake and Ladder board game
- Built with Pygame, a set of Python modules designed for writing video games
