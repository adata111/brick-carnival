
from headers import *
import globalVar
from globalVar import TOP, BOTTOM, LIVES, HT, WIDTH, LEFT, RIGHT, obj_bricks, paddle, ALT_LIVES

class Laser:
	"""docstring for Laser
	Laser objects are created when the Paddle shooter power up is activated and the player presses spacebar
	"""
	def __init__(self, x, y):
		super().__init__()
		self.width = 1
		self.height = 1
		self.visible = 1
		self.dead=0
		self.x = x
		self.y = y
		self.v_x = 0
		self.v_y = -1

	def move(self,v=1):
		self.y += self.v_y
		
		if(self.y<=TOP and self.v_y<0):
			self.visible = 0
			self.dead=1
		elif(self.y+self.v_y<TOP):
			self.y = TOP-self.v_y

	def check_brick_collision(self):
		check = 0
		for brick in (globalVar.obj_bricks):
			if(brick.is_broken()):
				continue
			if(self.y <= brick.gety()+brick.getheight() and self.x>=brick.getx() and self.x+self.width<=brick.getx()+brick.getwidth()):
				check = 1
			elif(self.y+self.v_y<brick.gety()+brick.getheight() and self.x>=brick.getx() and self.x+self.width<=brick.getx()+brick.getwidth()):
				self.y=brick.gety()+brick.getheight()-self.v_y
			
			if(check):
				os.system('aplay -q ./sounds/ball_brick.wav&')
				self.visible=0
				self.dead=1
				if(brick.strength != -1):
					brick.reduce_strength(self.v_x, self.v_y)
				break
		

	def getArr(self, colour, symbol, arr):
		y = self.y
		h = self.height
		w = self.width
		x = self.x
		for i in range(y, y+h):
			for j in range(x,x+w):
				arr[i][j] = (colour +symbol + Style.RESET_ALL)
		return arr