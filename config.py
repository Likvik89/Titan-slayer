import pygame
from pygame.math import *


class collisionbox():
    def __init__(self, area_type, size, position_x, position_y, image):
        self.size = size
        self.position = Vector2(position_x, position_y)
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(0, 0)
        self.image = image
        self.rotation = 0
        self.hitbox = 0
        if area_type == "rect":
            self.hitbox = pygame.Rect(self.position.x, self.position.y, self.size, self.size)




class players(collisionbox):
    def __init__(self, area_type,  size, position_x, position_y, image, speed, max_range, turnspeed):
        super().__init__(area_type, size, position_x, position_y, image)
        self.boost_speed = speed
        self.is_grappling = False
        self.max_grapple_range = max_range
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.turnspeed = turnspeed

    def boost(self):
        if w_pressed:
            self.velocity.y -= self.boost_speed

        if a_pressed:
            self.velocity.x -= self.boost_speed

        if  s_pressed:
            self.velocity.y += self.boost_speed

        if d_pressed:
            self.velocity.x += self.boost_speed

class titan(collisionbox):
    def __init__(self, area_type, size, position_x, position_y, image):
        super().__init__(area_type, size, position_x, position_y, image)


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
grapple_position = Vector2(400, 400)
mouse_direction = Vector2()

last_viewing_angle = 0
