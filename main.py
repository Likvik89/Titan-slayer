import pygame
from pygame.math import *
import config
from config import players


pygame.init()

screen = pygame.display.set_mode((1000 , 600), 0)

width, height = screen.get_size()



player = players("rect", #areatype
                 20, #size
                 100, #start position_x
                 100, #start position_y
                 0.5, #boost_speed
                 200 #max grapple range
                 )

#player_img = pygame.image.load("img/player.png").convert_alpha()
#player_img = pygame.transform.scale(player_img, (200, 150))

grapple_position = Vector2(200, 200)

def boost():
    if config.w_pressed:
        player.velocity.y -= player.boost_speed

    if config.a_pressed:
        player.velocity.x -= player.boost_speed

    if config.s_pressed:
        player.velocity.y += player.boost_speed

    if config.d_pressed:
        player.velocity.x += player.boost_speed

def looP():
    if player.position.x < 0:
        player.position.x = width - player.size
    if player.position.x > width - player.size:
        player.position.x = 0
    if player.position.y < 0:
        player.position.y = height - player.size
    if player.position.y > height - player.size:
        player.position.y = 0

def grapple(x, y):
    grapple_position = Vector2(x, y)



clock = pygame.time.Clock()
running = True
while running:   
    screen.fill((0, 0, 0))

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            config.mouse_pos = pygame.mouse.get_pos()  
            config.mouse_x, config.mouse_y = pygame.mouse.get_pos()
            grapple()
    

    boost()
    #looP()

    if player.position.distance_to(grapple_position) > player.max_grapple_range:
        grapple_vector = player.position - grapple_position

        player.direction = Vector2(-grapple_vector.y, grapple_vector.x).normalize() #sætter retningen til at være retvinklet med snoren

        player.direction = player.direction * player.velocity.length()

        #player.velocity = player.direction




    if player.velocity.length() != 0:
        player.direction = player.velocity.normalize()
    
    player.position += player.velocity
    pygame.draw.rect(screen, (0, 255, 0), (player.position.x, player.position.y, player.size, player.size))


    
    pygame.display.flip()
    clock.tick(60)
    

pygame.quit()