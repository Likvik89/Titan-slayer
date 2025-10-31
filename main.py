import pygame
from pygame.math import *
import config




pygame.init()

screen = pygame.display.set_mode((1000 , 600), 0)

width, height = screen.get_size()



player = players("rect", 20, 10, 10)



screen.fill((0, 0, 0))

running = True
while running:   

    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Press ESC to exit fullscreen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:  
                w_pressed = True
            if event.key == pygame.K_s:  
                s_pressed = True
            if event.key == pygame.K_a:  
                a_pressed = True
            if event.key == pygame.K_d:  
                d_pressed = True

            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                w_pressed = False
            elif event.key == pygame.K_s:
                s_pressed = False
            elif event.key == pygame.K_a:
                a_pressed = False
            elif event.key == pygame.K_d:
                d_pressed = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  
            mouse_x, mouse_y = pygame.mouse.get_pos()
    

    #pygame.draw.rect(screen, (0, 255, 0), (player.x, player.y, player.size, player.size))
    
        
    pygame.display.flip()
    

pygame.quit()