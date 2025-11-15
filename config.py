import pygame
from pygame.math import *


class collisionbox():
    def __init__(self, area_type, size, position_x, position_y, image):
        self.areatype = area_type
        self.size = size
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(0, 0)
        self.image = image
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rotation = 0
        self.hitbox = 0
        if area_type == "rect":
            self.hitbox = pygame.Rect((position_x, position_y), (self.size, self.size))
        
        if area_type == "circle":
            self.hitbox = pygame
        
        self.position = Vector2(self.hitbox.x, self.hitbox.y)
        #self.hitbox.x = self.position.x - self.size/2
        #self.hitbox.y = self.position.y = self.size/2

    def collide(self, body):
        self_center = Vector2(self.hitbox.x + self.size/2, self.hitbox.y + self.size/2)
        body_center = Vector2(body.hitbox.x + body.size/2, body.hitbox.y + body.size/2)
        retning = self_center - body_center
        vinkel = list(retning.as_polar())[1]
        print(vinkel)

        if vinkel > -45 and vinkel < 45: #body er til venstre for self
            self.velocity.x = 0
            self.position.x = body.position.x + body.size

        if vinkel < -135 or vinkel > 135: #body er til højre for self
            self.velocity.x = 0
            self.position.x = body.position.x - self.size
        
        if vinkel > 45 and vinkel < 135: #body er over self
            self.velocity.y = 0
            self.position.y = body.position.y + body.size

        if vinkel < -45 and vinkel > -135: #body er under self
            self.velocity.y = 0
            self.position.y = body.position.y - self.size
            
        
        



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


def clamp(value, floor, celing):
    return max(floor, min(celing, value))

def angle_between():
    pass


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

terrain = []
terrain_hitbox = []