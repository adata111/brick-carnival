
from headers import *
from globalVar import HT, WIDTH
rows = HT
cols = WIDTH

class Paddle:
	"""docstring for Paddle"""
	def __init__(self, width, height):
		super().__init__()
		self.width = width
		self.height = height
		self.x = 1
		self.y = rows-2
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
			arr[i] = arr[i][:x] + color + Style.BRIGHT + symbol*w + Fore.RESET + Back.RESET + arr[i][x+w:]
		return arr

	def shrink(self):
		if (self.width<=4):
			return
		self.width -= 2


	def expand(self):
		if (self.width>=36):
			return
		self.width += 2

	def paddleGrab(self):
		self.sticky = 1