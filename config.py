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
        self.hitbox.x = self.position.x - self.size/2
        self.hitbox.y = self.position.y = self.size/2

    def collide(self, body):
        # AABB resolution: if hitboxes overlap, push `self` out along the smallest penetration axis.
        if not hasattr(self, "hitbox") or not hasattr(body, "hitbox"):
            return
        if not self.hitbox.colliderect(body.hitbox):
            return

        # centers and delta
        self_c = Vector2(self.hitbox.center)
        body_c = Vector2(body.hitbox.center)
        delta = self_c - body_c

        # half extents
        half_w = (self.hitbox.width + body.hitbox.width) * 0.5
        half_h = (self.hitbox.height + body.hitbox.height) * 0.5

        overlap_x = half_w - abs(delta.x)
        overlap_y = half_h - abs(delta.y)

        if overlap_x <= 0 or overlap_y <= 0:
            return

        # resolve along smallest overlap (prevents corner-sticking)
        if overlap_x < overlap_y:
            # resolve horizontally
            if delta.x > 0:
                self.position.x += overlap_x
            else:
                self.position.x -= overlap_x
            self.velocity.x = 0
        else:
            # resolve vertically
            if delta.y > 0:
                self.position.y += overlap_y
            else:
                self.position.y -= overlap_y
            self.velocity.y = 0

        # keep hitbox synced with logical position
        self.hitbox.center = (int(self.position.x), int(self.position.y))


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