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
soundNames = []
soundFolder = 'mp3_files'
soundFilesPath = []
pygame.mixer.init()
for i in os.listdir(soundFolder):
    if i.endswith('.mp3'):
        try:
            soundFilesPath.append(pygame.mixer.Sound(os.path.join(soundFolder, i)))
            if len(i.split()) > 5:
                i = ' '.join(i.split()[:5]) + '...'
            soundNames.append(i)
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

# Images
backgroundImage = pygame.image.load("assets/background.png")
nameFrameImage = pygame.image.load("assets/nameframe.png")
openButtonImage = pygame.image.load("assets/openfilesbutton.png")
reloadButtonImage = pygame.image.load("assets/reloadbutton.png")
stopButtonImage = pygame.image.load("assets/stopbutton.png")

# Texts
font = pygame.font.SysFont('Roboto', 20)

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
            if event.button == 1:
                for i in range (len(openFilesButton)):
                    if mouseBox.colliderect(openFilesButton[i].move(0, scrollY)):
                        pygame.mixer.stop()  # Dừng tất cả âm thanh đang phát
                        soundFilesPath[i].play()  # Phát file mới
                
                if mouseBox.colliderect(stopButton):
                    pygame.mixer.stop()
                
                if mouseBox.colliderect(reloadButton):

                    pygame.mixer.stop()

                    scrollY = 0

                    # Reload sound files
                    soundNames = []
                    soundFolder = 'mp3_files'
                    soundFilesPath = []
                    pygame.mixer.init()
                    for i in os.listdir(soundFolder):
                        if i.endswith('.mp3'):
                            try:
                                soundFilesPath.append(pygame.mixer.Sound(os.path.join(soundFolder, i)))
                                soundNames.append(i)
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

    screen.blit(backgroundImage, (0, 0))

    # Draw frames and buttons
    for frame in nameFilesFrame:
        frame = frame.move(0, scrollY)
        # pygame.draw.rect(screen, grey, frame)
        screen.blit(nameFrameImage, (frame.x, frame.y))
    
    for button in openFilesButton:
        button = button.move(0, scrollY)
        # pygame.draw.rect(screen, black, button)
        screen.blit(openButtonImage, (button.x, button.y))

    for i in soundNames:
        text = font.render(i, True, white)
        screen.blit(text, (frameX + 20, nameFilesFrame[soundNames.index(i)].y + 40 + scrollY))
    
    # pygame.draw.rect(screen, red, reloadButton)
    screen.blit(reloadButtonImage, (reloadButton.x, reloadButton.y))
    # pygame.draw.rect(screen, blue, stopButton)
    screen.blit(stopButtonImage, (stopButton.x, stopButton.y))

    pygame.display.update()

pygame.quit()