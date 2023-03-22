import pygame
import sys

pygame.init

screen = pygame.display.set_mode((400, 800))
plateau = pygame.Surface((100, 100))

timer = pygame.time.Clock()

game_on = True

image_blanc = pygame.image.load("blanc.gif").convert()

while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(pygame.Color('Gray'))
    plateau.fill((154, 66, 4))
    screen.blit(plateau, (150, 200))
    pygame.display.update()
    timer.tick(60)