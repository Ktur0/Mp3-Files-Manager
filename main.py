import pygame
import os

# Initialize Pygame
pygame.init()
screenInfo = (530, 400)
screen = pygame.display.set_mode(screenInfo, pygame.RESIZABLE)
pygame.display.set_caption("Simple Sound Player")
clock = pygame.time.Clock()
run = True

# Load sound files
soundFolder = 'mp3_files'
soundFilesPath = []
pygame.mixer.init()
for i in os.listdir(soundFolder):
    if i.endswith('.mp3'):
        try:
            soundFilesPath.append(pygame.mixer.Sound(os.path.join(soundFolder, i)))
        except Exception as e:
            print(f"Lỗi khi load {i}: {e}")
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
reloadButton = pygame.Rect(460, frameY, 50, 50)
stopButton = pygame.Rect(460, frameY + 70, 50, 50)

# Mouse
mouseX, mouseY = 0,0
mouseSize = 10
mouseBox = pygame.Rect(mouseX, mouseY, mouseSize, mouseSize)

# Generate frames and buttons based on number of sound files
for i in range(len(soundFilesPath)):
    nameFilesFrame.append(pygame.Rect(frameX, frameY + i*(frameSizeY + frameY), frameSizeX, frameSizeY))
    openFilesButton.append(pygame.Rect(buttonX, buttonY + i*(buttonSizeY + frameY), buttonSizeX, buttonSizeY))

# Scroll variables
scrollSpeed = 10
scrollY = 0
maxScroll = -(len(openFilesButton) * (frameSizeY + frameY) - screenInfo[1])

while run:

    clock.tick(60)

    # Update mouse position
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseBox = pygame.Rect(mouseX, mouseY, mouseSize, mouseSize)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range (len(openFilesButton)):
                if mouseBox.colliderect(openFilesButton[i]):
                    pygame.mixer.stop()  # Dừng tất cả âm thanh đang phát
                    soundFilesPath[i].play()  # Phát file mới
            
            if mouseBox.colliderect(stopButton):
                pygame.mixer.stop()
            
            if mouseBox.colliderect(reloadButton):

                pygame.mixer.stop()

                # Reload sound files
                soundFolder = 'mp3_files'
                soundFilesPath = []
                pygame.mixer.init()
                for i in os.listdir(soundFolder):
                    if i.endswith('.mp3'):
                        try:
                            soundFilesPath.append(pygame.mixer.Sound(os.path.join(soundFolder, i)))
                        except Exception as e:
                            print(f"Lỗi khi load {i}: {e}")
                
                # Regenerate frames and buttons
                nameFilesFrame = []
                openFilesButton = []
                for i in range(len(soundFilesPath)):
                    nameFilesFrame.append(pygame.Rect(frameX, frameY + i*(frameSizeY + frameY), frameSizeX, frameSizeY))
                    openFilesButton.append(pygame.Rect(buttonX, buttonY + i*(buttonSizeY + frameY), buttonSizeX, buttonSizeY))

            if event.button == 4:
                scrollY += scrollSpeed
            
            if event.button == 5:
                scrollY -= scrollSpeed
    
    # Limit scrolling
    maxScroll = -(len(openFilesButton) * (frameSizeY + frameY) - screenInfo[1]) - 20
    scrollY = min(0, max(scrollY, maxScroll))

    screen.fill(white)

    # Draw frames and buttons
    for frame in nameFilesFrame:
        frame = frame.move(0, scrollY)
        pygame.draw.rect(screen, grey, frame)
    
    for button in openFilesButton:
        button = button.move(0, scrollY)
        pygame.draw.rect(screen, black, button)
    
    pygame.draw.rect(screen, red, reloadButton)
    pygame.draw.rect(screen, blue, stopButton)

    pygame.display.update()

pygame.quit()