import pygame
from pygame.math import *
import config
from config import players




pygame.init()

screen = pygame.display.set_mode((1000 , 600), 0)

width, height = screen.get_size()



player = players("rect", 20, 100, 100, 0.1, 0.01)

#player_img = pygame.image.load("img/player.png").convert_alpha()
#player_img = pygame.transform.scale(player_img, (200, 150))



#print(player.direction.angle_to(Vector2(1,1)))



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
            mouse_pos = pygame.mouse.get_pos()  
            mouse_x, mouse_y = pygame.mouse.get_pos()
    

    sped = 1
    if config.w_pressed:
        player.direction.y -= sped

    if config.a_pressed:
        player.direction.x -= sped

    if config.s_pressed:
        player.direction.y += sped

    if config.d_pressed:
        player.direction.x += sped


    player.velocity = player.direction.normalize() * 0.1
    player.position.x += player.velocity.x
    player.position.y += player.velocity.y
    pygame.draw.rect(screen, (0, 255, 0), (player.position.x, player.position.y, player.size, player.size))
    #print(player.position.x)
    #print(player.position.y)
    
        
    pygame.display.flip()
    

pygame.quit()