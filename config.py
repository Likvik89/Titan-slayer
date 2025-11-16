import pygame
from pygame.math import *


class collisionbox():
    def __init__(self, area_type, size, position_x, position_y, image, friction):
        self.areatype = area_type
        self.size = size
        self.friction = friction
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(0, 0)
        self.image = image
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rotation = 0
        self.hitbox = 0
        if area_type == "rect":
            self.hitbox = pygame.Rect((position_x, position_y), (self.size, self.size))
        
        self.position = Vector2(self.hitbox.x, self.hitbox.y)

    def collide(self, body):
        self_center = Vector2(self.position.x + self.size/2, self.position.y + self.size/2)
        body_center = Vector2(body.position.x + body.size/2, body.position.y + body.size/2)
        retning = self_center - body_center
        vinkel = list(retning.as_polar())[1]

        if vinkel > -45 and vinkel < 45: #body er til venstre for self
            self.velocity.x = 0
            self.velocity *= body.friction
            self.position.x = body.position.x + body.size #skubber self væk

        if vinkel < -135 or vinkel > 135: #body er til højre for self
            self.velocity.x = 0
            self.velocity *= body.friction
            self.position.x = body.position.x - self.size #skubber self væk
        
        if vinkel > 45 and vinkel < 135: #body er over self
            self.velocity.y = 0
            self.velocity *= body.friction
            self.position.y = body.position.y + body.size #skubber self væk

        if vinkel < -45 and vinkel > -135: #body er under self
            self.velocity.y = 0
            self.velocity *= body.friction
            self.position.y = body.position.y - self.size #skubber self væk
            
        
        



class players(collisionbox):
    def __init__(self, area_type,  size, position_x, position_y, image, friction, speed, max_range, turnspeed):
        super().__init__(area_type, size, position_x, position_y, image, friction)
        self.boost_speed = speed
        self.is_grappling = False
        self.max_grapple_range = max_range
        self.grapple_range = 0
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.turnspeed = turnspeed
        self.grapple_position = Vector2(400, 400)

    def boost(self):
        if w_pressed:
            self.velocity.y -= self.boost_speed

        if a_pressed:
            self.velocity.x -= self.boost_speed

        if  s_pressed:
            self.velocity.y += self.boost_speed

        if d_pressed:
            self.velocity.x += self.boost_speed

    def grapple_point(self, mouse_dir, mouse_position, terrain_):
        self.is_grappling = True

        grapple_start = tuple(map(int, self.hitbox.center))
        grapple_end = tuple(map(int, (mouse_dir * self.max_grapple_range) + self.position))

        grapple_vector = Vector2(Vector2(grapple_end) - self.position)
        #self.grapple_range = grapple_vector.length()

        global new_grapple_position
        new_grapple_position = False
        
        for body in terrain_:
            clipped_grapple_vector = body.clipline(grapple_start, grapple_end) #den del af snoren der overlapper terrain

            if (not clipped_grapple_vector): #snoren overlapper ikke terrain
                continue

            point, point2 = clipped_grapple_vector #start og slut af den klippede vector
            point = Vector2(point) #starten er altid tættest på

            self.grapple_position = point #grapple position sættes til kanten af terrænget
            new_grapple_position = point 
            self.grapple_range = (point - self.position).length() +10
        
        #tjekker om der er fundet et nyt validt grapplepunkt
        if not new_grapple_position:
            self.is_grappling = False
 


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
mouse_direction = Vector2()

last_viewing_angle = 0

terrain = []
terrain_hitbox = []