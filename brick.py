
from headers import *
from powerUp import *
from bomb import *
import globalVar
from globalVar import SCORE, obj_bricks, ufo_dead, bombs

colours = [Back.GREEN, Back.YELLOW, Back.RED ]

ufo = [
[" "," "," "," "," "," "," "," ","_","_","_"," "," "," "," "," "," "," "," "],
[" "," "," "," ","_","_","_","/"," "," "," ","\\","_","_","_"," "," "," "," "], 
[" "," "," ","/"," "," "," ","'","-","-","-","'"," "," "," ","\\"," "," "," "],
[" "," "," ","'","-","-","_","_","_","_","_","_","_","-","-","'"," "," "," "]]

unbreakable_strength = -1
exploding_strength = 100

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
    elif(pu=='shooter'):
        pu = Paddle_shooter(x,y)
        globalVar.power_ups.append(pu)
    elif(pu=='fire'):
        pu = Fire_ball(x,y)
        globalVar.power_ups.append(pu)
    # globalVar.all_power_ups.pop(ind)
    return pu

def destroy_brick(brick, v_x, v_y):
	if(brick.strength == 100):
		brick.reduce_strength(v_x, v_y)
	else:
		brick.break_it(v_x, v_y)


class Brick:
	def __init__(self, width, height, x,y, touch=1):
		super().__init__()
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.broken = 0
		self.strength = unbreakable_strength
		self.power_up = None
		self.touch = touch
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

	def getheight(self):
		return self.height

	def getwidth(self):
		return self.width

	def getstrength(self):
		return self.strength

	def move(self,paddle_y):
		self.y+=1
		if(self.y+self.height>=paddle_y):
			return 1
		return 0

	def fire(self, v_x, v_y):
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
		self.strength = exploding_strength
		if((x+y)%2):
			self.colour = Back.LIGHTMAGENTA_EX
		else:
			self.colour = Back.MAGENTA

	def reduce_strength(self, v_x, v_y):
		self.fire(v_x,v_y)

class Rainbow(Brick):
	def __init__(self, width, height, x,y, st):
		Brick.__init__(self,width, height, x,y,0)
		self.strength = st
		self.colour = colours[self.strength-1]

	def change_colour(self):
		self.strength-=1
		if(self.strength==0):
			self.strength=3
		self.colour = colours[self.strength-1]

	def reduce_strength(self, v_x, v_y):
		self.strength -= 1
		self.touch = 1
		if (self.strength == 0):
			self.break_it(v_x, v_y)
			return
		globalVar.SCORE += 5*(4-self.strength)
		self.colour = colours[self.strength-1]



class UFO(Brick):
	def __init__(self, width, height, x,y):
		Brick.__init__(self,width, height, x,y)
		self.strength = 5
		self.bomb_rate = 5
		self.last_bomb = time.time()-2
		self.colour = Back.CYAN
		globalVar.ufo_strength = self.strength
		os.system('aplay -q ./sounds/ufo.wav&')

	def move(self,paddle_x):
		self.x = paddle_x
		if(int(time.time()-self.last_bomb)>=self.bomb_rate):
			self.last_bomb = time.time()
			self.drop_bomb()

	def break_it(self,v_x,v_y):
		super().break_it(v_x, v_y)
		globalVar.ufo_dead = 1

	def drop_bomb(self):
		globalVar.bombs.append(Bomb(self.x+9, self.y+self.height))

	def getArr(self, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			for j in range(x,x+w):
				arr[i][j] = (self.colour + ufo[i-y][j-x] + Back.RESET)
		return arr

	def reduce_strength(self,v_x,v_y):
		self.strength -= 1
		globalVar.ufo_strength = self.strength
		globalVar.SCORE += 10
		if(self.strength==4):
			self.shields_up(1)
		if(self.strength==2):
			self.shields_up(1)
		
		if (self.strength == 0):
			self.break_it(v_x,v_y)

	def shields_up(self,m):
		for i in range(LEFT, WIDTH-self.width, self.width):
			globalVar.obj_bricks.append(Defense(self.width,self.height,i,self.y+(m*self.height)))	#bottom

class Defense(Brick):
	"""docstring for Defense"""
	def __init__(self, width, height, x,y):
		Brick.__init__(self,width,height,x,y)
		self.strength = 1
		self.colour = Back.GREEN
		
	def reduce_strength(self,v_x,v_y):
		self.strength -= 1
		if (self.strength == 0):
			self.break_it(v_x, v_y)
			return

	def break_it(self, v_x, v_y):
		globalVar.SCORE += 20
		self.broken=1
		self.colour = Back.RESET

	def move(self, paddle_y):
		pass
		

		