import pygame
from pygame.math import *


#keys pressed
w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False

m1_pressed = False
m2_pressed = False

#other variables
screen = pygame.display.set_mode((1500 , 1000), 0)
framerate = 5

mouse_pos = 0
mouse_direction = Vector2()

terrain = []
terrain_hitbox = []

enemies = []
enemies_hitbox = []

sprites = []
animations = []
attacks = []



class collisionbox():
    def __init__(self, size, position, image, friction):
        self.size = size
        self.friction = friction
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(0, 0)
        self.image = image
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rotation = 0
        self.hitbox = 0
        self.hitbox = pygame.Rect(position, (self.size, self.size))    
        self.position = Vector2(self.hitbox.x, self.hitbox.y)
        sprites.append(self)

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
            

class animation():
    def __init__(self, spiresheet, frame_size, frames, size):
        self.frame_size = frame_size
        self.position = Vector2(0,0)
        self.rotation = 0
        self.size = size

        self.current_frame = 0
        self.frame_number = frames
        self.is_playing = False

        self.animation = []
        for i in range(frames):
            frame_rect = pygame.Rect(0, frame_size * i, frame_size, frame_size)
            frame = spiresheet.subsurface(frame_rect).copy()
            frame = pygame.transform.scale(frame, (size, size))
            self.animation.append(frame)
        
    def play(self, position, rotation):
        self.position = position
        self.rotation = rotation
        self.is_playing = True
        if not self in animations:
            animations.append(self)


class attack():
    def __init__(self, animation, duration, hitbox, attacker, targets, targets_hitbox, cooldown):
        self.animation = animation
        self.time_left = duration
        self.duration = 0
        self.hitbox = hitbox
        self.target_hitboxes = targets_hitbox
        self.attacker = attacker
        self.enemies = targets
        self.cooldown = cooldown

    def attack(self):
        if self.attacker.cooldown <= 0:
            self.attacker.cooldown = self.cooldown
            self.animation.play()
            attacks.append(self)


class players(collisionbox):
    def __init__(self,  size, position, image, friction, speed, max_range, screen, max_fuel, fuel_regen, fuel_usage):
        super().__init__(size, position, image, friction)
        
        #grappling properties
        self.is_grappling = False
        self.max_grapple_range = max_range
        self.grapple_range = 0
        self.grapple_position = Vector2(400, 400)

        #visual properties
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.screen = screen
        self.boost_anim = animation(pygame.image.load("animation/ODM_boste.png").convert_alpha(), #spritesheet
                                    16, #frame size
                                    8, #number of frames
                                    self.size #size
                                    )
        
        #attack properties
        slash_anim = animation(
            pygame.image.load("animation/player_attack.png").convert_alpha(), #spritesheet
            32, #frame dimensioner
            10, #antal frames
            self.size #skalering
        )
    #    self.slash = attack(
     #       slash_anim,
     #       10 * framerate,
#
    #   )
        self.is_attacking = False

        #boosting properties
        self.is_boosting = False
        self.boost_speed = speed
        self.fuel = max_fuel
        self.max_fuel = max_fuel
        self.fuel_regen = fuel_regen
        self.fuel_usage = fuel_usage

    def boost(self):

        if self.fuel > self.fuel_usage:
            if w_pressed:
                self.is_boosting = True
                self.boost_anim.play(Vector2(self.position.x + self.size/2, self.position.y + self.size), 180)
                self.velocity.y -= self.boost_speed

            if a_pressed:
                self.is_boosting = True
                self.boost_anim.play(Vector2(self.position.x + self.size, self.position.y + self.size/2), -90)
                self.velocity.x -= self.boost_speed

            if  s_pressed:
                self.is_boosting = True
                self.boost_anim.play(Vector2(self.position.x + self.size/2, self.position.y), 0)
                self.velocity.y += self.boost_speed

            if d_pressed:
                self.is_boosting = True
                self.boost_anim.play(Vector2(self.position.x, self.position.y + self.size/2), 90)
                self.velocity.x += self.boost_speed
            
        if not (w_pressed or a_pressed or s_pressed or d_pressed):
            self.is_boosting = False

        if self.is_boosting and self.fuel > self.fuel_usage:
            self.fuel -= self.fuel_usage
        elif not self.is_boosting and self.fuel < self.max_fuel:
            self.fuel += self.fuel_regen


    def grapple_point(self, mouse_dir, bodies):
        self.is_grappling = True

        grapple_start = tuple(self.hitbox.center)
        grapple_end = tuple((mouse_dir * self.max_grapple_range) + self.position)

        #global new_grapple_position
        new_grapple_position = False

        for body in terrain_hitbox:
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
    
    def damage(self):
        print("YOU DIED")
 


class titan(collisionbox):
    def __init__(self, size, position, image):
        super().__init__(size, position, image)



