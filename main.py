import pygame
from pygame.math import *
import config
from config import players
import math


pygame.init()

screen = pygame.display.set_mode((1400 , 800), 0)

width, height = screen.get_size()



player = players("rect", #areatype
                 50, #size
                 200, #start position_x
                 300, #start position_y
                 pygame.image.load("img/player.png").convert_alpha(), #image
                 1/8, #boost_speed
                 300, #max grapple range
                 20 # turnspeed
                 )
player.orig_image = player.image.copy()



time = 0

clock = pygame.time.Clock()
running = True
while running:   
    screen.fill((0, 0, 0))
    time += 1


    grapple_vector = config.grapple_position - player.position
    config.mouse_pos = Vector2(pygame.mouse.get_pos())
    config.mouse_direction = Vector2(config.mouse_pos - player.position)
    


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
            
            if event.key == pygame.K_SPACE:
                config.grapple_position = config.mouse_pos
                player.is_grappling = True


            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                config.w_pressed = False
            elif event.key == pygame.K_s:
                config.s_pressed = False
            elif event.key == pygame.K_a:
                config.a_pressed = False
            elif event.key == pygame.K_d:
                config.d_pressed = False
            elif event.key == pygame.K_SPACE:
                player.is_grappling = False
            

        if event.type == pygame.MOUSEBUTTONDOWN:
            config.grapple_position = config.mouse_pos
            player.is_grappling = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            player.is_grappling = False
        
    
    
    

    string_color = (0, 255, 0) #grøn

    if (player.position.distance_to(config.grapple_position) > player.max_grapple_range) and player.is_grappling and player.velocity != [0,0]:

        string_color = (255, 0, 0) #rød

        #Roterer vektorerne, så vinkeln mellem dem er ens, men player.velocity er vandret
        velocity = player.velocity.rotate(-list(player.velocity.as_polar())[1])
        grapple = grapple_vector.rotate(-list(player.velocity.as_polar())[1])

        #Beregner vinklen mellem vektorerne
        leng = grapple.length()
        lenv = (velocity).length()
        dp = grapple.dot(velocity)
        cosv = dp/(lenv*leng)
        cosv = max(-1.0, min(1.0, cosv))
        sinv = math.sin(math.acos(cosv))

        if grapple.y > 0:
            velocity = -Vector2(-grapple_vector.y, grapple_vector.x).normalize()
            
        if grapple.y < 0:
            velocity = Vector2(-grapple_vector.y, grapple_vector.x).normalize()
        
        velocity = velocity * player.velocity.length() * sinv
        player.velocity = velocity


    player.boost()
    player.position += player.velocity

    if player.is_grappling:
        pygame.draw.line(screen, string_color, (player.position.x + player.size/2, player.position.y + player.size/2), config.grapple_position, 1)

    if player.velocity != [0,0]:
        pygame.draw.line(screen, (0, 0, 255), (player.position.x + player.size/2, player.position.y + player.size/2), (Vector2(player.position.x + player.size/2, player.position.y + player.size/2) + player.velocity*20 ), 1)

    
    
    if player.velocity.length_squared() > 1e-8:

        leng = grapple_vector.length()
        lenmd = (config.mouse_direction).length()
        dp = grapple_vector.dot(config.mouse_direction)
        cosv = dp/(lenmd*leng)
        cosv = max(-1.0, min(1.0, cosv))
        player.rotation = math.acos(cosv)
        player.rotation = math.degrees(player.rotation) -180

        if player.is_grappling:

            if player.rotation > 90:
                player.rotation = grapple_vector.as_polar()[1]
            
            if player.rotation < -90:
                player.rotation = grapple_vector.as_polar()[1]

        
        player.rotation = -(config.mouse_direction).as_polar()[1] - 90
 

        print("current angle: ", player.rotation)
        print("last angle: ", config.last_viewing_angle)
        if player.rotation - config.last_viewing_angle > player.turnspeed:
            player.rotation = config.last_viewing_angle + player.turnspeed
            print("right")

        if player.rotation - config.last_viewing_angle < -player.turnspeed:
            player.rotation = config.last_viewing_angle - player.turnspeed
            print("left")

    else:
        player.rotation = 0.0
    


    rotated = pygame.transform.rotate(player.orig_image, player.rotation)
    rot_rect = rotated.get_rect(center=(player.position.x + player.size/2, player.position.y + player.size/2))
    screen.blit(rotated, rot_rect.topleft)

    config.last_viewing_angle = player.rotation


    if time >= 10:
        time = 0
    
    pygame.display.flip()
    clock.tick(60)



pygame.quit()