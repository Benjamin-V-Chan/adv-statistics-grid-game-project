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
    def __init__(self, x_index, y_index, tile_size, tile_buffer, status):
        self.x_index = x_index
        self.y_index = y_index
        self.status = status
        self.tile_size = tile_size

        self.x_coordinate = (x_index * tile_size) + ((x_index + 1) * tile_buffer)
        self.y_coordinate = (y_index * tile_size) + ((y_index + 1) * tile_buffer)
        self.color = TILE_STATUS_COLORS[status]

    def update_status(self, new_status):
        self.status = new_status
        self.color = TILE_STATUS_COLORS[new_status]

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