

HT=50
SCREEN=200
WIDTH=200
DEAD = 0
INPUT_CHAR=''
# PLAY_AREA 
TOP = 5
BOTTOM = HT-1
LEFT = 1
RIGHT = WIDTH-2

obj_bricks=[]
x_bricks = []
paddle = None
balls = []
power_ups = []
all_power_ups = []
level = 0
gravity = 1

START_TIME = 0
LEVEL_START_TIME = 0
GAME_TIME=100

LIVES = 5
ALT_LIVES=0
SCORE = 0

POWERS = {'thru':'T', 'shrink':'S', 'expand':'E', 'fast':'F', 'grab':'G', 'multiplier':'M'}
