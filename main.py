import pygame
import random

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

PLAYER_COLORS = {
    "player1": RED,
    "player2": BLUE
}

FPS = 60

# Default Game Settings
GRID_SIZE = 10
TILE_BUFFER = 5
DICE_SIDES = 6

# Helper Functions
def mouse_collision(mouse_coordinates: list, object_dimensions: list):
    """returns True if mouse_coordinates are within the object_dimensions"""
    object_dimensions_x = object_dimensions[0]
    object_dimensions_y = object_dimensions[1]
    if (object_dimensions_x <= mouse_coordinates[0] <= object_dimensions_x + object_dimensions[2] and
        object_dimensions_y <= mouse_coordinates[1] <= object_dimensions_y + object_dimensions[3]):
        return True
    return False

# Button Class
class Button:
    def __init__(self):
        pass
        # Attributes for following:
        # x
        # y
        # width
        # height
        # text
        # main_color
        # border_color
        # border_thickness
        # highlight_color
        # pressed_action
    # ability to cause a specific event, func, or status update based off button pressed?
        # need way to recycle this class for different buttons
        # AND
        # for different actions/menus (especially nesting menus)

# Player Class
class Player:
    def __init__(self, player, turns):
        self.current_player = player
        self.current_turns = turns

        self.color = PLAYER_COLORS[player]

    def new_turn(self):
        """Changes player's player and color attribute to reflect a COMPLETE new turn"""
        self.current_player = "player2" if self.current_player == "player1" else "player1"
        self.color = PLAYER_COLORS[self.current_player]

    def roll_dice(self):
        self.current_turns = random.randint(1, DICE_SIDES)

    def flip_coin(self):
        if random.randint(1, 2) == 1:
            self.current_turns *= 2

# Grid Class
class Grid:
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
            if mouse_collision([x, y], [tile.x_coordinate, tile.y_coordinate, self.tile_size, self.tile_size]):
                return tile
        return None
    
    def update_player(self, active_tile, player):
        """Updates the active_tile status with current_player, if it is not already claimed by a player."""
        if active_tile and (active_tile.status == "mouse_hover" or active_tile.status == "empty"):
            active_tile.update_status(player)

    def reset_hover_tiles(self):
        """Resets all tiles that are currently 'mouse_hover' back to 'empty'."""
        for tile in self.tiles:
            if tile.status == "mouse_hover":
                tile.update_status("empty")

    def update_hover(self, active_tile):
        """Updates the active_tile status to mouse_hover, if it is empty."""
        self.reset_hover_tiles()        
        if active_tile and active_tile.status == "empty":
            active_tile.update_status("mouse_hover")

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
    grid = Grid(GRID_SIZE, screen_size, TILE_BUFFER)

    current_player = Player("player1", 4)

    running = True

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        active_tile = grid.find_tile(mouse_x, mouse_y)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if active_tile:
                    current_player = grid.update_player(active_tile, current_player)

        # Update mouse_hover status tiles
        grid.update_hover(active_tile)

        # Player Turn
        if current_player.turn == 0:
            current_player.switch_turn()
            current_player.roll_dice()


        # Rendering
        display.fill(BLACK)
        grid.draw()

        # Pygame updates
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()