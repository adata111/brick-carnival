
from headers import *
import globalVar
from globalVar import SCORE
from colorama import init, Fore, Back, Style

colours = [Back.GREEN, Back.YELLOW, Back.RED ]

class Brick:
	def __init__(self, width, height, x,y):
		super().__init__()
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.broken = 0
		self.strength = -1
		# self.actual_x = xx
		self.colour = Back.WHITE

	def getArr(self, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			arr[i] = arr[i][:x] + (self.colour +symbol + Back.RESET)*(w) + arr[i][x+w:]
		return arr

	def is_broken(self):
		return self.broken

	def break_it(self):
		self.broken=1
		self.colour = Back.RESET

	def getx(self):
		return self.x

	def gety(self):
		return self.y


class Breakable(Brick):
	def __init__(self, width, height, x,y,st):
		Brick.__init__(self,width, height, x,y)
		self.strength = st
		self.colour = colours[st-1]

	def reduce_strength(self):
		globalVar.SCORE += 5*(4-self.strength)
		self.strength -= 1
		if (self.strength == 0):
			self.break_it()
			return
		self.colour = colours[self.strength-1]

