
from headers import *
import globalVar
from globalVar import TOP, BOTTOM, LIVES, HT, WIDTH, LEFT, RIGHT, obj_bricks, paddle, ALT_LIVES
rows = HT
cols = WIDTH

class Bullet:
	"""docstring for Ball"""
	def __init__(self, x, y):
		super().__init__()
		self.width = 1
		self.height = 1
		self.visible = 1
		self.dead=0
		self.x = x
		# self.x=RIGHT-14
		self.y = y
		# self.y=TOP+5
		self.v_x = 0
		self.v_y = -1

	def move(self,v=1):
		self.y += self.v_y
		
		if(self.y<=TOP and self.v_y<0):
			self.visible = 0
			self.dead=1
		elif(self.y+self.v_y<TOP):
			# self.v_y = -self.v_y
			self.y = TOP-self.v_y

	def check_brick_collision(self):
		check = 0
		for brick in reversed(globalVar.obj_bricks):
			if(brick.is_broken()):
				continue
			# f=open("debug.txt","a")
			# f.write(str(brick.x)+ " " + str(brick.y) + " " + str(self.x) + " " + str(self.y) +"\n")
			# f.close()
			if(self.y <= brick.gety()+brick.height and self.x>=brick.getx() and self.x+self.width<=brick.getx()+brick.width):
				check = 1
			elif(self.y+self.v_y<brick.gety()+brick.height and self.x>=brick.getx() and self.x+self.width<=brick.getx()+brick.width):
				self.y=brick.gety()+brick.height-self.v_y
			
			if(check):
				self.visible=0
				self.dead=1
				if(brick.strength != -1):
					brick.reduce_strength(self.v_x, self.v_y)
				break
		

	def is_moving(self):
		return self.moving
	def set_moving(self):
		self.moving = 1
		if(not globalVar.paddle.is_sticky()):
			self.set_vel()

	def getArr(self, colour, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			for j in range(x,x+w):
				arr[i][j] = (colour +symbol + Style.RESET_ALL)
			#arr[i] = arr[i][:x] + color + Style.BRIGHT + symbol + Fore.RESET + Back.RESET + arr[i][x+1:]
		# arr1 = list(arr[y])
		# arr1[x] = Back.CYAN+" "+Style.RESET_ALL
		# arr[y] = ''.join(arr1)
		return arr