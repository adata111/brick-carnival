from headers import *

from globalVar import HT, WIDTH, TOP, BOTTOM, RIGHT,LEFT, level
from brick import *


class Board:
	def __init__(self, grid):
		 self.grid = np.zeros((HT,WIDTH),dtype='<U20')
		# self.grid[:] = ' '
		# self.grid[0,:] = '_'
		# self.grid[HT-1,:] = '_'
		# self.grid[:,0] = '|'
		# self.grid[:,WIDTH-1] = '|'


	def getArr(self, score, tim, lives, shooter_time, grid):
		
		sc = 'Score: '+score
		li = 'Lives: '+lives
		ti = 'Time: '+tim
		lev = 'Level: '+ str(globalVar.level)
		l_lev = len(lev)
		l_sc = len(sc)
		l_li = len(li)
		l_ti = len(ti)
		shoo = 'Shooter time left: '+str(shooter_time)
		l_shoo = len(shoo)
		
		# grid[0] = '_'*WIDTH
		# grid[HT-1] = '_'*WIDTH
		for j in range(WIDTH):
			grid[1][j] = Back.MAGENTA + Style.BRIGHT + '_' + Fore.RESET + Back.RESET
		border = ['\'',"-","'","-"]
		for i in (TOP-1, HT-1):
			for j in range(WIDTH):
				grid[i][j] = Back.WHITE+Fore.BLUE + Style.BRIGHT + border[j%4] + Style.RESET_ALL		# for i in range(0,HT):
		for i in range(TOP-1,BOTTOM):
			grid[i][LEFT-1] = Back.WHITE+ Style.BRIGHT + ' ' + Style.RESET_ALL
			grid[i][RIGHT+1] = Back.WHITE+ Style.BRIGHT + ' ' + Style.RESET_ALL
		# 	if (i==0):
		# 		grid[i] = ' ' + grid[i][1:WIDTH-2] + ' \n'
		# 	else:
		# 		grid[i] = '|' + grid[i][1:WIDTH-2] + '|\n'
		# grid[2] = grid[2][:5]+ sc + grid[2][l_sc+5:WIDTH-30] + li + grid[2][WIDTH-30+l_li:] 
		t = ''.join(grid[3])		
		if(shooter_time!=0):
			tem = t[:5]+ sc + t[l_sc+5:WIDTH-((WIDTH+l_ti)//2)-20] +  shoo + t[WIDTH-((WIDTH+l_ti)//2)-20+l_shoo:WIDTH-((WIDTH+l_ti)//2)+5] + ti + t[WIDTH-((WIDTH+l_ti)//2)+5+l_ti:WIDTH-50] + lev + t[WIDTH-50+l_lev :WIDTH-30] + li + t[WIDTH-30+l_li:]
			grid[3] = list(tem)
		else:
			tem = t[:5]+ sc + t[l_sc+5:WIDTH-((WIDTH+l_ti)//2)] + ti + t[WIDTH-((WIDTH+l_ti)//2)+l_ti:WIDTH-50] + lev + t[WIDTH-50+l_lev :WIDTH-30] + li + t[WIDTH-30+l_li:] 
			grid[3] = list(tem)
		
		return grid