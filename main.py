import pygame

pygame.init()

screenInfo = pygame.display.Info()
screen = pygame.display.set_mode((screenInfo.current_w, screenInfo.current_h), pygame.RESIZABLE)
run = True

while run:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    
