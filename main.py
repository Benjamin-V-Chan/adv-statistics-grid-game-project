import pygame

# Pygame Setup
pygame.init()

screen_size = 800
display = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()

# Main Loop
def main():

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Pygame updates
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()