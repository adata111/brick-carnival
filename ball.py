
from headers import *
import globalVar
from globalVar import TOP, BOTTOM, LIVES, HT, WIDTH, LEFT, RIGHT, obj_bricks, paddle
rows = HT
cols = WIDTH

class Ball:
	"""docstring for Paddle"""
	def __init__(self, width, height):
		super().__init__()
		self.width = width
		self.height = height
		self.x = random.randint(1, globalVar.paddle.width)
		# self.x=RIGHT-14
		self.y = globalVar.paddle.y-height
		# self.y=TOP+5
		self.v_x = 0
		self.v_y = 0
		self.moving = 0
		self.thru = 0

	def move(self,v=1):
		paddle=globalVar.paddle
		if(self.moving == 0): # movement with paddle
			if(paddle.x+paddle.width>=RIGHT and v>0):
				v = 0
			elif(paddle.x<2 and v<0):
				v = 0
			self.x += v*paddle.v
			return

		if(self.x+self.width>=RIGHT and self.v_x>0):
			self.v_x = -self.v_x
		elif(self.x<=LEFT and self.v_x<0):
			self.v_x = -self.v_x
		elif(self.x+self.v_x+self.width>RIGHT):
			self.x = RIGHT-self.v_x-self.width
		elif(self.x+self.v_x<LEFT):
			self.x = LEFT-self.v_x

		self.x += self.v_x

		
		if(self.y+self.height>=BOTTOM and self.v_y>0):	# v_y>0 means it will go down
			# f=open("debug.txt","a")
			# f.write(str(self.y) + " " + str(self.height) + " " + str(HT) + "\n")
			# f.close()
			self.kill_ball()
			return

		elif(self.y<=TOP and self.v_y<0):
			self.v_y = -self.v_y
		if(self.y+self.v_y>BOTTOM):
			self.y = BOTTOM-self.height
			# self.kill_ball()
			return
		elif(self.y+self.v_y<TOP):
			# self.v_y = -self.v_y
			self.y = TOP-self.v_y
		self.y += self.v_y


	def check_paddle_collision(self):
		paddle = globalVar.paddle
		if(self.x+self.width > paddle.x and self.x<paddle.x+paddle.width): # ball is within x coordinates of paddle
			if(self.y+self.height==paddle.y):
				self.set_vel(- self.v_y)
				if(paddle.is_sticky()):
					self.moving = 0
					
				return
		if(self.x+self.width<paddle.x+paddle.width and self.x+self.v_x+self.width>paddle.x and self.v_x>=0): # top-left collision possible
			if(self.y+self.height<paddle.y and self.y+self.v_y+self.height>paddle.y):
				# top-left collision 
				# self.set_vel(-self.v_y)
				self.y = paddle.y-self.height - self.v_y
		elif(self.x>(paddle.x) and self.x+self.v_x<paddle.width+paddle.x and self.v_x<=0): # top-right collision possible
			if(self.y+self.height<paddle.y and self.v_y+self.y+self.height>paddle.y):
				# top-right collision 
				# self.set_vel(-self.v_y)
				self.y = paddle.y-self.height - self.v_y


	def check_brick_collision(self):
		check = 0
		v_x=self.v_x
		v_y=self.v_y
		for brick in reversed(globalVar.obj_bricks):
			if(brick.is_broken()):
				continue
			# f=open("debug.txt","a")
			# f.write(str(brick.x)+ " " + str(brick.y) + " " + str(self.x) + " " + str(self.y) +"\n")
			# f.close()
			if((self.x>=brick.getx() and self.x+self.width<=brick.getx()+brick.width) and ((self.y<=brick.gety()+brick.height and self.y+self.height>=brick.gety() and self.v_y<0) or (self.y+self.height>=brick.gety() and self.y<=brick.gety()+brick.height and self.v_y>0)) ):
				if(self.v_y==0): #not possible, but okay
					continue
				# collision with top or bottom brick surface 
				v_y = -self.v_y
				check = 1
			elif((self.x+self.width==brick.getx() or self.x==brick.getx()+brick.width) and (self.y+self.height<=brick.gety()+brick.height and self.y>=brick.gety())):
				if(self.v_x==0):
					continue
				# collision with left or right edge of brick
				v_x = -self.v_x
				check = 1
			
			if(check):
				if(self.thru==0):
					self.v_y = v_y
					self.v_x = v_x
				else:
					brick.break_it()
					break
				if(brick.strength != -1):
					brick.reduce_strength()
				break
		if(check):
			return
		check=0
		for brick in globalVar.obj_bricks:
			if(brick.is_broken()):
				continue
			if((self.x+self.width)==brick.getx() and self.v_x>0): # top-left or bottom-left collision possible
				if(self.y==brick.gety()+brick.height and self.v_y<0): 
					# bottom-left collision
					v_y = -self.v_y
					# self.v_x = -self.v_x
					check = 1
				elif(self.y+self.height==brick.gety() and self.v_y>0):
					# top-left collision 
					# self.v_y = -self.v_y
					v_x = -self.v_x
					check = 1
			elif(self.x==(brick.getx()+brick.width) and self.v_x<0): # top-right or bottom-right collision possible
				if(self.y==brick.gety()+brick.height and self.v_y<0): 
					# bottom-right collision
					v_y = -self.v_y
					# self.v_x = -self.v_x
					check = 1
				elif(self.y+self.height==brick.gety() and self.v_y>0):
					# top-right collision 
					# self.v_y = -self.v_y
					v_x = -self.v_x
					check = 1
			if(check):
				if(self.thru==0):
					self.v_y = v_y
					self.v_x = v_x
				else:
					brick.break_it()
					break
				if(brick.strength != -1):
					brick.reduce_strength()
				break
		if(check):
			return
		check=0
		for brick in globalVar.obj_bricks:
			if(brick.is_broken()):
				continue

			if((self.x+self.width)<brick.getx()+brick.width and self.x+self.v_x+self.width>brick.getx() and self.v_x>=0): # top-left or bottom-left collision possible
				if(self.y>brick.gety()+brick.height and self.y+self.v_y<brick.gety()+brick.height): 
					# bottom-left collision
					v_y = -self.v_y
					self.y = brick.gety()+brick.height
					# self.v_x = -self.v_x
					check = 1
				elif(self.y+self.height<brick.gety() and self.y+self.v_y+self.height>brick.gety()):
					# top-left collision 
					# self.v_y = -self.v_y
					v_x = -self.v_x
					self.x = brick.getx()+brick.width
					check = 1
			elif(self.x>(brick.getx()) and self.x+self.v_x<brick.width+brick.getx() and self.v_x<=0): # top-right or bottom-right collision possible
				if(self.y>brick.gety()+brick.height and self.v_y+self.y<brick.gety()+brick.height): 
					# bottom-right collision
					v_y = -self.v_y
					self.y = brick.gety()+brick.height
					# self.v_x = -self.v_x
					check = 1
				elif(self.y+self.height<brick.gety() and self.v_y+self.y+self.height>brick.gety()):
					# top-right collision 
					# self.v_y = -self.v_y
					v_x = -self.v_x
					self.x = brick.getx()+brick.width
					check = 1
			if(check):
				if(self.thru==0):
					self.v_y = v_y
					self.v_x = v_x
				else:
					brick.break_it()
					break
				if(brick.strength != -1):
					brick.reduce_strength()
				break

			

	def kill_ball(self):
		p = globalVar.paddle
		if(p==None):
			return
		l = globalVar.LIVES
		globalVar.LIVES = l-1
		self.x = random.randint(p.x, p.x+p.width-self.width)
		self.y = p.y-self.height
		self.moving = 0
		self.v_y = -2
		self.v_x = 0
		self.thru = 0
		globalVar.paddle.unGrab()
		


	def is_moving(self):
		return self.moving
	def set_moving(self):
		self.moving = 1
		if(not globalVar.paddle.is_sticky()):
			self.set_vel()

	def set_vel(self, vy=-2):
		paddle = globalVar.paddle
		cen = paddle.width//2
		p1 = cen//2
		p3 = cen+p1
		if(self.x - paddle.x<=p1):
			self.v_x = self.v_x - 2
		elif(self.x - paddle.x<cen):
			self.v_x = self.v_x - 1
		elif(self.x - paddle.x==cen):
			self.v_x = self.v_x
		elif(self.x - paddle.x<=p3):
			self.v_x += 1
		elif(self.x - paddle.x>p3):
			self.v_x += 2
		# self.v_x = self.v_x + (-((self.x-paddle.x-(paddle.width//2))//-5))
		# self.v_x = 2
		self.v_y = vy

	def incr_vel(self):
		if(self.v_x > 0):
			self.v_x += 1
		elif(self.v_x < 0):
			self.v_x -= 1
		if(self.v_y > 0):
			self.v_y += 1
		elif(self.v_y < 0 or not (self.is_moving())):
			self.v_y -= 1

	def getArr(self, colour, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		print(x,y,h,w)
		for i in range(y, y+h):
			for j in range(x,x+w):
				arr[i][j] = (colour +symbol + Back.RESET)
			#arr[i] = arr[i][:x] + color + Style.BRIGHT + symbol + Fore.RESET + Back.RESET + arr[i][x+1:]
		# arr1 = list(arr[y])
		# arr1[x] = Back.CYAN+" "+Style.RESET_ALL
		# arr[y] = ''.join(arr1)
		return arr

	def set_thru(self):
		self.thru = 1

	def unset_thru(self):
		self.thru = 0