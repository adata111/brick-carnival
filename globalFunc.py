from brick import *
from ball import *
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
        for i in range(WIDTH-15-(10*(j%2)), 4+(j%2), -10):
            #print(i,j)
            if((j+i)%7 ==0):
                globalVar.obj_bricks.append(Brick(10,2,i,y))
            else:
                newPowerUp = Thru_ball( i+5, y)
                globalVar.power_ups.append(newPowerUp)
                globalVar.obj_bricks.append(Breakable(10,2,i,y, 1+((i+j)%3), newPowerUp))
            k+=1

def create_ball():
    newBall = Ball(1, 1, 20)
    globalVar.balls.append(newBall)
    return newBall

