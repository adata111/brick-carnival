
from headers import *
import globalVar
from globalVar import SCORE, LIVES, paddle
from colorama import init, Fore, Back, Style


class Bomb:
	"""docstring for Bomb"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.v_y = 1
		self.visible = 1
		self.width = 1
		self.height = 1

	def move(self,v=1):
		self.y += self.v_y
		
		if(self.y>globalVar.paddle.y):
			self.visible = 0

	def check_paddle_collision(self):
		check = 0
		paddle = globalVar.paddle
		if(self.x+self.width > paddle.x and self.x<paddle.x+paddle.width): # bomb is within x coordinates of paddle in this frame
			if(self.y+self.height>=paddle.y):
				globalVar.LIVES -= 1
				os.system('aplay -q ./sounds/lose_life.wav&')
				self.visible = 0
			elif(self.y+self.height+self.v_y>paddle.y):
				self.y= paddle.y-self.height-self.v_y		
		

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
		
