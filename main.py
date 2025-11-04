import pygame
from pygame.math import *
import config
from config import players




pygame.init()

screen = pygame.display.set_mode((1000 , 600), 0)

width, height = screen.get_size()



player = players("rect", 20, 100, 100, 0.1, 0.1)

#print(player.direction.angle_to(Vector2(1,1)))



running = True
while running:   
    screen.fill((0, 0, 0))
    player.direction = player.velocity.normalize()

    print("vx: ", player.velocity.x)
    print("vy: ", player.velocity.y)
    
    
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
    

    if config.w_pressed and player.velocity.y > -player.max_speed:
        print("w")
        player.velocity.y -= player.acceleration

    if config.a_pressed and player.velocity.x > -player.max_speed:
        player.velocity.x -= player.acceleration
        print("a")

    if config.s_pressed and player.velocity.y < player.max_speed:
        player.velocity.y += player.acceleration
        print("s")

    if config.d_pressed and player.velocity.x < player.max_speed:
        player.velocity.x += player.acceleration
        print("d")



    player.position.x += player.velocity.x
    player.position.y += player.velocity.y
    pygame.draw.rect(screen, (0, 255, 0), (player.position.x, player.position.y, player.size, player.size))
    
        
    pygame.display.flip()
    

pygame.quit()