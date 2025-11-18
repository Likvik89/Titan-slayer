import pygame
from pygame.math import *
import config
from config import *
import math


pygame.init()


width, height = config.screen.get_size()

time = 0


player = players(
                 40, #size
                 (200, 300), #start position
                 pygame.image.load("img/player.png").convert_alpha(), #image
                 0.5, #friction
                 1/8, #boost_speed
                 300, #max grapple range
                 config.screen,
                 100, #maxfuel
                 1, #fuel recharge
                 1  #fuel consumption
                 )


def inputs():
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
                player.grapple_point(config.mouse_direction, terrain_hitbox)


            
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
            player.grapple_point(config.mouse_direction, terrain_hitbox)


        elif event.type == pygame.MOUSEBUTTONUP:
            player.is_grappling = False
           

def collision():
    body_index = player.hitbox.collidelist(config.terrain_hitbox)

    if body_index != -1:

        body = config.terrain[body_index]

        player.collide(body)


def generate_terrain():
    global pillar


    pillar = collisionbox(
                          200,#size
                          (500, 500), #position
                          pygame.image.load("img/pillar_5.png").convert_alpha(), #image
                          0.5 #friction
                        )
    
    config.terrain_hitbox.append(pillar.hitbox)
    config.terrain.append(pillar)

generate_terrain()

def animate():

    for animation in config.animations:
        draw(animation.animation[animation.current_frame], animation.frame_size, animation.position, animation.rotation)
        if time == config.framerate:
            animation.current_frame += 1
        if animation.current_frame >= animation.frame_number:
            animation.is_playing = False
            animation.current_frame = 0
            config.animations.remove(animation)
            

    for image in config.sprites:
        draw(image.image, image.size, image.position, image.rotation)    

    #grappling hook
    if player.is_grappling:
        pygame.draw.line(config.screen, string_color, (player.position.x + player.size/2, player.position.y + player.size/2), player.grapple_position, 1)    
    pygame.draw.circle(config.screen, (255, 0, 255), player.position, player.max_grapple_range, 1)



def draw(image, size, position, rotation):
    rotated = pygame.transform.rotate(image, rotation)
    rot_rect = rotated.get_rect(center=(position.x + size/2, position.y + size/2))
    config.screen.blit(rotated, rot_rect.topleft)



clock = pygame.time.Clock()
running = True
while running:   
    config.screen.fill((0, 0, 0))
    time += 1


    grapple_vector = player.grapple_position - player.position
    config.mouse_pos = Vector2(pygame.mouse.get_pos())
    config.mouse_direction = Vector2(config.mouse_pos - player.position).normalize()
    
    if player.velocity.length() != 0:
        player.direction = player.velocity.normalize()
    

    inputs()
    

    string_color = (0, 255, 0) #grøn

    if (player.position.distance_to(player.grapple_position) > player.grapple_range) and player.is_grappling and player.velocity != [0,0]: #spiller grappler og er længere væk end grapple_range


        string_color = (255, 0, 0) #rød

        #Roterer vektorerne, så vinklen mellem dem er ens, men player.velocity er vandret
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
            velocity = -Vector2(-grapple_vector.y, grapple_vector.x).normalize() #sætter hastigheden vinkelret på snoren
            
        if grapple.y < 0:
            velocity = Vector2(-grapple_vector.y, grapple_vector.x).normalize() #sætter hastigheden vinkelret på snoren

        
        velocity = velocity * player.velocity.length() * sinv
        player.velocity = velocity

    
    player.boost()
    collision()

    player.position += player.velocity
    player.hitbox.x = player.position.x
    player.hitbox.y = player.position.y
    player.rotation = -(config.mouse_direction).as_polar()[1] - 90  

    
    animate()


    if time >= config.framerate:
        time = 0
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()