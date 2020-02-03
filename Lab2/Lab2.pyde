#Patrick, Shea, Jonathan, Alexanne

x=25
y=550

import random
import class_ball
import class_bricks

def draw_star(x,y):
    ellipse(x,y,5,5)

def top_margin():
    fill(0)
    rect(0,0,width,20)

def border():
    fill(91,91,92)
    rect(0,20,width,10)
    rect(0,20,10,height)
    rect(width-10,20,height,width)
    
def slider():
    global x,y
    if keyPressed:
        if keyCode== LEFT:
            x=x-10
        if keyCode== RIGHT:
            x=x+10
    fill(245,42,15)
    ellipse(x,y+13,25,25)
    ellipse(x+75,y+13,25,25)
    fill(91,91,92)
    rect(x,y,75,25)
    if x < 15:
        x = 15
    if x > 480:
        x = 480    
    if mousePressed:
        x=mouseX
    if x < 15:
        x = 15
    if x > 480:
        x = 480

def setup():
    global Ball
    global bricks
    size(580,600)
    Ball = class_ball.Ball(x+40,y-15)
    
    bricks = []
    for j in range(16):
        for i in range(14):
            pos_x = i * 40
            pos_y = j * 15
            Brick = class_bricks.Brick(pos_x,pos_y,40,15)
            bricks.append(Brick)

def draw():
    global bricks, Ball

    background (14,47,130)
    fill(255)
    for i in range(10):
     rvar = random.random()
     draw_star(random.random()*width, map(rvar,0,1,1,600))
    
    top_margin()
    border()
    slider()
    Ball.update()
    Ball.draw()
    
    pushMatrix()
    translate(10,30)
    for i in range(len(bricks)):
        if bricks[i].hit_test(Ball.pos_x, Ball.pos_y) == False :
            bricks[i].active = not bricks[i].active
        bricks[i].draw()
    popMatrix()
    
