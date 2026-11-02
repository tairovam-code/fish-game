import math
import os
import random
import sys

import pygame

pygame.init()

# 1. Окно
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Рыбка на pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")


def load(name, scale=2):
    """Картинка с прозрачным фоном (convert_alpha), увеличенная без размытия."""
    img = pygame.image.load(os.path.join(IMG, name)).convert_alpha()
    w, h = img.get_size()
    return pygame.transform.scale(img, (w * scale, h * scale))


# 2. Картинки Kenney (PNG без фона). Рыбка в файле смотрит ВПРАВО.
fishes = [load(f"fish_{c}.png") for c in ("orange", "red", "blue", "green", "pink")]
fish_index = 0
bubble_imgs = [load(f"bubble_{c}.png", 1) for c in "abc"]

bubbles = [
    {
        "img": random.choice(bubble_imgs),
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "v": random.uniform(0.5, 1.8),
    }
    for _ in range(12)
]

# 3. Управление
x, y = WIDTH / 2, HEIGHT / 2
speed = 5
facing_right = True
tilt_target = 0.0
tilt = 0.0
t = 0.0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:  # пробел - сменить цвет рыбки
                fish_index = (fish_index + 1) % len(fishes)

    keys = pygame.key.get_pressed()
    dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
    dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])

    moving = bool(dx or dy)
    if moving:
        length = math.hypot(dx, dy)
        x += dx / length * speed
        y += dy / length * speed
        t += 0.35  # "плавание": рыбка покачивается
        if dx:
            facing_right = dx > 0
        tilt_target = -dy * 15  # вверх - нос кверху, вниз - нос книзу
    else:
        t += 0.08  # в покое покачивается медленнее
        tilt_target = 0

    tilt += (tilt_target - tilt) * 0.2  # плавный наклон
    wobble = math.sin(t) * (6 if moving else 2)

    fish = fishes[fish_index]
    if not facing_right:
        fish = pygame.transform.flip(fish, True, False)
    angle = tilt + wobble
    if not facing_right:
        angle = -angle
    fish = pygame.transform.rotate(fish, angle)

    rect = fish.get_rect(center=(x, y))
    rect.clamp_ip(screen.get_rect())
    x, y = rect.center

    # рисуем
    screen.fill((51, 153, 220))
    for b in bubbles:
        b["y"] -= b["v"]
        if b["y"] < -20:
            b["y"] = HEIGHT + 20
            b["x"] = random.randint(0, WIDTH)
        screen.blit(b["img"], (b["x"], b["y"]))
    screen.blit(fish, rect)
    hint = font.render("Стрелки / WASD - плыть, Пробел - цвет, Esc - выход", True, (255, 255, 255))
    screen.blit(hint, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
