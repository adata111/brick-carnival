
from headers import *
import globalVar
from globalVar import SCORE
from colorama import init, Fore, Back, Style

colours = [Back.GREEN, Back.YELLOW, Back.RED ]

class Brick:
	def __init__(self, width, height, x,y, xx):
		super().__init__()
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.broken = 0
		self.strength = -1
		self.actual_x = xx
		self.colour = Back.WHITE
		print(x,y)
		print("width height",width,height)

	def getArr(self, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			arr[i] = arr[i][:x+5] + self.colour +(symbol)*(w) + Back.RESET + arr[i][x+5+w:]
		return arr

	def is_broken(self):
		return self.broken

	def break_it(self):
		self.broken=1
		self.colour = Back.RESET

	def getx(self):
		return self.actual_x

	def gety(self):
		return self.y

	def setx(self, k):
		self.x = self.x-(k*10)


class Breakable(Brick):
	def __init__(self, width, height, x,y, xx,st):
		Brick.__init__(self,width, height, x,y, xx)
		self.strength = st
		self.colour = colours[st-1]

	def reduce_strength(self):
		globalVar.SCORE += 5*(4-self.strength)
		self.strength -= 1
		if (self.strength == 0):
			self.break_it()
			return
		self.colour = colours[self.strength-1]

