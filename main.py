import pygame
from pygame.math import *
import config
from config import *
import math


pygame.init()

screen = pygame.display.set_mode((1500 , 1000), 0)

width, height = screen.get_size()



player = players("rect", #areatype
                 40, #size
                 200, #start position_x
                 300, #start position_y
                 pygame.image.load("img/player.png").convert_alpha(), #image
                 1/8, #boost_speed
                 300, #max grapple range
                 20 # turnspeed
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
                player.grapple_point(config.mouse_pos, terrain_hitbox)

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
            player.grapple_point(config.mouse_pos, terrain_hitbox)
            player.is_grappling = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            player.is_grappling = False


lastangle = 0
def rotate():
    player.rotation = -(config.mouse_direction).as_polar()[1] - 90         


def collision():
    body_index = player.hitbox.collidelist(config.terrain_hitbox)

    if body_index != -1:

        body = config.terrain[body_index]

        player.collide(body)



def generate_terrain():
    global pillar

    pillar = collisionbox("rect",
                      300,#size
                      500, #start x
                      500, #start y
                      pygame.image.load("img/pillar_5.png").convert_alpha() #image
                        )
    
    config.terrain_hitbox.append(pillar.hitbox)
    config.terrain.append(pillar)

generate_terrain()

time = 0

clock = pygame.time.Clock()
running = True
while running:   
    screen.fill((222, 222, 222))
    time += 1


    grapple_vector = player.grapple_position - player.position
    config.mouse_pos = Vector2(pygame.mouse.get_pos())
    config.mouse_direction = Vector2(config.mouse_pos - player.position).normalize()
    
    if player.velocity.length() != 0:
        player.direction = player.velocity.normalize()
    

    inputs()
    

    string_color = (0, 255, 0) #grøn

    if (player.position.distance_to(player.grapple_position) > player.max_grapple_range) and player.is_grappling and player.velocity != [0,0]:

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

    

    if player.is_grappling:
        pygame.draw.line(screen, string_color, (player.position.x + player.size/2, player.position.y + player.size/2), player.grapple_position, 1)
    #if player.velocity != [0,0]:
     #   pygame.draw.line(screen, (0, 0, 255), (player.position.x + player.size/2, player.position.y + player.size/2), (Vector2(player.position.x + player.size/2, player.position.y + player.size/2) + player.velocity*20 ), 1)
    
    rotate()
    
    rotated = pygame.transform.rotate(player.image, player.rotation)
    rot_rect = rotated.get_rect(center=(player.position.x + player.size/2, player.position.y + player.size/2))
    pygame.draw.rect(screen, (0, 255, 0), player.hitbox)
    
    screen.blit(rotated, rot_rect.topleft)
    

    pygame.draw.circle(screen, (255, 0, 255), player.position, player.max_grapple_range, 1)
    pygame.draw.rect(screen, (0, 0, 0), pillar.hitbox, width=0)
    screen.blit(pillar.image, (pillar.position.x , pillar.position.y))

    config.last_viewing_angle = player.rotation

    if time >= 10:
        time = 0
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()