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

    string_color = (0, 255, 0) #green

    if (player.position.distance_to(grapple_position) > player.max_grapple_range) and player.is_grappling:

        string_color = (255, 0, 0) #rød

        grapple_vector =  grapple_position - player.position

        #lastangle = angle


        #cos(v) = (a*b)/(lena*lenb)
        if player.velocity != [0,0]:
            lena = grapple_vector.length()

            lenb = player.velocity.length()
            dp = player.velocity.dot(grapple_vector)


            if player.wish_direction != [0,0]:
                lenb = player.wish_direction.length()
                dp = player.wish_direction.dot(grapple_vector)

            cosv = dp/(lena * lenb)

            angle = math.acos(cosv)
            angle = math.degrees(angle)
            
            if time == 10:
                print()
                print(angle)
                print(player.position)
                print()
                

        if angle > 180:
            player.direction = -Vector2(-grapple_vector.y, grapple_vector.x).normalize()
            #print("left")

        
        elif angle < 181:
            player.direction = Vector2(-grapple_vector.y, grapple_vector.x).normalize()
            #print("right")
        
        player.direction = player.direction * player.velocity.length()



        player.velocity = player.direction




    player.position += player.velocity
    
    if player.is_grappling:
        pygame.draw.line(screen, string_color, (player.position.x + player.size/2, player.position.y + player.size/2), grapple_position, 1)
        #player.position = (new_grapple_vector.normalize() * player.max_grapple_range) + grapple_position

    pygame.draw.rect(screen, (0, 255, 0), (player.position.x, player.position.y, player.size, player.size))
    
    if player.wish_direction != [0,0]:
        pygame.draw.line(screen, (255, 255, 0), (player.position.x + player.size/2, player.position.y + player.size/2), (Vector2(player.position.x + player.size/2, player.position.y + player.size/2) + player.wish_direction.normalize()*88 ), 1)

    if time >= 10:
        time = 0
    
    pygame.display.flip()
    clock.tick(60)
    

pygame.quit()