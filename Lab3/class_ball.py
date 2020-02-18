import random
class Ball:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_x = 0
        self.speed_y = 0
        self.radius = 15

    def starting_point(self):
        #starting point and reset when you lose the ball
        if self.speed_x == 0 and self.speed_y == 0:
            if keyPressed and self.speed_x == 0 and self.speed_y == 0:
                if keyCode == LEFT:
                    self.pos_x=self.pos_x-10
                if keyCode == RIGHT:
                    self.pos_x=self.pos_x+10
                    
            if self.pos_x < 59 and self.speed_x == 0 and self.speed_y == 0:
                self.pos_x = 59
            if self.pos_x > 517 and self.speed_x == 0 and self.speed_y == 0:
                self.pos_x = 517
                
            if mousePressed:
                x=mouseX
                self.speed_x = 5
                self.speed_y = -5
    

    def update(self, sliderx, slidery, sliderz):
        # updates the position of the ball according to game physics.
        if self.speed_x != 0 and self.speed_y != 0:
            self.pos_x = self.pos_x + self.speed_x
            self.pos_y = self.pos_y + self.speed_y
                
            if self.pos_x > width - self.radius - 20:
                self.speed_x = -self.speed_x
                
            if self.pos_y < self.radius:
                self.speed_y = -self.speed_y
                
            if self.pos_y > height + 200:
                self.speed_y = 0
                self.speed_x = 0
                self.pos_x = sliderx + 25
                self.pos_y = slidery
                            
            if self.pos_x < 10:
                self.speed_x = -self.speed_x
            
            if self.pos_y == slidery and sliderx < self.pos_x < sliderz:
                self.speed_y = -self.speed_y


    def draw(self):
        # Draws the ball on the screen
        noStroke()
        fill(192)
        ellipse(self.pos_x, self.pos_y,self.radius,self.radius)
        fill(255)
        ellipse(self.pos_x-2, self.pos_y-2,9,9)
         
