
from headers import *
import globalVar
from globalVar import TOP, BOTTOM, LIVES, HT, WIDTH, LEFT, RIGHT, obj_bricks
rows = HT
cols = WIDTH

class Ball:
	"""docstring for Paddle"""
	def __init__(self, width, height, paddle_width):
		super().__init__()
		self.width = width
		self.height = height
		self.x = random.randint(1,paddle_width)
		self.y = rows-2-height
		self.v_x = 0
		self.v_y = 0
		self.moving = 0
		self.weird = 0

	def move(self,v=1, paddle=None):
		if(self.moving == 0):
			if(paddle.x+paddle.width>=cols-1 and v>0):
				v = 0
			elif(paddle.x<2 and v<0):
				v = 0
			self.x += v*paddle.v
			return

		if(self.x+self.width>=RIGHT and self.v_x>0):
			self.v_x = -self.v_x
		elif(self.x<LEFT and self.v_x<0):
			self.v_x = -self.v_x

		self.x += self.v_x

		
		if(self.y+self.height>=BOTTOM and self.v_y>0):	# v_y>0 means it will go down
			# f=open("debug.txt","a")
			# f.write(str(self.y) + " " + str(self.height) + " " + str(HT) + "\n")
			# f.close()
			self.kill_ball(paddle)
			return

		elif(self.y<=TOP and self.v_y<0):
			self.v_y = -self.v_y
		self.y += self.v_y
		# if(self.y<16 and self.weird==0):
		# 	self.x = 2*self.x
		# 	self.v_x = 2*self.v_x
		# 	self.weird=1
		# elif(self.y>=16 and self.weird):
		# 	self.x = self.x/2
		# 	self.v_x = self.v_x/2
		# 	self.weird=0
		

	def check_paddle_collision(self, paddle):
		if(self.x+self.width > paddle.x and self.x<paddle.x+paddle.width): # ball is within x coordinates of paddle
			if(self.y+self.height==paddle.y):
				self.v_y = - self.v_y

	def check_brick_collision(self):
		check = 0
		for brick in globalVar.obj_bricks:
			if(brick.is_broken()):
				continue
			# f=open("debug.txt","a")
			# f.write(str(brick.x)+ " " + str(brick.y) + " " + str(self.x) + " " + str(self.y) +"\n")
			# f.close()
			if((self.x>=brick.getx() and self.x+self.width<=brick.getx()+brick.width) and (self.y<=brick.gety()+brick.height and self.y+self.height>=brick.gety()) ):
				if(self.v_y==0): #not possible, but okay
					continue
				# collision with top or bottom brick surface 
				self.v_y = -self.v_y
				check = 1
			elif((self.x+self.width>=brick.getx() and self.x<=brick.getx()+brick.width) and (self.y+self.height<=brick.gety()+brick.height and self.y>=brick.gety())):
				if(self.v_x==0):
					continue
				# collision with left or right edge of brick
				self.v_x = -self.v_x
				check = 1
			elif((self.x+self.width)==brick.getx() and self.v_x>0): # top-left or bottom-left collision possible
				if(self.y==brick.gety()+brick.height and self.v_y<0): 
					# bottom-left collision
					self.v_y = -self.v_y
					self.v_x = -self.v_x
					check = 1
				elif(self.y+self.height==brick.gety() and self.v_y>0):
					# top-left collision 
					self.v_y = -self.v_y
					self.v_x = -self.v_x
					check = 1
			elif(self.x==(brick.getx()+brick.width) and self.v_x<0): # top-right or bottom-right collision possible
				if(self.y==brick.gety()+brick.height and self.v_y<0): 
					# bottom-right collision
					self.v_y = -self.v_y
					self.v_x = -self.v_x
					check = 1
				elif(self.y+self.height==brick.gety() and self.v_y>0):
					# top-right collision 
					self.v_y = -self.v_y
					self.v_x = -self.v_x
					check = 1
			if(check):
				if(brick.strength != -1):
					brick.reduce_strength()
				break
			

	def kill_ball(self, p):
		if(p==None):
			return
		l = globalVar.LIVES
		globalVar.LIVES = l-1
		self.x = random.randint(p.x, p.x+p.width-self.width)
		self.y = p.y-self.height
		self.moving = 0
		self.v_y = -2
		


	def is_moving(self):
		return self.moving
	def set_moving(self):
		self.moving = 1
		self.set_vel()

	def set_vel(self, vx=2, vy=-2):
		self.v_x = vx
		self.v_y = vy

	def getArr(self, color, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		print(x,y,h,w)
		for i in range(y, y+h):
			arr[i] = arr[i][:x] + color + Style.BRIGHT + symbol*w + Fore.RESET + Back.RESET + arr[i][x+w:]
		return arr
