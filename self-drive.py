import pygame
import sys

# initialize simulation
pygame.init()

#display setup
width =1024
height = 768
screen = pygame.display.set_mode((width, height))#resolution-->4:3(1024x768)
pygame.display.set_caption("Self-Driving Car Simulation")

# main loop-keeps the window open and the simulation running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color (black)
    screen.fill((0, 0, 0))

    # update the display
    pygame.display.flip()

# quit pygame
pygame.quit()