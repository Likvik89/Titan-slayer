import pygame
from pygame.math import *
import config
from config import players
import math


pygame.init()

screen = pygame.display.set_mode((1400 , 800), 0)

width, height = screen.get_size()



player = players("rect", #areatype
                 20, #size
                 200, #start position_x
                 300, #start position_y
                 1/8, #boost_speed
                 300 #max grapple range
                 )

#player_img = pygame.image.load("img/player.png").convert_alpha()
#player_img = pygame.transform.scale(player_img, (200, 150))

grapple_position = Vector2(400, 400)
new_grapple_vector = Vector2()

def boost():
    if config.w_pressed:
        player.velocity.y -= player.boost_speed
        player.wish_direction.y -= player.boost_speed
        

    if config.a_pressed:
        player.velocity.x -= player.boost_speed
        player.wish_direction.x -= player.boost_speed

    if config.s_pressed:
        player.velocity.y += player.boost_speed
        player.wish_direction.y += player.boost_speed

    if config.d_pressed:
        player.velocity.x += player.boost_speed
        player.wish_direction.x += player.boost_speed



def looP():
    if player.position.x < 0:
        player.position.x = width - player.size
    if player.position.x > width - player.size:
        player.position.x = 0
    if player.position.y < 0:
        player.position.y = height - player.size
    if player.position.y > height - player.size:
        player.position.y = 0


angle = 0
lastangle = 0
time = 0

clock = pygame.time.Clock()
running = True
while running:   
    screen.fill((0, 0, 0))
    time += 1

    player.wish_direction = Vector2(0,0)

    if player.velocity.length() != 0:
        player.direction = player.velocity.normalize()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Press ESC to exit fullscreen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_w:  
                config.w_pressed = True


            if event.key == pygame.K_s:  
                config.s_pressed = True


            if event.key == pygame.K_a:  
                config.a_pressed = True


            if event.key == pygame.K_d:  
                config.d_pressed = True


            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                config.w_pressed = False
            elif event.key == pygame.K_s:
                config.s_pressed = False
            elif event.key == pygame.K_a:
                config.a_pressed = False
            elif event.key == pygame.K_d:
                config.d_pressed = False
            

        if event.type == pygame.MOUSEBUTTONDOWN:
            config.mouse_pos = pygame.mouse.get_pos()  
            config.mouse_x, config.mouse_y = pygame.mouse.get_pos()
            grapple_position = Vector2(config.mouse_pos)
            player.is_grappling = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            player.is_grappling = False
        
    
    boost()
    #looP()

    # compute vector from grapple to player once
    delta = player.position - grapple_position
    dist = delta.length()

    # string color and range handling
    string_color = (0, 255, 0)
    if player.is_grappling and dist > player.max_grapple_range:
        string_color = (255, 0, 0)

        # clamp position to the rope circle (soft / gradual correction)
        if dist > 0:
            normal = delta.normalize()            # outward normal from grapple -> player
            overlap = dist - player.max_grapple_range

            # SOFT POSITION CORRECTION: move a fraction of the overlap so it's not an instant teleport
            softness = 0.2          # 0 < softness <= 1 (smaller = softer)
            player.position -= normal * (overlap * softness)

            # PRESERVE TANGENTIAL VELOCITY: split velocity into radial and tangential parts
            radial_speed = player.velocity.dot(normal)
            radial = normal * radial_speed
            tangential = player.velocity - radial

            # If radial component points outward, damp it instead of zeroing it
            if radial_speed > 0:
                radial *= 0.2     # keep a small fraction of outward radial velocity (0 = kill, 1 = keep)
            # else if radial_speed <= 0 it's inward and we can keep it (or damp less)

            player.velocity = tangential + radial

            # small global damping to remove residual oscillation (tweak value)
            player.velocity *= 0.995
        


    player.position += player.velocity
    
    if player.is_grappling:
        pygame.draw.line(screen, string_color, (player.position.x + player.size/2, player.position.y + player.size/2), grapple_position, 1)
        #player.position = (new_grapple_vector.normalize() * player.max_grapple_range) + grapple_position

    pygame.draw.rect(screen, (0, 255, 0), (player.position.x, player.position.y, player.size, player.size))
    
    # draw wish direction only if nonzero
    if player.wish_direction.length_squared() != 0:
        pygame.draw.line(screen, (255, 255, 0), (player.position.x + player.size/2, player.position.y + player.size/2), (Vector2(player.position.x + player.size/2, player.position.y + player.size/2) + player.wish_direction.normalize()*88 ), 1)

    if time >= 10:
        time = 0
    
    pygame.display.flip()
    clock.tick(60)
    

pygame.quit()