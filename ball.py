from headers import *
import globalVar
from globalVar import TOP, BOTTOM, LIVES, HT, WIDTH, LEFT, RIGHT, obj_bricks, paddle, ALT_LIVES
rows = HT
cols = WIDTH

class Ball:
	"""docstring for Ball
	contains all methods that can modify state of the ball.
	"""
	def __init__(self, x, y, vx, vy, m):
		super().__init__()
		self.width = 1
		self.height = 1
		self.x = x
		self.y = y
		self.v_x = vx
		self.v_y = -1
		self.moving = m
		self.thru = 0
		self.dead = 0
		self.fast = 0
		self.fire = 0

	def move(self,v=1):
		paddle=globalVar.paddle
		temp = self.v_x

		if(self.moving == 0): # movement with paddle
			if(paddle.x+paddle.width>=RIGHT and v>0):
				v = 0
			elif(paddle.x<=LEFT and v<0):
				v = 0
			self.x += v*paddle.v
			return
		self.x += self.v_x

		if(self.x+self.width>=RIGHT and self.v_x>0):
			self.v_x = -self.v_x
		elif(self.x<=LEFT and self.v_x<0):
			self.v_x = -self.v_x
		elif(self.x+self.v_x+self.width>RIGHT):
			self.x = RIGHT-self.v_x-self.width
		elif(self.x+self.v_x<LEFT):
			self.x = LEFT-self.v_x

		if(self.v_x!=temp):
			os.system('aplay -q ./sounds/ball_wall.wav&')


		self.y += self.v_y
		temp = self.v_y
		if(self.y+self.height>=BOTTOM and self.v_y>0):	# v_y>0 means it will go down
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

		if(self.v_y!=temp):
			os.system('aplay -q ./sounds/ball_wall.wav&')


	def check_paddle_collision(self):
		paddle = globalVar.paddle
		check =0
		if(self.x+self.width > paddle.x and self.x<paddle.x+paddle.width): # ball is within x coordinates of paddle
			if(self.y+self.height==paddle.y):
				self.set_vel(- self.v_y)
				if(paddle.is_sticky()):
					self.moving = 0
				os.system('aplay -q ./sounds/ball_paddle.wav&')
				return 1
		if(self.x+self.width<paddle.x+paddle.width and self.x+self.v_x+self.width>paddle.x and self.v_x>=0): # top-left collision possible
			if(self.y+self.height<paddle.y and self.y+self.v_y+self.height>paddle.y):
				# top-left collision 
				self.y = paddle.y-self.height - self.v_y
				check=1
		elif(self.x>(paddle.x) and self.x+self.v_x<paddle.width+paddle.x and self.v_x<=0): # top-right collision possible
			if(self.y+self.height<paddle.y and self.v_y+self.y+self.height>paddle.y):
				# top-right collision 
				# self.set_vel(-self.v_y)
				self.y = paddle.y-self.height - self.v_y
				check=1
		return check


	def check_brick_collision(self):
		check = 0
		v_x=self.v_x
		v_y=self.v_y
		for brick in reversed(globalVar.obj_bricks):
			if(brick.is_broken()):
				continue
			if((self.x>=brick.getx() and self.x+self.width<=brick.getx()+brick.width) and ((self.y<=brick.gety()+brick.height and self.y+self.height>=brick.gety() and self.v_y<0) or (self.y+self.height>=brick.gety() and self.y<=brick.gety()+brick.height and self.v_y>0)) ):
				if(self.v_y==0): #not possible, but okay
					continue
				# collision with top or bottom brick surface 
				v_y = -self.v_y
				check = 1
			elif(((self.x+self.width==brick.getx() and self.v_x>0) or (self.x==brick.getx()+brick.width and self.v_x<0)) and (self.y+self.height<=brick.gety()+brick.height and self.y>=brick.gety())):
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
					if(brick.strength == 100):	# exploding
						brick.reduce_strength(self.v_x, self.v_y)
						break
					if(self.fire==0):
						brick.break_it(self.v_x, self.v_y)
					else:
						brick.fire(self.v_x, self.v_y)
					break
				if(brick.strength != -1):
					if(self.fire):
						brick.fire(self.v_x, self.v_y)
					else:
						brick.reduce_strength(self.v_x, self.v_y)
				else:
					if(self.fire):
						brick.fire(self.v_x, self.v_y)
				break
		if(check):

			os.system('aplay -q ./sounds/ball_brick.wav&')
			return
		check=0
		for brick in globalVar.obj_bricks:
			if(brick.is_broken()):
				continue
			if((self.x+self.width)==brick.getx() and self.v_x>0): # top-left or bottom-left collision possible
				if(self.y==brick.gety()+brick.height and self.v_y<0): 
					# bottom-left collision
					v_y = -self.v_y
					v_x = -self.v_x
					# self.v_x = -self.v_x
					check = 1
				elif(self.y+self.height==brick.gety() and self.v_y>0):
					# top-left collision 
					# self.v_y = -self.v_y
					v_x = -self.v_x
					v_y = -self.v_y
					check = 1
			elif(self.x==(brick.getx()+brick.width) and self.v_x<0): # top-right or bottom-right collision possible
				if(self.y==brick.gety()+brick.height and self.v_y<0): 
					# bottom-right collision
					v_y = -self.v_y
					v_x = -self.v_x
					# self.v_x = -self.v_x
					check = 1
				elif(self.y+self.height==brick.gety() and self.v_y>0):
					# top-right collision 
					# self.v_y = -self.v_y
					v_x = -self.v_x
					v_y = -self.v_y
					check = 1
			if(check):
				# ball-brick collision occurred, reduce brick strength now
				os.system('aplay -q ./sounds/ball_brick.wav&')
				if(self.thru==0):
					self.v_y = v_y
					self.v_x = v_x
				else:
					# if thru ball power up is activated, destroy bricks 
					if(brick.strength == 100): # exploding brick
						brick.reduce_strength(self.v_x, self.v_y)
						break
					if(self.fire==0):
						brick.break_it(self.v_x, self.v_y)
					else:
						# if fire ball power up is activated, destroy bricks exploding bricks style
						brick.fire(self.v_x, self.v_y)
					break
				if(brick.strength != -1):
					if(self.fire):
						brick.fire(self.v_x, self.v_y)
					else:
						brick.reduce_strength(self.v_x, self.v_y)
				else:
					# unbreakable brick breaks only if the ball is fireball
					if(self.fire):
						brick.fire(self.v_x, self.v_y)
				break
		if(check):
			return
		check=0
		for brick in globalVar.obj_bricks:
			if(brick.is_broken()):
				continue

			if(self.x+self.width<brick.getx() or self.x>brick.getx()+brick.width or self.y+self.height<brick.gety() or self.y>brick.gety()+brick.height):

				x = self.x+self.v_x
				y = self.y + self.v_y
				for b_x in range(brick.getx(),brick.getx()+brick.width):
					for b_y in range(brick.gety(),brick.gety()+brick.height):
						if(x==b_x and y==b_y):
							if(self.v_x>0 and self.v_y>0):	# approaching from north west
								if(x-brick.getx()<y-brick.gety()):
									v_x = -self.v_x
								elif(x-brick.getx()==y-brick.gety()):
									v_x = -self.v_x
									v_y = -self.v_y
								else:
									v_y = -self.v_y
							elif(self.v_x<0 and self.v_y>0):	# approaching from north east
								if(brick.getx()+brick.width-x<y-brick.gety()):
									v_x = -self.v_x
								elif(brick.getx()+brick.width-x==y-brick.gety()):
									v_x = -self.v_x
									v_y = -self.v_y
								else:
									v_y = -self.v_y
							elif(self.v_x>0 and self.v_y<0):	# approaching from south west
								if(x-brick.getx()<brick.gety()+brick.height-y):
									v_x = -self.v_x
								elif(x-brick.getx()==brick.gety()+brick.height-y):
									v_x = -self.v_x
									v_y = -self.v_y
								else:
									v_y = -self.v_y
							elif(self.v_x<0 and self.v_y<0):	# approaching from south east
								if(brick.getx()+brick.width-x<brick.gety()+brick.height-y):
									v_x = -self.v_x
								elif(brick.getx()+brick.width-x==brick.gety()+brick.height-y):
									v_x = -self.v_x
									v_y = -self.v_y
								else:
									v_y = -self.v_y
							
							
							check = 1
							break
					if(check==1):
						break
				if(check):
					os.system('aplay -q ./sounds/ball_brick.wav&')
					if(self.thru==0):
						self.x += self.v_x
						self.y += self.v_y
						self.v_y = v_y
						self.v_x = v_x
					else:
						if(brick.strength == 100):
							brick.reduce_strength(self.v_x, self.v_y)
							break
						if(self.fire==0):
							brick.break_it(self.v_x, self.v_y)
						else:
							brick.fire(self.v_x, self.v_y)
						break
					if(brick.strength != -1):
						if(self.fire):
							brick.fire(self.v_x, self.v_y)
						else:
							brick.reduce_strength(self.v_x, self.v_y)
					else:
						if(self.fire):
							brick.fire(self.v_x, self.v_y)
							
					break

			

	def kill_ball(self):
		p = globalVar.paddle
		if(p==None):
			return
		os.system('aplay -q ./sounds/lose_life.wav&')
		if(globalVar.ALT_LIVES>0):
			globalVar.ALT_LIVES -= 1
			self.dead = 1
		else:
			l = globalVar.LIVES
			globalVar.LIVES = l-1
			for power_up in globalVar.power_ups:
				if(power_up.is_activated()):
					power_up.deactivate_power_up()
			self.x = random.randint(p.x, p.x+p.width-self.width)
			self.y = p.y-self.height
			self.moving = 0
			self.v_y = -2
			self.v_x = 0
			self.thru = 0
			self.fast = 0
			self.fire = 0
		
	def set_props(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.v_x = vx
		self.v_y = vy

	def is_moving(self):
		return self.moving
	def set_moving(self):
		self.moving = 1
		if(not globalVar.paddle.is_sticky()):
			self.set_vel()

	def set_vel(self, vy=-1):
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
		self.v_y = vy

	def incr_vel(self):
		if(self.fast):
			return
		self.fast = 1
		if(self.v_y > 0):
			self.v_y += 1
		elif(self.v_y < 0 or not (self.is_moving())):
			self.v_y -= 1

	def decr_vel(self):
		if(self.fast):
			self.fast =0
			if(self.v_y > 0):
				self.v_y -= 1
			elif(self.v_y < 0):
				self.v_y += 1

	def getArr(self, colour, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			for j in range(x,x+w):
				arr[i][j] = (colour +symbol + Style.RESET_ALL)
		return arr

	def set_thru(self):
		self.thru = 1

	def unset_thru(self):
		self.thru = 0

	def set_fire(self):
		self.fire = 1
	def unset_fire(self):
		self.fire = 0