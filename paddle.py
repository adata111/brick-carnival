
from headers import *
import globalVar
from globalVar import HT, WIDTH,BOTTOM, LEFT, balls
rows = HT
cols = WIDTH

class Paddle:
	"""docstring for Paddle"""
	def __init__(self, width, height):
		super().__init__()
		self.width = width
		self.height = height
		self.x = LEFT
		self.y = BOTTOM-height
		self.v = 2
		self.sticky = 0

	def move(self,v):
		if(self.x+self.width>=cols-1 and v>0):
			v = 0
		elif(self.x<2 and v<0):
			v = 0
		self.x += v*self.v

	def getArr(self, color, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			for j in range(x, x+w):
				arr[i][j] = color + Style.BRIGHT + symbol + Fore.RESET + Back.RESET
		return arr

	def shrink(self):
		if (self.width<=10):
			return
		for ball in globalVar.balls:
			if(not ball.is_moving()):
				if(ball.x>self.x+self.width-10):
					ball.x = self.x+self.width-10
		self.width -= 10


	def expand(self):
		if (self.width>=50):
			return
		self.width += 10

	def grab(self):
		self.sticky = 1

	def unGrab(self):
		self.sticky = 0

	def is_sticky(self):
		return self.sticky