from brick import *
import globalVar
from globalVar import HT, WIDTH, x_bricks, obj_bricks

def setBricks():
    for i in range(7,WIDTH-10, 10):
        globalVar.x_bricks.append(i)
    k=0
    for j in range(4, 16, 2):
        k=0
        for i in range(2,WIDTH+160, 20):
            #print(i,j)
            if((j+i)%7 ==0):
                globalVar.obj_bricks.append(Brick(10,2,i,j, globalVar.x_bricks[k]))
            else:
                globalVar.obj_bricks.append(Breakable(10,2,i,j, globalVar.x_bricks[k],1+((i+j)%3)))
            k+=1

