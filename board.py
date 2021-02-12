from headers import *

from globalVar import HT, WIDTH
from brick import *

class Board:
	def __init__(self, grid):
		 self.grid = np.zeros((HT,WIDTH),dtype='<U20')
		# self.grid[:] = ' '
		# self.grid[0,:] = '_'
		# self.grid[HT-1,:] = '_'
		# self.grid[:,0] = '|'
		# self.grid[:,WIDTH-1] = '|'


	def getArr(self, score, lives, grid):
		
		sc = 'Score: '+score
		li = 'Lives: '+lives
		l_sc = len(sc)
		l_li = len(li)
		
		grid[0] = '_'*WIDTH
		grid[HT-1] = '_'*WIDTH
		# for i in range(0,HT):
		# 	if (i==0):
		# 		grid[i] = ' ' + grid[i][1:WIDTH-2] + ' \n'
		# 	else:
		# 		grid[i] = '|' + grid[i][1:WIDTH-2] + '|\n'
		grid[2] = grid[2][:5]+ sc + grid[2][l_sc+5:WIDTH-30] + li + grid[2][WIDTH-30+l_li:] 
		
		return grid