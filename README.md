# ExtendedTris
This is a extended version of tic tac toe


## Game
The game is like tic tac toe, but the goal is to win with the big squares. 
Each big square is a tic tac toe game, that can be won with the normal rules.
The placement of a sign determines in which subsequent big square the game is played.

![Image of game](http://i.imgur.com/mYLORGf.png)

## Usage

For Windows users there's an executable in the `ExtendedTris.zip` compressed folder

For Unix and Mac sadly I don't have executables but the game can be run from `python3.4`.
Clone the repository and start the script `main.py`

## Libraries and dependencies
- The `tkinter` library for the graphics
- `random` for the AI, because who doesnt like a casual opponent
- `sys` and `os` are there because of pyinstaller, yet could be deleted
