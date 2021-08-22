## Brick Carnival
### *Basic simulator of the classic brick breaker game*

### Overview
This a terminal-based arcade game in Python3, inspired by the classic brick-breaker game. The player will be using a paddle with a bouncing ball to smash a
wall of bricks and make high scores! The objective of the game is to break all the bricks as fast as possible and beat the highest score! You lose a life when the ball touches the ground below the paddle. Different sounds are played when different events (like life lost, brick collision, wall collision, laser shoot, etc.) occur.

### To start the game
- Open the terminal in full screen
- `python3 main.py`

### Controls
- To move the paddle right or left use <kbd>D</kbd> or <kbd>A</kbd> respectively
- To release the ball from paddle, use <kbd>P</kbd>
- To shoot bullets, use <kbd>spacebar</kbd>
- To quit the game, press <kbd>Q</kbd>

### Details
- The direction of movement of the ball after collision with the paddle will depend on the distance from the center of the paddle and the collision point, i.e further the ball hits from the center, more the deflection 
- If the ball hits the  bottom wall(or the floor), it dies and a ball life is lost
- The player gets 5 ball lives after which game ends
- The bricks are of 3 strengths:
	* `RED` -> strength=3
	* `YELLOW` -> strength = 2
	* `GREEN` -> strength = 1
Hitting a RED brick will reduce strength to 2 and change its colour to YELLOW. Similarly on hitting a YELLOW brick, the strength reduces to 1 and brick colour changes to GREEN. On hitting a GREEN brick, the brick breaks. Thus RED bricks require 3 hits to get broken, YELLOW bricks require 2 and GREEN just 1. 
- There are unbreakable bricks that can't be broken by the ball(unless it's a thru-ball, we shall talk about power-ups later). These bricks are `WHITE`
- There are exploding bricks which on breaking with the ball would explode resulting in the destruction of all the bricks adjacent to it(diagonally, vertically and horizontally). These bricks are not found individually and are placed in linear group of size 6 and contact with either one of them would lead to a chain reaction among this group. These bricks are `MAGENTA` or `LIGHT MAGENTA`
- On breaking any breakable brick (exploding or the RED/YELLOW/GREEN ones), a power may randomly drop down. These power ups can be collected by the paddle when they collide with the paddle
- Rainbow bricks change colour in every frame until it hit by the ball

### Power-ups
All power-ups (except ball multiplier) are are present only for a fixed amount of time(10 seconds) and lost at loss of a life. Power ups are displayed as yellow coloured letters
The power ups have gravity effect and take the velocity of the ball when the ball hits the brick
1. Expand Paddle(E): Increases the size of the paddle by a certain amount (10 units). The size can't increase beyond 50 units
2. Shrink Paddle(S): Reduce the size of the paddle by a certain amount (10 units) but not completely.
3. Ball Multiplier(M): Each of the balls which are present will be further divided into two.
4. Fast Ball(F): Increases the speed of the ball.
5. Thru-ball(T): This enables the ball to destroy and go through any brick it touches, irrespective of the strength of the wall.(Even the unbreakable ones which you couldn’t previously destroy)
6. Paddle Grab(G):Allows the paddle to grab the ball on contact and relaunch the ball at will. The ball will follow the same expected trajectory after release, similar to the movement expected without the grab.
7. Paddle Shooter(B):Canons appear at the ends of the paddle and pressing spacebar lets you release lasers to destroy the bricks. The cooldown time between laser shoots is 1 second
8. Fireball (R): This amazing power up causes an effect similar to exploding bricks on hitting a brick. It can destroy unbreakable bricks too!

### Scores and time
Score and time are displayed on top of the screen throughout the game
 - On hitting a GREEN brick or on destroying any brick, you get 20 points
 - On hitting a RED brick, you get 10 points
 - On hitting a YELLOW brick, you get 15 points
 - On hitting UFO you get 10 points

### Levels
There are 3 levels in the game. 
Level 1:
<img src="/screenshots/level1.png">

Level 2: 
Rainbow bricks are introduced
<img src="/screenshots/level2.png">

Level 3:
The UFO is introduced. This level has no power ups.
<img src="/screenshots/level3.png">

### UFO Enemy
Cyan coloured brick that drops bombs(@) every 5 seconds. It also moves along with the paddle. The health of the UFO is 5 initially and the strength reduces by 1 everytime the ball hits the UFO. The bombs cause the paddle to lose a life. The UFO spawns a layer of GREEN bricks below it when its health becomes 4 and again when its health becomes 2

### Time attack
After 10 seconds in Level 1, 15 seconds in level 2 and 30 seconds in level 3, the brick layout moves down by a unit everytime the ball hits the paddle. 

## Code details
### Classes created

1. **Brick**
Has subclasses `Breakable` for creating RED, YELLOW and GREEN breakable bricks, `Rainbow` for rainbow bricks of level 2, `Exploding` for creating the exploding bricks, `UFO` for the UFO brick and `Defense` for UFO's defense wall bricks.
2. **Ball**
3. **PowerUp**
Has one sublass for each power up. Therefore there are 8 subclasses as follows: Paddle_shooter, Fire_ball, Expand_paddle, Shrink_paddle, Ball_multiplier, Fast_ball, Thru_ball and Paddle_grab
4. **Board**
5. **Paddle**
6. **Laser**


### OOPS concepts

#### Inheritance
Common attributes of the parent class inherited by the child classes. (Helps in avoiding redundant code)
Here, a base class `Brick` has been declared from which multiple subclasses(`Breakable`, `Rainbow`, `Exploding`, `UFO` and `Defense`) inherit properties
Also, a base class `PowerUp` has been declared from which multiple subclasses(`Paddle_shooter`, `Fire_ball`, `Expand_paddle`, `Shrink_paddle`, `Ball_multiplier`, `Fast_ball`, `Thru_ball` and `Paddle_grab`) inherit properties

#### Polymorphism
Utililizing the same function of a parent class for different functionalites of child classes
Ex: `deactivate_power_up()` function in parent class `PowerUp` has been over-ridden by function of the same name in the different subclasses of `PowerUp`

#### Encapsulation
It is the idea of wrapping data and the methods that work on data within one unit. Prevents accidental modification of data. Class and object based approach for all the functionality implemented. For eg, all the methods that can modify the properties of the paddle are inside the `Paddle` class.

#### Abstraction
Abstraction means hiding the complexity. Intuitive functions like move(), break_it(), kill_ball(), etc, used to hide inner details from the end user.
