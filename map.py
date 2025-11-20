import pygame
import random
import config
from config import *


def generate_terrain():
    global pillar

    i = random.randint(5, 10)
    p = 0


    while p < i:
    
        size = random.randint(100, 200)
        width, height = config.screen.get_size()

        x = random.randint(0, width - size)
        y = random.randint(0, height - size)

        img_number = random.randint(1, 6)
        if img_number == 1:
            img = pygame.image.load("img/pillar_1.png").convert_alpha()
        elif img_number == 2:
            img = pygame.image.load("img/pillar_2.png").convert_alpha()
        elif img_number == 3:
            img = pygame.image.load("img/pillar_3.png").convert_alpha()
        elif img_number == 4:
            img = pygame.image.load("img/pillar_4.png").convert_alpha()
        elif img_number == 5:
            img = pygame.image.load("img/pillar_5.png").convert_alpha()
        else:
            img = pygame.image.load("img/pillar_6.png").convert_alpha()

        pillar = collisionbox(size, (x, y), img, 0.5)

        if pillar.hitbox.collidelist(config.terrain_hitbox) != -1:
            if pillar in config.sprites:
                config.sprites.remove(pillar)
            del pillar
            continue
        else:
            config.terrain_hitbox.append(pillar.hitbox)
            config.terrain.append(pillar)
            p += 1




