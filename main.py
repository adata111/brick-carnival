import colorama, sys, os, math, time, copy
from colorama import Fore, Back, Style
from headers import *
from paddle import *
from input import *
from board import *
from ball import *
import globalVar
from globalVar import TOP, BOTTOM, LIVES, SCORE, WIDTH, HT, obj_bricks, paddle
import globalFunc
from globalFunc import setBricks

fps = 25
t = 1/fps

blank_arr = []

for i in range(HT):
	blank_arr.append(' '*WIDTH + '\n')

board_arr = copy.deepcopy(blank_arr)
newBoard = Board(board_arr)
globalVar.paddle = Paddle(20, 1)
newBall = Ball(1, 1, 20)
setBricks()
# for obj in obj_bricks:
	
# 	print(obj.getx(),obj.gety())

while True:
	key = input_to()
	display_arr = copy.deepcopy(blank_arr)
	if(globalVar.LIVES<=0):
		print("GAME OVER")
		print("Score:",globalVar.SCORE)
		break
	print("\033[H\033[J", end="")

	if(key=='d'):
		if(newBall.is_moving()==0):
			newBall.move(1)
		globalVar.paddle.move(1)
	elif(key=="a"):
		if(newBall.is_moving()==0):
			newBall.move(-1)
		globalVar.paddle.move(-1)
	elif(key=="b" and newBall.is_moving()==0):
		newBall.set_moving()
		newBall.move(1)

	display_arr = newBoard.getArr(str(globalVar.SCORE), str(globalVar.LIVES), display_arr)
	display_arr = globalVar.paddle.getArr(Back.BLUE, ' ', display_arr)
	if(newBall.is_moving()):
		newBall.check_paddle_collision()
		newBall.check_brick_collision()
		newBall.move(1)
	display_arr = newBall.getArr(Fore.CYAN, '⚪', display_arr)
	k=0
	j=0
	for obj in globalVar.obj_bricks:
		display_arr = obj.getArr(' ',display_arr)
		

	display_arr = ''.join(display_arr)
	print(display_arr)
	
	time.sleep(t)


