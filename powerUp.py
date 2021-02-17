
from headers import *
from globalVar import HT, WIDTH, BOTTOM, balls, paddle, POWERS
rows = HT
cols = WIDTH

class PowerUp:
	"""docstring for Paddle"""
	def __init__(self, x, y, sym):
		super().__init__()
		self.width = len(sym)
		self.height = 1
		self.x = x
		self.y = y
		self.v = 2
		self.symbol = sym
		self.visible = 0
		self.max_time = 10
		self.time_active = 0
		self.activated = 0

	def move(self):
		paddle = globalVar.paddle
		if(self.x+self.width > paddle.x and self.x<paddle.x+paddle.width): # powerup is within x coordinates of paddle
			if(self.y+self.height>=paddle.y):
				self.activate_power_up()
		elif(self.y+self.height>=BOTTOM):
			self.visible = 0
		elif(self.y+self.v+self.height>BOTTOM):
			self.y=BOTTOM-self.height-self.v
		self.y += self.v

	def activate_power_up(self):
		# this will be over-ridden for every power up. Polymorphism here :)
		self.activated = 1
		self.visible = 0

	def set_visible(self):
		self.visible = 1

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
		for ball in balls:
			ball.set_thru()

class Fast_ball(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y, globalVar.POWERS['fast'])

	def activate_power_up(self):
		super().activate_power_up()
		for ball in balls:
			ball.incr_vel()

class Shrink_paddle(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y,globalVar.POWERS['shrink'])

	def activate_power_up(self):
		super().activate_power_up()
		globalVar.paddle.shrink()

class Expand_paddle(PowerUp):
	def __init__(self, x, y):
		super().__init__(x,y,globalVar.POWERS['expand'])

	def activate_power_up(self):
		super().activate_power_up()
		globalVar.paddle.expand()
