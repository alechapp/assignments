import random
class Brick:
    def __init__(self, pos_x, pos_y, w, h):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.w = w
        self.h = h
        self.active = True
        self.right = self.pos_x + self.w
        self.bottom = self.pos_y + self.h

    def hit_test(self, ballx, bally):
        if self.pos_x < ballx < self.right and self.pos_y < bally < self.bottom :
            return False

    def draw(self):
        if self.active and self.pos_x < 270:
            fill(227,33,11)
            rect(self.pos_x, self.pos_y, 40, 15, 7)
        if self.active and self.pos_x > 270:
            fill(27,127,228)
            rect(self.pos_x, self.pos_y, 40, 15, 7)
