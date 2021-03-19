
from headers import *
from powerUp import *
import globalVar
from globalVar import SCORE, obj_bricks
from colorama import init, Fore, Back, Style

colours = [Back.GREEN, Back.YELLOW, Back.RED ]


def get_power_up(ind,x,y):
    pu = globalVar.all_power_ups[ind]
    if(pu=='expand'):
        pu = Expand_paddle(x,y)
        globalVar.power_ups.append(pu)
    elif(pu=='shrink'):
        pu = Shrink_paddle(x,y)
        globalVar.power_ups.append(pu)
    elif(pu=='fast'):
        pu = Fast_ball(x,y)
        globalVar.power_ups.append(pu)
    elif(pu=='thru'):
        pu = Thru_ball(x,y)
        globalVar.power_ups.append(pu)
    elif(pu=='multi'):
        pu = Ball_multiplier(x,y)
        globalVar.power_ups.append(pu)
    elif(pu=='grab'):
        pu = Paddle_grab(x,y)
        globalVar.power_ups.append(pu)
    # globalVar.all_power_ups.pop(ind)
    return pu

class Brick:
	def __init__(self, width, height, x,y, touch=1):
		super().__init__()
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.broken = 0
		self.strength = -1
		self.power_up = None
		self.touch = touch
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
		ind = random.randint(0,len(globalVar.all_power_ups)-1)
		self.power_up = get_power_up(ind,self.x+5,self.y)
		if(self.power_up):
			self.power_up.set_visible(v_x, v_y)

	def getx(self):
		return self.x

	def gety(self):
		return self.y


class Breakable(Brick):
	def __init__(self, width, height, x,y,st):
		Brick.__init__(self,width, height, x,y)
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
	def __init__(self, width, height, x,y):
		Brick.__init__(self,width, height, x,y)
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

class Rainbow(Brick):
	def __init__(self, width, height, x,y):
		Brick.__init__(self,width, height, x,y,0)
		self.strength = 3
		self.colour = colours[self.strength-1]

	def change_colour(self):
		self.strength-=1
		if(self.strength==0):
			self.strength=3
		self.colour = colours[self.strength-1]
		f = open("debug.txt", "a")
		f.write(str(self.colour)+" "+str(self.strength)+"\n")
		f.close()

	def reduce_strength(self, v_x, v_y):
		self.strength -= 1
		self.touch = 1
		if (self.strength == 0):
			self.break_it(v_x, v_y)
			return
		globalVar.SCORE += 5*(4-self.strength)
		self.colour = colours[self.strength-1]
