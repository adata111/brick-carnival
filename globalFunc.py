from brick import *
from powerUp import *
import globalVar
from globalVar import TOP, HT, WIDTH, x_bricks, obj_bricks, balls, power_ups

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
                globalVar.obj_bricks.append(Exploding(13,4,i,y, None))
            elif((j+i)%7 ==0):
                globalVar.obj_bricks.append(Brick(13,4,i,y))
            else:
                newPowerUp = Fast_ball( i+5, y)
                globalVar.power_ups.append(newPowerUp)
                globalVar.obj_bricks.append(Breakable(13,4,i,y, 1+((i+j)%3), newPowerUp))
            k+=1

def check_ball_death():
    to_del = []
    for ball in globalVar.balls:
        if(ball.dead):
            to_del.append(ball)

    for it in to_del:
        globalVar.balls.remove(it)
