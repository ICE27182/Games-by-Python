#BRICK BREAKER v1.0

#Intro
print('Brick Breaker v1.0')
input('------------Press Enter To Continue------------')


#Functions
import math,time,threading

def draw_c(coordinate,y_axis=False,x_limit=True,end='\n'):
    '''支持24色彩色输出 坐标格式为coordinate={y:{x:color}}
    color应为3或4位integer 前两位表示颜色 第三位为 暗/默认/高亮 第四位可选为闪烁
    y_axis 默认为False 不显示纵坐标 0或False为不显示 1或True为显示
    x_limit 默认为True 不限制'''
    if y_axis != True and y_axis != False and y_axis != 0 and y_axis != 1:
        raise ValueError('y_axis仅接受True或False或1或0')
    if x_limit != True and x_limit != False and x_limit != 0 and x_limit != 1:
        raise ValueError('x_limit仅接受True或False或1或0')     
    x_max,x_min = 0,0
    for y in coordinate.keys():
        for x in coordinate[y].keys():
            if x > x_max:
                x_max = x
            elif x < x_min:
                x_min = x
    def x_line(former_x):
        if x in coordinate[y].keys():   
                print('  '*(x-former_x-1),end='')
                if coordinate[y][x] == 0:
                    print(f'\033[0m██\033[0m',end='')
                elif coordinate[y][x] < 1000:
                    print(f'\033[{str(coordinate[y][x])[2]};{str(coordinate[y][x])[0:2]}m██\033[0m',end='')
                elif len(str(coordinate[y][x])) == 4:
                    print(f'\033[{int(str(coordinate[y][x])[2])};{int(str(coordinate[y][x])[3])};{int(str(coordinate[y][x])[0:2])}m██\033[0m',end='')
                former_x = x
        return former_x
    for y in range(max(coordinate.keys()),min(coordinate.keys())-1,-1):
        if y_axis == True or y_axis == 1:
            print(y,'\t',end='')        
        if y not in coordinate.keys() or coordinate[y]=={}:
            print('')
            continue 
        if x_limit == False or x_limit == 0:
            former_x = x_min-1
            for x in range(x_min,x_max+1):
                former_x = x_line(former_x)
        elif x_limit == True or x_limit == 1:
            former_x = 0
            for x in range(0,x_max+1):
                former_x = x_line(former_x)
        print('')
    print(end,end='')

def brick(bricks):
    '''Adding all bricks' shape and color to coordinate.'''
    for i in range(1,bricks_count+1):
        if i in bricks.keys() and len(bricks[i]) != 0:
            for y in range(bricks[i][1]-1,bricks[i][1]-bricks['s'][1],-1):                
                for x in range(bricks[i][0]+1,bricks[i][0]+bricks['s'][0]):
                    coordinate[y].update({x:bricks['c']*10+1})
                coordinate[y][bricks[i][0]] = bricks['c']*10
                coordinate[y][bricks[i][0]+bricks['s'][0]-1] = bricks['c']*10                
            coordinate[bricks[i][1]].update({x:bricks['c']*10 for x in range(bricks[i][0],bricks[i][0]+bricks['s'][0])})
            coordinate[bricks[i][1]-bricks['s'][1]+1].update({x:bricks['c']*10 for x in range(bricks[i][0],bricks[i][0]+bricks['s'][0])})
            
def sin(theta):    return math.sin(theta*math.pi/180)
def cos(theta):    return math.cos(theta*math.pi/180)
def Int(val):    return int(round(val,0))
def angle(theta,max=180,min=-180):
    '''To ensure that the theta is in the right range.'''
    while theta > max:
        theta -= 360
    while theta < min:
        theta += 360
    return theta

