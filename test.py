import pygame, math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

water_y = HEIGHT
water_speed = 15
wave_time = 0

running = True
while running:
    dt = clock.tick(60) / 1000
    wave_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    water_y -= water_speed * dt
    if water_y < 0:
        water_y = 0

    screen.fill((25, 25, 25))

    points = []
    for x in range(0, WIDTH + 1, 10):
        y = water_y + math.sin(x * 0.02 + wave_time * 2) * 6
        points.append((x, y))

    points.append((WIDTH, HEIGHT))
    points.append((0, HEIGHT))

    pygame.draw.polygon(screen, (40, 120, 255), points)

    pygame.display.flip()

pygame.quit()