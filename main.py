import pygame
import os

# Initialize Pygame
pygame.init()

screenInfo = (460, 400)
screen = pygame.display.set_mode(screenInfo, pygame.RESIZABLE)
run = True

# Load sound files
soundFolder = 'mp3_files'
soundFilesPath = []
for i in os.listdir(soundFolder):
    if i.endswith('.mp3'):
        soundFilesPath.append(pygame.mixer.Sound(os.path.join(soundFolder, i)))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
grey = (128, 128, 128)

# Initalize frames and buttons
frameX, frameY = 20, 20
frameSizeX, frameSizeY = 300, 100
buttonX, buttonY = frameX + frameSizeX + 20, frameY
buttonSizeX, buttonSizeY = 100, 100
nameFilesFrame = []
openFilesButton = []

for i in range(len(soundFilesPath)):
    nameFilesFrame.append(pygame.Rect(frameX, frameY + i*(frameSizeY + frameY), frameSizeX, frameSizeY))
    openFilesButton.append(pygame.Rect(buttonX, buttonY + i*(buttonSizeY + frameY), buttonSizeX, buttonSizeY))

while run:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    screen.fill(white)

    for frame in nameFilesFrame:
        pygame.draw.rect(screen, grey, frame)
    
    for button in openFilesButton:
        pygame.draw.rect(screen, black, button)

    pygame.display.update()

pygame.quit()