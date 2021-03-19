import copy
from headers import *
from paddle import *
from input import *
from board import *
from ball import *
from powerUp import *
from laser import *
import globalVar
from globalVar import TOP, BOTTOM, LEFT, LIVES, SCORE, WIDTH, HT, SHOOT_COOLDOWN, obj_bricks, paddle, power_ups, balls, level, lasers, last_shoot
import globalFunc
from globalFunc import setBricks1, setBricks2, setBricks3, check_ball_death, init_power_ups, game_over


fps = 20
t = 1/fps

def setup():
	os.system('clear')
	globalVar.balls.clear()
	globalVar.power_ups.clear()
	globalVar.obj_bricks.clear()
	globalVar.lasers.clear()
	blank_arr = []
	# blank_arr = np.array([[" " for i in range(WIDTH)] for j in range(HT)])
	for i in range(HT):
		temp=[]
		for j in range(WIDTH):
			temp.append(' ')
		blank_arr.append(temp)

	board_arr = copy.deepcopy(blank_arr)
	newBoard = Board(board_arr)
	globalVar.paddle = Paddle(20, 2)
	newBall = Ball(LEFT+random.randint(0, globalVar.paddle.width-1), globalVar.paddle.y-1,0,0,0)
	globalVar.balls.append(newBall)
	init_power_ups()
	globalVar.LEVEL_START_TIME = time.time()
	if(globalVar.level==0):
		setBricks1()
		globalVar.level=1
	elif(globalVar.level==1):
		# globalVar.power_ups.clear()
		setBricks2()
		globalVar.level=2
	elif(globalVar.level==2):
		# globalVar.power_ups = []
		setBricks3()
		globalVar.level=3
	else:
		game_over()
		print("Score:",globalVar.SCORE)
	return newBoard

def shoot(x,y, paddle_width):
	# print("hi")
	if(int(time.time() - globalVar.last_shoot)>=SHOOT_COOLDOWN):

		os.system('aplay -q ./sounds/laser.wav&')
		globalVar.lasers.append(Laser(x,y-1))
		globalVar.lasers.append(Laser(x+paddle_width-1,y-1))
		globalVar.last_shoot = time.time()
	
# for obj in obj_bricks:
	
# 	print(obj.getx(),obj.gety())
time_limit = [0, 10,15,30]
blank_arr = []
# blank_arr = np.array([[" " for i in range(WIDTH)] for j in range(HT)])
for i in range(HT):
	temp=[]
	for j in range(WIDTH):
		temp.append(' ')
	blank_arr.append(temp)

