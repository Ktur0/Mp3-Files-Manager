import pygame
import tkinter as tk
from tkinter import filedialog
import shutil
import os

# thư mục đích
DEST_FOLDER = "D:/Music App/mp3_files"
os.makedirs(DEST_FOLDER, exist_ok=True)

# khởi tạo pygame
pygame.init()
screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Thêm file vào phần mềm")

font = pygame.font.SysFont(None, 36)

# tạo nút
button_rect = pygame.Rect(150, 120, 200, 60)

def add_file():
    # ẩn cửa sổ Tkinter chính
    root = tk.Tk()
    root.withdraw()

    # mở cửa sổ chọn file
    file_path = filedialog.askopenfilename()
    root.destroy()  # đóng Tkinter

    if file_path:
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(DEST_FOLDER, file_name)
        shutil.copy(file_path, dest_path)
        print(f"Đã lưu file vào: {dest_path}")
        return f"Đã lưu: {file_name}"
    return "Không có file nào được chọn."

status_text = "Chưa chọn file nào."

running = True
while running:
    screen.fill((30, 30, 30))

    # vẽ nút
    pygame.draw.rect(screen, (70, 130, 180), button_rect)
    text_surface = font.render("Chọn file", True, (255, 255, 255))
    screen.blit(text_surface, (button_rect.x + 40, button_rect.y + 15))

    # vẽ trạng thái
    status_surface = font.render(status_text, True, (200, 200, 200))
    screen.blit(status_surface, (50, 220))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                status_text = add_file()

    pygame.display.flip()

pygame.quit()
