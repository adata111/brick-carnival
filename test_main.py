import unittest
import mock
from main import *

class Test(unittest.TestCase):

	def test_initialization(self):
		board = setup()
		# test_board_size
		assert len(board.grid) == globalVar.HT 
		assert len(board.grid[0]) == globalVar.WIDTH
		# test_initial_level
		assert globalVar.level == 1


	def test_ball_func(self):
		pass

if __name__ == '__main__':
	unittest.main()