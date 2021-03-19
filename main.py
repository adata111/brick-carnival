import copy
from headers import *
from paddle import *
from input import *
from board import *
from ball import *
from powerUp import *
import globalVar
from globalVar import TOP, BOTTOM, LEFT, LIVES, SCORE, WIDTH, HT, obj_bricks, paddle, power_ups, balls, level
import globalFunc
from globalFunc import setBricks1, setBricks2, check_ball_death, init_power_ups, game_over


fps = 20
t = 1/fps

def setup():
	os.system('clear')
	globalVar.balls=[]
	globalVar.power_ups.clear()
	globalVar.obj_bricks=[]
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
	if(globalVar.level==0):
		setBricks1()
		globalVar.level=1
	elif(globalVar.level==1):
		# globalVar.power_ups.clear()
		setBricks2()
		globalVar.level=2
	elif(globalVar.level==2):
		# globalVar.power_ups = []
		setBricks1()
		globalVar.level=3
	else:
		game_over()
		print("Score:",globalVar.SCORE)
	return newBoard

	
# for obj in obj_bricks:
	
# 	print(obj.getx(),obj.gety())
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
	if(flag == 0):
		os.system('clear')
		game_over()
		print("Yay")
		print("Score:",globalVar.SCORE)
		break
	print("\033[%d;%dH" % (0, 0))
	globalVar.GAME_TIME = int(time.time()-globalVar.START_TIME)

	power_ups_to_del = []
	for power_up in globalVar.power_ups:
		if(power_up.is_activated()):
			power_up.update_active_time()
		elif(power_up.active_time>power_up.max_time):
			power_ups_to_del.append(power_up)

	for to_del in power_ups_to_del:
		globalVar.power_ups.remove(to_del)


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
	elif(key==" "):
		for ball in globalVar.balls:
			if(ball.is_moving()==0):
				ball.set_moving()
				ball.move(1)
	elif(key=='q' or key=='Q'):
		os.system('clear')
		print("You quit")
		print("Your Score:",globalVar.SCORE)
		break
	elif(key=='l' or key=='L'):
		newBoard = setup()
		if(globalVar.level==-1):
			break


	grid = newBoard.getArr(str(globalVar.SCORE), str(globalVar.GAME_TIME), str(globalVar.LIVES), grid)
	grid = globalVar.paddle.getArr(Back.BLUE, ' ', grid)
	
	check_ball_death()
	k=0
	j=0
	for ball in globalVar.balls:
		grid = ball.getArr(Fore.WHITE,'●', grid)
	for obj in globalVar.obj_bricks:
		if(obj.is_broken()):
			continue
		grid = obj.getArr(' ',grid)

	for ball in globalVar.balls:
		if(ball.is_moving()):
			ball.check_paddle_collision()
			if(ball.is_moving()):	# checking again because if paddle grab is activated, check_paddle_collision will set ball.moving to 0
				ball.check_brick_collision()
				ball.move(1)
	
	for power_up in power_ups:
		f = open("debug.txt", "a")
		f.write(str(power_up.x)+" "+str(power_up.y)+"\n")
		f.close()
		if(power_up.visible):
			grid = power_up.getArr(Fore.YELLOW, grid)
			power_up.move()

	#grid = ''.join(grid)
	# print(grid)
	pr = []
	for i in range(HT):
		tem = []
		for j in range(WIDTH):
			tem.append(grid[i][j])
		
		print(''.join(tem))
	
	
	time.sleep(t)


