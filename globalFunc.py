import random
from brick import *
from powerUp import *
import globalVar
from globalVar import TOP, HT, WIDTH, x_bricks, obj_bricks, balls, power_ups, all_power_ups

def init_power_ups():
    globalVar.all_power_ups.extend(['expand','shrink','fast', 'thru', 'multi', 'grab'])
    for i in range(20):
        globalVar.all_power_ups.append(None)

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

def setBricks():
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
                
                globalVar.obj_bricks.append(Exploding(13,4,i,y, get_power_up(ind, i+5,y)))
            elif((j+i)%7 ==0):
                globalVar.obj_bricks.append(Brick(13,4,i,y))
            else:
                ind = random.randint(0,len(globalVar.all_power_ups)-1)
                globalVar.obj_bricks.append(Breakable(13,4,i,y, 1+((i+j)%3), get_power_up(ind, i+5,y)))
            k+=1

def check_ball_death():
    to_del = []
    for ball in globalVar.balls:
        if(ball.dead):
            to_del.append(ball)

    for it in to_del:
        globalVar.balls.remove(it)


def game_over():
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