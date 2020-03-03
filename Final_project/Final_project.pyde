class Ball:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_x = 0
        self.speed_y = 0
        self.radius = 5
        
    def update(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        
    def draw(self):
        noStroke()
        fill(128, 128, 128)
        circle(self.pos_x, self.pos_y, 10)
        fill(192, 192, 192)
        circle(self.pos_x - 1, self.pos_y - 1, 2*self.radius)
        
    def hit_test(self, x, y):
    # Returns true if the coordinate x, y is within the ball.
        return (self.pos_x - x) ** 2 + (self.pos_y - y) ** 2 < self.radius ** 2
        

class Brick:
    def __init__(self, pos_x, pos_y, w, h, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.w = w
        self.h = h
        self.active = True
        self.color = color
        
    def hit_test(self, x, y):
        return ((x > self.pos_x) and 
                (x < self.pos_x + self.w) and
                (y > self.pos_y) and 
                (y < self.pos_y + self.h))
        
    def draw(self):
        if self.active:
            if self.color == 'r':
                fill(227,33,11)
            elif self.color == 'b':
                fill(27,127,228)
            noStroke()
            rect(self.pos_x, self.pos_y, self.w, self.h)
            

class Paddle:
    def __init__(self, pos_x, pos_y, field_size):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.w = 40
        self.field_size = field_size
        self.circle_size = 10
        
    def update(self, target_x):
        self.pos_x = min(max(target_x, self.w / 2 + self.circle_size), self.field_size - self.circle_size - self.w / 2)
        
    def hit_test(self, x, y):
        if ((x > self.pos_x - self.w / 2 - self.circle_size / 2) and 
            (x < self.pos_x + self.w / 2 + self.circle_size / 2) and
            (y > self.pos_y - self.circle_size/2) and 
            (y < self.pos_y + 20)):
            return True
        return False
            
        
    def draw(self):
        # Draw the paddle
        stroke(0)
        pushMatrix()
        translate(self.pos_x, self.pos_y)
        fill(255, 0, 0)
        circle(-self.w // 2, 0, self.circle_size)
        circle( self.w // 2, 0, self.circle_size)
        fill(128, 128, 128)
        rect(-self.w // 2, -self.circle_size/2, self.w, self.circle_size)
        popMatrix()


marginX = 10
marginY = 16
mode = 'mouse'
dragging = True
nballs_initial = 3
game_state = 'frozen'
state_start_time = 0

def reset_game():
    global game_over, nballs, dragging, bricks
    game_over = False
    nballs = nballs_initial
    dragging = True
    for brick in bricks:
        brick.active = True

def create_brick_layout():
    # Read a level from disk and draw it as a pattern of bricks.
    bricks = []
    lines = []
    f = open('files/bricks.txt')
    for line in f.readlines():
        lines.append(line)
    f.close()
    
    nbricks_wide = len(lines[0]) - 1
    nbricks_high = len(lines)
    
    brick_width = (width - 2 * marginX) / nbricks_wide
    brick_height = brick_width / 2 
    
    for j in range(nbricks_high):
        for i in range(nbricks_wide):
            color = lines[j][i]
            if color != ' ':
                bricks.append(Brick(i * brick_width, j * brick_height, brick_width, brick_height, color))
     
    # For debugging purposes, make one big brick.        
    #bricks = [Brick(0, 0, width - 2 * marginX, 100, 'r')]
    return bricks
    
def setup():
    global bricks, Ball, score_balls, paddle
    size(600, 600)
    
    pos_x = 0
    pos_y = height - 40
    bricks = create_brick_layout()
    
    # Use the Ball class to draw some balls on the score board (trick!).
    score_balls = []
    for i in range(nballs_initial):
        score_balls.append(Ball(i * 10 + 10, 8))
    
    paddle = Paddle(pos_x, pos_y, width - marginX * 2)
    Ball = Ball(pos_x, pos_y - 20)
    
    reset_game()
    frameRate(60)

def draw():
    global game_state, state_start_time, elapsed_time
    new_state = 'null'
    if game_state == 'playing':
        new_state = play_game(True)
    elif game_state == 'frozen':
        new_state = play_game(False)
    elif game_state == 'won' or game_state == 'lost':
        print("in state")
        print(game_state)
        new_state = display_game_over(game_state, elapsed_time)
    elif game_state == 'frozen_prize':
        new_state = prize(False)
    elif game_state == 'prize':
        new_state = prize(True)
    
    if new_state and new_state != game_state:
        game_state = new_state
        elapsed_time = millis() - state_start_time
        state_start_time = millis()

    if game_state == 'frozen_prize' and (millis() - state_start_time) > 500:
        # Unfreeze after 500 milliseconds.
        game_state = 'prize'
        elapsed_time = millis() - state_start_time
        state_start_time = millis()
                        
    if game_state == 'frozen' and (millis() - state_start_time) > 500:
        # Unfreeze after 500 milliseconds.
        game_state = 'playing'
        elapsed_time = millis() - state_start_time
        state_start_time = millis()
        
def play_game(process_inputs):
    global bricks, dragging, Ball, score_balls, nballs, Ball, paddle, mode
    
    background(0)
    # Draw the background frame
    fill(128)
    rect(0, marginY, width, height - marginY)
    noStroke()
    fill(0, 0, 64)
    rect(marginX, marginY, width - 2*marginX, height)
    stroke(255)
    line(0, marginY, width, marginY)

    circle_size = Ball.radius
    field_size = width - 2*marginX
    
    pos_x = paddle.pos_x
    oldpos_x = paddle.pos_x
    
    for brick in bricks:
        if brick.active:
            # Collision detection type 1:
            # Bottom hit detection
            if brick.hit_test(Ball.pos_x, Ball.pos_y - Ball.radius):
                brick.active = False
                Ball.speed_y = -Ball.speed_y
            if brick.hit_test(Ball.pos_x, Ball.pos_y + Ball.radius):
                brick.active = False
                Ball.speed_y = -Ball.speed_y
            if brick.hit_test(Ball.pos_x +Ball.radius, Ball.pos_y):
                brick.active = False
                Ball.speed_x = -Ball.speed_x
            if brick.hit_test(Ball.pos_x -Ball.radius, Ball.pos_y):
                brick.active = False
                Ball.speed_x = -Ball.speed_x
                continue
            
    # Now test the other parts of the ball
                     
            # Collision detection type 2:
            # Bottom right corner
            if Ball.hit_test(brick.pos_x + brick.w, brick.pos_y + brick.h):
                brick.active = False
                Ball.speed_x, Ball.speed_y = -Ball.speed_y, -Ball.speed_x
            if Ball.hit_test(brick.pos_x - brick.w, brick.pos_y - brick.h):
                brick.active = False
                Ball.speed_x, Ball.speed_y = -Ball.speed_y, -Ball.speed_x
            if Ball.hit_test(brick.pos_x, brick.pos_y):
                brick.active = False
                Ball.speed_y, Ball.speed_x = -Ball.speed_y, -Ball.speed_x
            if Ball.hit_test(brick.pos_x , brick.pos_y):
                brick.active = False
                Ball.speed_y, Ball.speed_x = -Ball.speed_y, -Ball.speed_x
                continue
    
    if process_inputs:
        # Process input
        if pmouseX != mouseX or pmouseY != mouseY:
            mode = 'mouse'
            
        if keyPressed:
            mode = 'keyboard'
        
        if mode == 'mouse':
            pos_x = mouseX - marginX
            if mousePressed and dragging:
                Ball.speed_x = 5
                Ball.speed_y = -5
                dragging = False
            
        if mode == 'keyboard':
            if keyPressed and keyCode == LEFT:
                pos_x -= 10
            if keyPressed and keyCode == RIGHT:
                pos_x += 10
            if keyPressed and key == ' ' and dragging:
                Ball.speed_x = 5
                Ball.speed_y = -5
                dragging = False

    paddle.update(pos_x)

    if dragging:
        Ball.pos_x = paddle.pos_x
        Ball.pos_y = paddle.pos_y - 10
        
    Ball.update()
    
    paddle_speed = (paddle.pos_x - oldpos_x)
    
    # Bounce the balls off the walls.
    if Ball.pos_x > width - 2 * marginX - Ball.radius or Ball.pos_x < Ball.radius:
        Ball.speed_x = -Ball.speed_x
  
    if Ball.pos_y < 15:
        Ball.speed_y = -Ball.speed_y
    
    # Paddle hit detection.
    if Ball.speed_y > 0 and paddle.hit_test(Ball.pos_x, Ball.pos_y + Ball.radius-19):
        print("Collided!")
        # Check for collision
        Ball.speed_y = - Ball.speed_y
        
        # add momentum transfer
        Ball.speed_x -= .2 * paddle_speed        

    if Ball.pos_y  >= paddle.pos_y + 20:
        # Remove one ball from play
        dragging = True
        nballs -= 1

    # Draw the bricks, paddle and balls (in that order!).
    pushMatrix()
    translate(marginX, 20)
    score = 0
    ndown = 0
    for j in range(len(bricks)):
        if bricks[j].hit_test(Ball.pos_x, Ball.pos_y):
            bricks[j].active = False
            
        bricks[j].draw()
        if not bricks[j].active:
            ndown += 1
            if bricks[j].color == 'r':
                score += 200
            else:
                score += 100
                
    paddle.draw()
    Ball.draw()
    
    popMatrix()
    
    # Draw some around the score board.
    for i in range(nballs):
        score_balls[i].draw()

    # Draw the score.
    fill(255)
    textAlign(RIGHT)
    text("%d" % score, width - 10, 12)
    textSize(10)
    if ndown == len(bricks):
        # won!
        return 'won'
        
    if nballs <= 0:
        return 'lost'
    
def display_game_over(win_state, elapsed_time):
    global bricks
    textAlign(CENTER)
    fill(255)
    if win_state == 'lost':
        textSize(32)
        fill(255)
        text("Game over :(\n\nClick to continue", width / 2, height/2)
    elif win_state == 'won':
        textSize(32)
        fill(0)
        text("You won in %.1fs!\n\nYou cleared %.1f bricks/seconds\n\nCLICK FOR YOUR PRIZE!!!" % (elapsed_time / 1000.0, elapsed_time / float(len(bricks)) / 1000.0), 
            width/2, height/2)
        textSize(32)
        fill(255)
        text("You won in %.1fs!\n\nYou cleared %.1f bricks/seconds\n\nCLICK FOR YOUR PRIZE!!!" % (elapsed_time / 1000.0, elapsed_time / float(len(bricks)) / 1000.0), 
            (width/2)-1, (height/2)-1)
        
    if mousePressed:
        return 'frozen_prize'
    
    # if keyPressed==True:
    #     reset_game()
    #     return 'frozen'
        
def prize(is_active):
    img = loadImage("img.jpg")
    image(img, -70, -70)
    if is_active and mousePressed:
        reset_game()
        return 'frozen'
      
