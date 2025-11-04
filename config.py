import pygame
from pygame.math import *


class collisionbox():
    def __init__(self, area_type, size, position_x, position_y):
        self.area_type = area_type
        self.size = size
        self.position = Vector2(position_x, position_y)
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(0.00001, 0.00001)



class players(collisionbox):
    def __init__(self, area_type,  size, position_x, position_y, maxspeed, speed):
        super().__init__(area_type, size, position_x, position_y)
        self.boost_speed = speed
        self.max_speed = maxspeed


#keys pressed:
 
w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False