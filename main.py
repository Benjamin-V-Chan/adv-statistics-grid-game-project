import pygame

# Pygame Setup
pygame.init()

screen_size = 800
display = pygame.display.set_mode((screen_size, screen_size))
clock = pygame.time.Clock()

# Constants
WHITE = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 64, 64)
BLUE = (64, 64, 255)

TILE_STATUS_COLORS = {
    "empty": WHITE,
    "mouse_hover": LIGHT_GREY,
    "player1": RED,
    "player2": BLUE
}

FPS = 60


# Default Game Settings
grid_size = 10
tile_buffer = 5


class Grid:
    def __init__(self):
        pass

# Grid Class
    # handles all tiles
    # will have attributes for:
        # storing each tile in a list
        # grid size/dimensions
        # tile sizes
            # create a func for calcualating a single tile's size
            # func would input screen size (for changing total length amounts)
            # func would use grid constant attributes for grid size, tile buffer, and num tiles
            # func should look smth like this:
                # tile buffer total = tiles count * tile_buffer + tile_buffer (since 0_index still has single buffer)
                # tiles total = total scren size - tile buffer total (remaining space that tiles should take up)
                # return tiles total / tiles count
        # tile amount
        # tile buffer (empty space between tiles)
    # funcs for:
        # drawing tiles/grid
        # managing tile statuses
        # updating tile statuses
        # being able to manage how tiles interact with eachother



class Tile:
    def __init__(self):
        pass

# Tile Class
    # attributes:
        # x_index (constant)
        # y_index (constant)
        # status
        # tile_size (constant)
        # x_coord (calculated based off x_index and grid dimensions/configurations)
        # y_coord (calculated based off y_index and grid dimensions/configurations)
        # color
    # should have method for easy status + color updates (since they update together)

# Main Loop
def main():
    running = True

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rendering
        display.fill(BLACK)

        # Pygame updates
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()