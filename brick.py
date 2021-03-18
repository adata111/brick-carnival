
from headers import *
import globalVar
from globalVar import SCORE, obj_bricks
from colorama import init, Fore, Back, Style

colours = [Back.GREEN, Back.YELLOW, Back.RED ]

class Brick:
	def __init__(self, width, height, x,y, pu=None):
		super().__init__()
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.broken = 0
		self.strength = -1
		self.power_up = pu
		# self.actual_x = xx
		self.colour = Back.WHITE

	def getArr(self, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			for j in range(x,x+w):
				arr[i][j] = (self.colour +symbol + Back.RESET)
		return arr

	def is_broken(self):
		return self.broken

	def break_it(self, v_x, v_y):
		if(self.strength != 100):	# exploding brick strength
			globalVar.SCORE += 5*(4-self.strength)
		else:
			globalVar.SCORE += 20
		self.broken=1
		self.colour = Back.RESET
		if(self.power_up):
			self.power_up.set_visible(v_x, v_y)

	def getx(self):
		return self.x

	def gety(self):
		return self.y


class Breakable(Brick):
	def __init__(self, width, height, x,y,st, pu):
		Brick.__init__(self,width, height, x,y, pu)
		self.strength = st
		self.colour = colours[st-1]

	def reduce_strength(self, v_x, v_y):
		self.strength -= 1
		if (self.strength == 0):
			self.break_it(v_x, v_y)
			return
		globalVar.SCORE += 5*(4-self.strength)
		self.colour = colours[self.strength-1]

class Exploding(Brick):
	def __init__(self, width, height, x,y,pu):
		Brick.__init__(self,width, height, x,y, pu)
		self.strength = 100
		if((x+y)%2):
			self.colour = Back.LIGHTMAGENTA_EX
		else:
			self.colour = Back.MAGENTA

	def reduce_strength(self, v_x, v_y):
		self.break_it(v_x, v_y)
		for brick in globalVar.obj_bricks:
			if(brick.is_broken()):
				continue
			if(brick.getx()+brick.width==self.getx() and brick.gety()==self.gety()): #left
				if(brick.strength == 100):
					brick.reduce_strength(v_x, v_y)
				else:
					brick.break_it(v_x, v_y)

			elif(brick.getx()+brick.width==self.getx() and brick.gety()+brick.height==self.gety()): #top-left
				if(brick.strength == 100):
					brick.reduce_strength(v_x, v_y)
				else:
					brick.break_it(v_x, v_y)

			elif(brick.getx()+brick.width==self.getx() and brick.gety()==self.gety()+self.height): #bottom-left
				if(brick.strength == 100):
					brick.reduce_strength(v_x, v_y)
				else:
					brick.break_it(v_x, v_y)

			elif(brick.getx()==self.getx() and brick.gety()+brick.height==self.gety()): #top
				if(brick.strength == 100):
					brick.reduce_strength(v_x, v_y)
				else:
					brick.break_it(v_x, v_y)

			elif(brick.getx()==self.getx() and brick.gety()==self.gety()+self.height): #bottom
				if(brick.strength == 100):
					brick.reduce_strength(v_x, v_y)
				else:
					brick.break_it(v_x, v_y)

			elif(brick.getx()==self.getx()+self.width and brick.gety()==self.gety()): #right
				if(brick.strength == 100):
					brick.reduce_strength(v_x, v_y)
				else:
					brick.break_it(v_x, v_y)

			elif(brick.getx()==self.getx()+self.width and brick.gety()+brick.height==self.gety()): #top-right
				if(brick.strength == 100):
					brick.reduce_strength(v_x, v_y)
				else:
					brick.break_it(v_x, v_y)

			elif(brick.getx()==self.getx()+self.width and brick.gety()==self.gety()+self.height): #bottom-right
				if(brick.strength == 100):
					brick.reduce_strength(v_x, v_y)
				else:
					brick.break_it(v_x, v_y)
