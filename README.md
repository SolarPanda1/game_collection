# game_collection
A collection of games and programs that I have coded in python. Will be updated in the future    
## REQUIREMENTS
1. Python 3.6 or 3.7
1. numpy == 1.18.2
1. pygame == 1.9.6
## Installation
Ensure that you have either python 3.6 or python 3.7, pip and virtualenv installed.  
Create a new directory. On windows, open up the comamnd prompt.  
On CMD, change working directory to newdir  
```
cd path\to\new\dir
```
Create new virtual environment
```
python -m virtualenv nameofvirtualenv
```
Activate virtual environment.
```
.\nameofvirutalenv\Scripts\activate.bat
```
You will know it is activated if you see something like this
```
(nameofvirtualenv)c:\path\to\working\dir>
```
Install pygame and numpy(optional) using pip. It will install into your venv folder
```
pip install pygame==1.9.6
pip install numpy==1.18.2
```
Download chess.py, game.py and other python scripts. Run the program
```
python chess.py
```
Enjoy!
## Chess
![Chess](/README_Images/chess1.png)  
A simple chess game. The game is played by 2 human players. For every move by a player, the game then checks if the other player is checkmated. Click on the piece that you want to move, then click on another sqaure to move the piece. Game will tell you if move is invalid.  
![Chess](/README_Images/chess2.png)  
Since there is no more valid move for Black, and the King is under check, White wins.  
Note: vectormanipulation.py can be used with numpy arrays
## 3d_cube
![3d Cube](/README_Images/3d_cube2.png)  
Press the arrow keys to rotate the cube in four directions.<br/><br/>
![3D Cube](/README_Images/3d_cube.png)<br/><br/>
The points on the cube are coordinates in the x,y,x plane. A line is drawn between the point on the cube and the Vanishing Point. The line would intersect with an infinite plane, representing the screen. The points of intersection are then drawn on the 2d screen.  
Note: The distance between the vanishing point and the screen can be adjusted by changing the value of the variable **vpDistance**. Angular velocity of the cube can be adjusted using the variable **angularVelocity**.  
##  Mandelbrot set
![MandelBrot](/README_Images/mandelbrot.png)  
The Mandelbrot set is the set of values c in the complex planes such that repeated iteration of the function f(x) = x^2 + c remain bounded. First value of x is 0.  
![Julia set](/README_Images/juliaset.png)  
The Julia Set consists of values such that an arbitrarily small perturbation can cause drastic changes in the sequence of iterated function values. https://en.wikipedia.org/wiki/Julia_set  
The julia set shown is the set of all points x such that repeated iteration of the function f(x) = x^2 + c remain bounded. For this case, c is the golden ratio.




