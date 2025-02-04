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
    def __init__(self, grid_size, screen_size, tile_buffer):
        self.grid_size = grid_size
        self.tile_buffer = tile_buffer
        
        self.tile_size = self.calculate_tile_size(screen_size)

        tiles = []
        for x in range(grid_size):
            for y in range(grid_size):
                tiles.append(Tile(x, y, self.tile_size, tile_buffer, "empty"))
        self.tiles = tiles

    def calculate_tile_size(self, total_length):
        """Calculates the size of each tile based on screen size and buffer."""
        tile_buffer_total = self.tile_buffer * self.grid_size + self.tile_buffer
        tiles_total = total_length - tile_buffer_total
        return tiles_total / self.grid_size

    def draw(self):
        for tile in self.tiles:
            pygame.draw.rect(display, tile.color, (tile.x_coordinate, tile.y_coordinate, self.tile_size, self.tile_size))

    def find_tile(self, x, y):
        """Finds the tile at a given (x, y) coordinate."""
        for tile in self.tiles:
            if (tile.x_coordinate <= x <= tile.x_coordinate + self.tile_size and
                tile.y_coordinate <= y <= tile.y_coordinate + self.tile_size):
                return tile
        return None
    
    # funcs for:
        # drawing tiles/grid
        # managing tile statuses
        # updating tile statuses
        # being able to manage how tiles interact with eachother


# Tile Class
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
    grid = Grid(grid_size, screen_size, tile_buffer)

    running = True

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rendering
        display.fill(BLACK)
        grid.draw()

        # Pygame updates
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()