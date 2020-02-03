import random
class Ball:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_x = 0
        self.speed_y = 0

        
    def update(self):
        # updates the position of the ball according to game physics.
        self.pos_x = self.pos_x + self.speed_x
        self.pos_y = self.pos_y + self.speed_y
        if self.pos_x > 560 - 10 :
            self.speed_x = -2
        if self.pos_y < 30 :
            self.speed_y = 2
        if self.pos_y > height - 25 :
            self.speed_y = -2
        if self.pos_x < 20 :
            self.speed_x = 2
        
    def draw(self):
        # Draws the ball on the screen
        pos_x=0
        pos_y=0
        rvar = random.random()
        if self.speed_x==0:
            fill(255)
            ellipse(self.pos_x, self.pos_y+13,15,15)
        else:
            fill(map(rvar,0,1,255,0))
            ellipse(self.pos_x, self.pos_y+13,12,12)
        if keyPressed and self.speed_x ==0:
            if keyCode== LEFT:
                self.pos_x=self.pos_x-10
            if keyCode== RIGHT:
                self.pos_x=self.pos_x+10
        if mousePressed:
            self.speed_x = 2
            self.speed_y = -2