def pad():
    '''A function for adding the paddle's shape in to coordiante.'''
    coordinate[1].update({x:padata[2] for x in range(paddle-padata[1]//2,paddle+padata[1]//2+1)})
    coordinate[2].update({x:padata[2] for x in range(paddle-padata[1]//2+1,paddle+padata[1]//2)})

def biu(theta,bottom_bounce=False):
    '''A function for ball boucing on the walls, bricks and paddle,
    also enabling the ball to break bricks it hits.
    The bottom_bounce works as a cheat.'''

    #Ball's moving
    ball[0] += cos(theta)*velocity
    ball[1] += sin(theta)*velocity

    #Bouncing on the walls
    #Left, Right, Top
    if ball[0] <= 0:
        ball[0] = 0
        theta = 180-theta
    elif ball[0] >= frame[0]+1:
        ball[0] = frame[0]
        theta = 180-theta
    elif ball[1] >= frame[1]+1:
        ball[1] = frame[1]
        theta = -theta
    #Bottom
    elif ball[1] <= 0 and bottom_bounce == True:    #cheat on
        ball[1] = 0
        theta = -theta
    elif ball[1] <= 0 and bottom_bounce == False:    #cheat off and losing the game
        return 'LOSER'
    
    #Bouncing on the paddle
    #On its top
    elif Int(ball[1]) in (1,2) and Int(ball[0]) in range(paddle-padata[1]//2+1,paddle+padata[1]//2):
        theta = -theta
    #On its leaning side
    elif Int(ball[1]) in (1,2) and Int(ball[0]) in (paddle-padata[1]//2,paddle+padata[1]//2):
        #theta = angle(360-2*padata[0]-theta)   May have a bug so keep it unused now
        theta = -theta

    #Hitting the bricks
    for i in range(1,bricks_count+1):
        if i not in bricks.keys():  
            continue

        if Int(ball[0]) in range(bricks[i][0]+1,bricks[i][0]+bricks['s'][0]):
            if Int(ball[1]) in range(bricks[i][1]-bricks['s'][1],bricks[i][1]+1):
                theta = -theta   #hitting on the brick's top or bottom
                del bricks[i]
        
        elif Int(ball[0]) in (bricks[i][0],bricks[i][0]+bricks['s'][0]):
            if Int(ball[1]) in range(bricks[i][1]-bricks['s'][1]+1,bricks[i][1]):
                theta = 180 - theta   #hitting on the brick's side
                del bricks[i]
            
            elif Int(ball[1]) in (bricks[i][1],bricks[i][1]-bricks['s'][1]):
                theta = angle(270 - theta)   #hitting on the corner of the brick   May have a bug here
                del bricks[i]
    
    coordinate[Int(ball[1])].update({Int(ball[0]):ball[2]})
    return theta

def control():
    '''A funcuntion for receiving control.'''
    global c,state,cheat
    state,c = 0,0
    while True:
        c = input()
        if 'a' in c and 'd' not in c:
            c = int(- 2 / 3 * padata[1])
            break
        elif 'd' in c and 'a' not in c:
            c = int( 2 / 3 * padata[1])
            break
        elif c == 'wwssaaddbaba':
            cheat = True
    state = 1

timer = []
#Arguments
frame = (120,60)
bricks = {
    1:(36,30),
    2:(56,30),
    3:(76,30),
    4:(36,40),
    5:(56,40),
    6:(76,40),
    7:(36,50),
    8:(56,50),
    9:(76,50),
    'c':32,'s':(8,4),
    }
bricks_count = max([n for n in bricks.keys() if type(n) == int])
velocity = 1   #Don't set a value that is too high. May cause bugs. 
theta = 160   #Default angle for the ball
ball = [60,5,361]   #Default position a for the ball
paddle = 20
padata = (45,15,3315)
cheat = False    #use wwssaaddbaba to turn it on

#A part of control part using threading
state,c = 0,0
E = threading.Thread(target=control,daemon=True)
E.start()

while len(bricks) >= 2:
    #frame
    coordinate = {}    # {y:{x:color}}
    coordinate[frame[1]+1] = {x:0 for x in range(0,frame[0]+2)}
    coordinate[0] = coordinate[frame[1]+1]
    for y in range(frame[1],0,-1):
        coordinate[y] = {0:0, frame[0]+1:0}
    #Add the paddle's coordiante into coordinate, the dict
    pad()
    #Fly the ball and break the bricks
    theta = biu(theta,cheat)
    #Add all bricks(alive) into coordiante, the dict
    brick(bricks)
    
    if theta == 'LOSER':
        break

    #print('\n'*150)
    draw_c(coordinate)
    
    if len(bricks) == 2:
        break
    
    if state == 1:
        if paddle + c in range(padata[1]//2, frame[0] - padata[1]//2 +1):
            paddle += c
        elif paddle + c < padata[1]//2:
            paddle = padata[1]//2 +1
        elif paddle - c > frame[0] - padata[1]//2 +1 :
            paddle = frame[0] - padata[1]//2 +2
        E = threading.Thread(target=control,daemon=True)
        E.start()
    if cheat:
        print('Cheat is on')
    
    time.sleep(1/60)

if theta == 'LOSER':
    print('YOU PATHETIC EXCUSE FOR HUMAN BEINGS LOSE THE GAME')
elif cheat == False:
    print('You, the mighty BRICK BREAKER, have passed the Game')