newBoard = setup()
globalVar.START_TIME = time.time()
while True:
	key = input_to()
	grid = copy.deepcopy(blank_arr)
	if(globalVar.LIVES<=0):

		os.system('clear')
		game_over()
		print("Score:",globalVar.SCORE)
		break
	flag = 0
	for brick in globalVar.obj_bricks:
		if(not brick.is_broken() and brick.strength!=-1):
			flag = 1
	if(globalVar.ufo_dead):
		flag=0
	if(flag == 0):
		if(globalVar.ufo_dead):
			os.system('clear')
			game_over()
			print("Yay")
			print("Score:",globalVar.SCORE)
			os.system('aplay -q ./sounds/win.wav&')
			break
		else:
			setup()
	print("\033[%d;%dH" % (0, 0))
	globalVar.GAME_TIME = int(time.time()-globalVar.START_TIME)

	power_ups_to_del = []
	for power_up in globalVar.power_ups:
		if(power_up.is_activated()):
			power_up.update_active_time()
		elif(power_up.active_time>=power_up.max_time):
			power_ups_to_del.append(power_up)

	for to_del in power_ups_to_del:
		globalVar.power_ups.remove(to_del)


	lasers_to_del = []
	for laser in globalVar.lasers:
		if(laser.dead):
			lasers_to_del.append(laser)

	for to_del in lasers_to_del:
		globalVar.lasers.remove(to_del)

	bombs_to_del = []
	for bomb in globalVar.bombs:
		if(bomb.visible==0):
			bombs_to_del.append(bomb)

	for to_del in bombs_to_del:
		globalVar.bombs.remove(to_del)


	if(key=='d' or key =='D'):
		for ball in globalVar.balls:
			if(ball.is_moving()==0):
				ball.move(1)
		globalVar.paddle.move(1)
	elif(key=="a" or key=="A"):
		for ball in globalVar.balls:
			if(ball.is_moving()==0):
				ball.move(-1)
		globalVar.paddle.move(-1)
	elif(key=="p" or key=="P"):
		for ball in globalVar.balls:
			if(ball.is_moving()==0):
				ball.set_moving()
				ball.move(1)
	elif(key==" "):
		if(globalVar.paddle.areGunsOut()):
			shoot(globalVar.paddle.x, globalVar.paddle.y, globalVar.paddle.width)
	elif(key=='q' or key=='Q'):
		os.system('clear')
		print("You quit")
		print("Your Score:",globalVar.SCORE)
		break
	elif(key=='l' or key=='L'):
		newBoard = setup()
		if(globalVar.level==-1):
			break

	shooter_time = 0
	for power_up in globalVar.power_ups:
		if(isinstance(power_up,Paddle_shooter) and power_up.is_activated()):
			shooter_time = int(power_up.max_time - power_up.active_time)
			break

	grid = newBoard.getArr(str(globalVar.SCORE), str(globalVar.GAME_TIME), str(globalVar.LIVES), shooter_time, grid)
	grid = globalVar.paddle.getArr(Back.BLUE, ' ', grid)
	
	check_ball_death()
	k=0
	j=0
	for ball in globalVar.balls:
		grid = ball.getArr(Fore.WHITE,'●', grid)

	paddle_ball = 0		# =1 if paddle and ball collided
	for ball in globalVar.balls:
		if(ball.is_moving()):
			ret = ball.check_paddle_collision()
			if(ret):
				paddle_ball = 1
			if(ball.is_moving()):	# checking again because if paddle grab is activated, check_paddle_collision will set ball.moving to 0
				ball.check_brick_collision()
				ball.move(1)
		

	for obj in globalVar.obj_bricks:
		if(obj.is_broken()):
			continue
		if(obj.touch==0 and isinstance(obj, Rainbow)):
			obj.change_colour()
		grid = obj.getArr(' ',grid)

	for obj in globalVar.obj_bricks:
		if(obj.is_broken()):
			continue
		if(isinstance(obj,UFO)):
			obj.move(globalVar.paddle.x)
			break

	if(int(time.time()-globalVar.LEVEL_START_TIME)>time_limit[globalVar.level]):
		over = 0
		if(paddle_ball):
			for obj in globalVar.obj_bricks:
				if(obj.is_broken()):
					continue
				if(isinstance(obj, UFO)):
					continue
				else:
					ret = obj.move(globalVar.paddle.y)
				if(ret):
					over = 1
					break
			if(over):
				os.system('clear')
				game_over()
				print("Score:",globalVar.SCORE)
				break
	
	for power_up in power_ups:
		# f = open("debug.txt", "a")
		# f.write(str(power_up.x)+" "+str(power_up.y)+"\n")
		# f.close()
		if(power_up.visible):
			grid = power_up.getArr(Fore.YELLOW, grid)
			power_up.move()

	for laser in globalVar.lasers:
		if(laser.visible):
			laser.check_brick_collision()
			laser.move()
			grid = laser.getArr(Fore.RED, '^', grid)

	for bomb in globalVar.bombs:
		if(bomb.visible):
			bomb.check_paddle_collision()
			bomb.move()
			grid = bomb.getArr(Back.RED, '@', grid)
	#grid = ''.join(grid)
	# print(grid)
	pr = []
	for i in range(HT):
		tem = []
		for j in range(WIDTH):
			tem.append(grid[i][j])
		
		print(''.join(tem))
	
	
	time.sleep(t)


