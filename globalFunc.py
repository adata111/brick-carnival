import random
from brick import *
# from powerUp import *
import globalVar
from globalVar import TOP, HT, WIDTH, LEFT, x_bricks, obj_bricks, balls, power_ups, all_power_ups, level

def init_power_ups():
    globalVar.all_power_ups = []
    globalVar.all_power_ups.extend(['expand','shrink','fast', 'thru', 'multi', 'grab','shooter'])
    for i in range(20):
        globalVar.all_power_ups.append(None)



def setBricks1():
    for i in range(WIDTH-18, 2, -10):
        globalVar.x_bricks.append(i)
    k=0
    for j in range(0, 3):
        k=0
        y=TOP+j*4
        for i in range(WIDTH-19-(13), 10, -13):
            #print(i,j)
            if(j==1 and k>=3 and k<10):
                ind = random.randint(0,len(globalVar.all_power_ups)-1)
                
                globalVar.obj_bricks.append(Exploding(13,4,i,y))
            elif((j+i)%7 ==0):
                globalVar.obj_bricks.append(Brick(13,4,i,y))
            else:
                ind = random.randint(0,len(globalVar.all_power_ups)-1)
                # ind = 0
                globalVar.obj_bricks.append(Breakable(13,4,i,y, 1+((i+j)%3)))
            k+=1


def setBricks2():
    for i in range(WIDTH-18, 2, -10):
        globalVar.x_bricks.append(i)
    k=0
    for j in range(0, 3):
        k=0
        brick_width = 10
        y= TOP + j*4
        for i in range(LEFT,WIDTH-brick_width, brick_width ):
            if(k%5==0):
                globalVar.obj_bricks.append(Brick(brick_width,4,i,y))
            elif(k%5==4):
                ind = random.randint(0,len(globalVar.all_power_ups)-1)
                globalVar.obj_bricks.append(Exploding(brick_width,4,i,y))
            elif(k%5==2):
                ind = random.randint(0,len(globalVar.all_power_ups)-1)
                globalVar.obj_bricks.append(Rainbow(brick_width,4,i,y))
            else:
                ind = random.randint(0,len(globalVar.all_power_ups)-1)
                # ind = 0
                globalVar.obj_bricks.append(Breakable(brick_width,4,i,y, 1+((i+j)%3)))
            k+=1


def check_ball_death():
    to_del = []
    for ball in globalVar.balls:
        if(ball.dead):
            to_del.append(ball)

    for it in to_del:
        globalVar.balls.remove(it)


def game_over():
    globalVar.level = -1
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT+ "                                                     ".center(WIDTH))                 
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT+ "  _____                         ____                 ".center(WIDTH))                 
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT+ " / ____|                       / __ \                ".center(WIDTH))              
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT+ "| |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ ".center(WIDTH))
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +"| | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|".center(WIDTH))
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +"| |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   ".center(WIDTH))
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT +" \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   ".center(WIDTH))
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT+ "                                                     ".center(WIDTH)+Style.RESET_ALL)                 
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT+ "                                                     ".center(WIDTH)+Style.RESET_ALL)                 
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT+ "                                                     ".center(WIDTH)+Style.RESET_ALL)  