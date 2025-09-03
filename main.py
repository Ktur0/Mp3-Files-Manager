import pygame

pygame.init()

screenInfo = (800, 600)
screen = pygame.display.set_mode(screenInfo, pygame.RESIZABLE)
run = True

soundFiles = []

while run:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()