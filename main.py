import pygame
from game import Game

p = pygame
p.display.set_caption("Sad-Tap")
screen = p.display.set_mode((800, 800))

clock = pygame.time.Clock()
FPS = 60


g = Game(screen, FPS)
running = True
while running:

    g.update()

    p.display.flip()
    for ev in p.event.get():
        if ev.type == p.QUIT:
            running = False
            p.quit()
        elif ev.type == p.MOUSEBUTTONDOWN:
            for apple in g.apples:
                if apple.rect.collidepoint(ev.pos):
                    if apple.state == 'sad':
                        apple.make_happy()
                    else:
                        g.timer -= g.TIME_PUNITION
    clock.tick(FPS)

