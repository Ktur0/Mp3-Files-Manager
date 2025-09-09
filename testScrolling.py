import pygame

pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Tạo nhiều khối giả lập map dài
blocks = []
for i in range(100):
    rect = pygame.Rect(i * 120, HEIGHT // 2, 100, 100)
    blocks.append(rect)

# Vị trí camera
scroll_x = 0
speed = 10

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Điều khiển cuộn bằng phím
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        scroll_x -= speed
    if keys[pygame.K_LEFT]:
        scroll_x += speed

    # Giới hạn cuộn để không vượt map
    max_scroll = -(len(blocks) * 120 - WIDTH)
    scroll_x = min(0, max(scroll_x, max_scroll))

    # Vẽ nền
    screen.fill(WHITE)

    # Vẽ các khối nằm trong vùng nhìn thấy
    for block in blocks:
        # Vị trí sau khi dịch camera
        draw_rect = block.move(scroll_x, 0)

        # Chỉ vẽ nếu nằm trong màn hình
        if draw_rect.colliderect(screen.get_rect()):
            pygame.draw.rect(screen, RED, draw_rect)

    pygame.display.flip()

pygame.quit()
