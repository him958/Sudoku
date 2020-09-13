import pygame

pygame.init( )
win = pygame.display.set_mode((500, 500));
pygame.display.set_caption("First Game")
# pygame.time.delay(10000)
run = True
x = 45
y = 100

width = 30
height = 60
vel: int = 5
b = 0
while run:
    pygame.time.delay(100)

    for event in pygame.event.get( ):

        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed( )
    print(keys)
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel
    win.fill((0, 0, 255))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update( )
