import pygame
from pygame.math import *


class collisionbox():
    def __init__(self, area_type, size, position_x, position_y):
        self.area_type = area_type
        self.size = size
        self.position = Vector2(position_x, position_y)
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(0, 0)



class players(collisionbox):
    def __init__(self, area_type,  size, position_x, position_y, speed, max_range):
        super().__init__(area_type, size, position_x, position_y)
        self.boost_speed = speed
        self.is_grappling = False
        self.max_grapple_range = max_range




#keys pressed
w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False

mouse_pos = 0
mouse_x = 0
mouse_y = 0
m1_pressed = False
m2_pressed = False

#other variables
