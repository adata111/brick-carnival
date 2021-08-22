
from headers import *
import globalVar
from globalVar import SCORE, LIVES, paddle


class Bomb:
	"""docstring for Bomb
	Bomb dropped by UFO in level 3
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.v_y = 1
		self.visible = 1
		self.width = 1
		self.height = 1

	def move(self):
		self.y += self.v_y
		if(self.y>globalVar.paddle.y):	# If it goes below paddle, make it disappear
			self.visible = 0

	def check_paddle_collision(self):
		paddle = globalVar.paddle
		if(self.x+self.width > paddle.getx() and self.x<paddle.getx()+paddle.getwidth()): # bomb is within x coordinates of paddle in this frame
			if(self.y+self.height>=paddle.gety()):
				globalVar.LIVES -= 1
				os.system('aplay -q ./sounds/lose_life.wav&')
				self.visible = 0
			elif(self.y+self.height+self.v_y>paddle.gety()):
				self.y= paddle.gety()-self.height-self.v_y		
		

	def getArr(self, colour, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			for j in range(x,x+w):
				arr[i][j] = (colour +symbol + Style.RESET_ALL)
		return arr
		
