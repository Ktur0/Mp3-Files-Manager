import pygame
import os
import tkinter as tk
from tkinter import filedialog
import shutil
import sys

# Initialize Pygame
pygame.init()
screenInfo = (530, 400)
screen = pygame.display.set_mode(screenInfo, pygame.RESIZABLE)
pygame.display.set_caption("Simple Sound Player")
clock = pygame.time.Clock()
run = True

# Lấy đường dẫn của file py hiện tại
if getattr(sys, 'frozen', False):
    # Nếu chạy bằng file exe
    current_dir = os.path.dirname(sys.executable)
else:
    # Nếu chạy bằng file .py
    current_dir = os.path.dirname(os.path.abspath(__file__))

# Lấy đường dẫn folder mp3_files
DEST_FOLDER = os.path.join(current_dir, "mp3_files")
os.makedirs(DEST_FOLDER, exist_ok=True)

def addFiles():

    # ẩn cửa sổ Tkinter chính
    root = tk.Tk()
    root.withdraw()

    # mở cửa sổ chọn file
    file_path = filedialog.askopenfilename()
    root.destroy()  # đóng Tkinter

    # Lưu file vào thư mục
    if file_path:
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(DEST_FOLDER, file_name)
        shutil.copy(file_path, dest_path)

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
addFilesButton = pygame.Rect(460, frameY + 140, 50, 50)
deleteFilesButton = pygame.Rect(460, frameY + 210, 50, 50)

# Mouse
mouseX, mouseY = 0,0
mouseSize = 10
mouseBox = pygame.Rect(mouseX, mouseY, mouseSize, mouseSize)

# Load sound files
soundNames = []
soundFilesPath = []
soundFolder = 'mp3_files'
indexSelected = None
            
def reload():
    global soundNames, soundFilesPath, indexSelected

    soundNames = []
    soundFilesPath = []
    indexSelected = None

    scrollY = 0

    pygame.mixer.init()
    for i in os.listdir(soundFolder):
        if i.endswith('.mp3'): # Tìm các file đuôi .mp3 trong folder
            try:
                soundFilesPath.append(os.path.join(soundFolder, i))
                if len(i.split()) > 5:
                    i = ' '.join(i.split()[:5]) + '...'
                soundNames.append(i)
            except Exception as e:
                print(f"Lỗi khi load {i}: {e}")
    
    generateFramesAndButtons()

# Generate frames and buttons based on number of sound files
def generateFramesAndButtons():
    global nameFilesFrame, openFilesButton

    nameFilesFrame = []
    openFilesButton = []

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
addFilesImage = pygame.image.load("assets/addfile.png")
deleteFilseImage = pygame.image.load("assets/deletefiles.png")
nameFrameSelectedImage = pygame.image.load("assets/selectednameframe.png")

# Texts
font = pygame.font.SysFont('Roboto', 20)

# Load mp3 files before start main loop
reload()

# Main Loop
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
                        pygame.mixer.Sound(soundFilesPath[i]).play()  # Phát file mới
                
                if mouseBox.colliderect(stopButton):
                    pygame.mixer.stop() # Dừng toàn bộ âm thanh đang phát
                
                if mouseBox.colliderect(reloadButton):

                    pygame.mixer.stop()
                    reload()

                if mouseBox.colliderect(addFilesButton):
                    
                    addFiles()
                    pygame.mixer.stop()
                    reload()
                    
                for i in range(len(nameFilesFrame)):
                    if mouseBox.colliderect(nameFilesFrame[i].move(0, scrollY)):
                        indexSelected = i
                
                if mouseBox.colliderect(deleteFilesButton) and indexSelected != None:

                    pygame.mixer.stop()  # Dừng tất cả âm thanh đang phát
                    
                    if os.path.exists(soundFilesPath[indexSelected]): # Kiểm file có tồn tại hay không nếu có thì xóa
                        try:
                            os.remove(soundFilesPath[indexSelected])
                            reload()
                        except:
                            print("File not found")
                    
                    indexSelected = None

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
        # pygame.draw.rect(screen, grey, frame)
        if nameFilesFrame.index(frame) == indexSelected:
            frame = frame.move(0, scrollY)
            screen.blit(nameFrameSelectedImage, (frame.x, frame.y))
        else:
            frame = frame.move(0, scrollY)
            screen.blit(nameFrameImage, (frame.x, frame.y))
    
    for button in openFilesButton:
        button = button.move(0, scrollY)
        # pygame.draw.rect(screen, black, button)
        screen.blit(openButtonImage, (button.x, button.y))

    for name in soundNames:
        if soundNames.index(name) == indexSelected:
            text = font.render(name, True, black)
        else:
            text = font.render(name, True, white)
        screen.blit(text, (frameX + 20, nameFilesFrame[soundNames.index(name)].y + 38 + scrollY))
    
    # pygame.draw.rect(screen, red, reloadButton)
    screen.blit(reloadButtonImage, (reloadButton.x, reloadButton.y))
    # pygame.draw.rect(screen, blue, stopButton)
    screen.blit(stopButtonImage, (stopButton.x, stopButton.y))
    # pygame.draw.rect(screen, black, addFilesButton)
    screen.blit(addFilesImage, (addFilesButton.x, addFilesButton.y))
    # pygame.draw.rect(screen, grey, deleteFilesButton)
    screen.blit(deleteFilseImage, (deleteFilesButton.x, deleteFilesButton.y))

    pygame.display.update()

pygame.quit()