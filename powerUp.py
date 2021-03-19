
from headers import *
from ball import *
import globalVar
from globalVar import HT, WIDTH, BOTTOM, LEFT, RIGHT, balls, paddle, POWERS, ALT_LIVES, gravity
rows = HT
cols = WIDTH

class PowerUp:
	"""docstring for Power Up"""
	def __init__(self, x, y, sym):
		super().__init__()
		self.width = len(sym)
		self.height = 1
		self.x = x
		self.y = y
		self.v_x = 2
		self.v_y = 2
		self.symbol = sym
		self.visible = 0
		self.max_time = 10
		self.start_time = time.time()
		self.active_time = 0
		self.activated = 0

	def update_active_time(self):
		self.active_time = time.time()-self.start_time
		# print(self.active_time)
		if(self.active_time>=self.max_time):
			self.deactivate_power_up()

	def move(self):
		paddle = globalVar.paddle
		self.y += self.v_y
		self.x += self.v_x

		if(self.x+self.width > paddle.x and self.x<paddle.x+paddle.width): # powerup is within x coordinates of paddle in this frame
			if(self.y+self.height>=paddle.y):
				self.activate_power_up()
		elif(self.x+self.width+self.v_x > paddle.x and self.x+self.v_x<paddle.x+paddle.width): # powerup is within x coordinates of paddle in next frame
			if(self.y+self.height+self.v_y>paddle.y):
				self.y= paddle.y-self.height-self.v_y
		elif(self.y+self.height>=BOTTOM and self.v_y>0):
			self.visible = 0
		elif(self.y+self.v_y+self.height>BOTTOM):
			self.y=BOTTOM-self.height-self.v_y

		elif(self.y <= TOP and self.v_y<0):
			self.v_y = -self.v_y
		elif(self.y+self.v_y < TOP):	# will go out of top boundary in next iteration
			self.y = TOP - self.v_y		#so that it hits TOP in this time instant and then in the next instant, the previous elif will be executed

		elif((self.x<=LEFT and self.v_x<0) or (self.x + self.width>= RIGHT and self.v_x>0)):	# left or right wall collision
			self.v_x = -self.v_x

		elif(self.x + self.v_x <LEFT):	#will go out of left boundary in next iteration
			self.x = LEFT - self.v_x
		elif(self.x + self.v_x + self.width > RIGHT):
			self.x = RIGHT - self.v_x - self.width

		self.v_y += gravity

	def is_activated(self):
		return self.activated

	def activate_power_up(self):
		# Polymorphism here :)
		self.activated = 1
		self.start_time = time.time()
		self.visible = 0

	def deactivate_power_up(self):
		# this will be over-ridden for every power up. Polymorphism here :)
		pass

	def set_visible(self, v_x, v_y):
		self.visible = 1
		self.v_x = v_x
		self.v_y = v_y

	def getArr(self, colour, arr):
		
		if(self.visible==0):
			return arr
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			# arr[i] = arr[i][:x] + color + Style.BRIGHT + self.symbol + Fore.RESET + Back.RESET + arr[i][x+w:]
			for j in range(x,x+w):
				arr[i][j] = (colour+ Style.BRIGHT +self.symbol + Style.RESET_ALL)
		return arr

class Thru_ball(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y, globalVar.POWERS['thru'])

	def activate_power_up(self):
		super().activate_power_up()
		for ball in globalVar.balls:
			if(ball.thru==0):
				ball.set_thru()
			else:
				self.active_time=self.max_time+1	# so that it gets deleted in next frame
				self.activated = 0		# so that it doesn't update active_time in next frame
				for powerup in globalVar.power_ups:
					if(isinstance(powerup,Thru_ball)):
						powerup.max_time += self.max_time
						break

	def deactivate_power_up(self):
		self.activated = 0
		for ball in globalVar.balls:
			ball.unset_thru()

class Fast_ball(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y, globalVar.POWERS['fast'])

	def activate_power_up(self):
		super().activate_power_up()
		for ball in globalVar.balls:
			ball.incr_vel()

	def deactivate_power_up(self):
		self.activated = 0
		for ball in globalVar.balls:
			ball.decr_vel()

class Shrink_paddle(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y,globalVar.POWERS['shrink'])
		did_shrink=0

	def activate_power_up(self):
		super().activate_power_up()
		self.did_shrink = globalVar.paddle.shrink()

	def deactivate_power_up(self):
		self.activated = 0
		if(self.did_shrink):
			globalVar.paddle.expand()

class Expand_paddle(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y,globalVar.POWERS['expand'])
		did_expand = 0

	def activate_power_up(self):
		super().activate_power_up()
		self.did_expand = globalVar.paddle.expand()

	def deactivate_power_up(self):
		self.activated = 0
		if(self.did_expand):
			globalVar.paddle.shrink()

class Paddle_grab(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y,globalVar.POWERS['grab'])

	def activate_power_up(self):
		super().activate_power_up()
		if(globalVar.paddle.grab==0):
			globalVar.paddle.grab()	
		else:
			self.active_time=self.max_time+1	# so that it gets deleted in next frame
			self.activated = 0		# so that it doesn't update active_time in next frame
			for powerup in globalVar.power_ups:
				if(isinstance(powerup,Paddle_grab)):
					powerup.max_time += self.max_time
					break

	def deactivate_power_up(self):
		self.activated = 0
		globalVar.paddle.unGrab()		

class Ball_multiplier(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y, globalVar.POWERS['multiplier'])

	def activate_power_up(self):
		super().activate_power_up()
		temp = []
		for ball in globalVar.balls:
			v=-ball.v_x
			if(v == 0):
				v=2
			newBall = Ball(ball.x,ball.y,v,ball.v_y,1)
			temp.append(newBall)
			# newBall.set_props(ball.x,ball.y,-ball.v_x,ball.v_y)
		for newBall in temp:
			globalVar.balls.append(newBall)
			globalVar.ALT_LIVES += 1


class Paddle_shooter(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y,globalVar.POWERS['shooter'])

	def activate_power_up(self):
		super().activate_power_up()
		if(globalVar.paddle.shooter==0):
			globalVar.paddle.gunsOut()	
		else:
			self.active_time=self.max_time+1	# so that it gets deleted in next frame
			self.activated = 0		# so that it doesn't update active_time in next frame
			for powerup in globalVar.power_ups:
				if(isinstance(powerup,Paddle_shooter)):
					powerup.max_time += self.max_time
					f=open("debug.txt","a")
					f.write(str(powerup.max_time)+"\n")
					f.close()
					break

	def deactivate_power_up(self):
		self.activated = 0
		globalVar.paddle.killGuns()		
