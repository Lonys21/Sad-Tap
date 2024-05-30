import pygame
from game import Game

pygame.init()
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
            if g.actual_screen == 'welcome':
                if g.play_button.rect.collidepoint(ev.pos):
                    g.actual_screen = 'game'
                    g.play_button.resize("reset")
            elif g.actual_screen == 'game':
                for apple in g.apples:
                    if apple.rect.collidepoint(ev.pos):
                        if apple.state == 'sad':
                            apple.make_happy()
                        else:
                            g.timer -= g.TIME_PUNITION
            elif g.actual_screen == 'loose':
                if g.replay_button.rect.collidepoint(ev.pos):
                    g.actual_screen = 'game'
                    g.reset()
                    g.replay_button.resize("reset")
        elif ev.type == p.MOUSEMOTION:
            if g.actual_screen == 'welcome':
                if g.play_button.rect.collidepoint(ev.pos):
                    g.play_button.resize("extension")
                else:
                    g.play_button.resize("reset")
            elif g.actual_screen == 'loose':
                if g.replay_button.rect.collidepoint(ev.pos):
                    g.replay_button.resize("extension")
                else:
                    g.replay_button.resize("reset")
    clock.tick(FPS)

