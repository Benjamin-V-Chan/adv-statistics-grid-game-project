import pygame
import random

# Pygame Setup
pygame.init()
screen_width, screen_height = 600, 800
display = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Constants
WHITE = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 64, 64)
BLUE = (64, 64, 255)
HIGHLIGHT_YELLOW = (255, 255, 0)

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

BOARD_SIZE = screen_width
GAME_INFO_DISPLAY_HEIGHT = screen_height - BOARD_SIZE
SPLIT_OFFSET = 50  # Adjustable offset for the diagonal split

FPS = 60
GRID_SIZE = 10
TILE_BUFFER = 5
DICE_SIDES = 6
NUMBER_OF_DICE = 2
ROLL_ANIMATION_FRAMES = 100  # Total frames to roll
ROLL_CHANGES = 10  # Number of number changes in animation


# Helper Functions
def mouse_collision(mouse_pos, obj_rect):
    """Check if mouse is within a rectangle."""
    return (obj_rect[0] <= mouse_pos[0] <= obj_rect[0] + obj_rect[2] and 
            obj_rect[1] <= mouse_pos[1] <= obj_rect[1] + obj_rect[3])

# Button Class
class Button:
    def __init__(self, x, y, width, height, text, main_color, border_color, highlight_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.main_color = main_color
        self.border_color = border_color
        self.highlight_color = highlight_color
        self.action = action
        self.is_hovering = False
        self.enabled = True  # Prevent clicking multiple times per turn

    def draw(self, screen, font):
        """Draw the button and change color when hovered."""
        color = self.highlight_color if self.is_hovering and self.enabled else self.main_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        """Check if the mouse is over the button."""
        return self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        """Call action if clicked and not enabled."""
        if self.is_hovered(mouse_pos) and self.action:
            self.action()
            self.enabled = False

# Player Class
class Player:
    def __init__(self, player):
        self.current_player = player
        self.current_turns = 0
        self.color = PLAYER_COLORS[player]

    def switch_turn(self):
        """Switch player and reset turns."""
        self.current_player = "player2" if self.current_player == "player1" else "player1"
        self.color = PLAYER_COLORS[self.current_player]
        self.roll_dice()

    def roll_dice(self):
        """Rolls a dice to determine the number of turns."""
        self.current_turns = random.randint(1, DICE_SIDES)

    def flip_coin(self):
        """Doubles turns on heads."""
        if random.randint(1, 2) == 1:
            self.current_turns *= 2

# Tile Class
class Tile:
    def __init__(self, x_index, y_index, tile_size, tile_buffer, status="empty"):
        self.x_index = x_index
        self.y_index = y_index
        self.status = status
        self.tile_size = tile_size
        self.x_coordinate = (x_index * tile_size) + ((x_index + 1) * tile_buffer)
        self.y_coordinate = (y_index * tile_size) + ((y_index + 1) * tile_buffer)
        self.color = TILE_STATUS_COLORS[status]

    def update_status(self, new_status):
        """Update the tile's status and color."""
        self.status = new_status
        self.color = TILE_STATUS_COLORS[new_status]

# Grid Class
class Grid:
    def __init__(self, grid_size, screen_size, tile_buffer):
        self.grid_size = grid_size
        self.tile_buffer = tile_buffer
        self.tile_size = self.calculate_tile_size(screen_size)
        self.tiles = [Tile(x, y, self.tile_size, tile_buffer) for x in range(grid_size) for y in range(grid_size)]

    def calculate_tile_size(self, total_length):
        """Calculate tile size dynamically."""
        return (total_length - ((self.grid_size + 1) * self.tile_buffer)) / self.grid_size

    def draw(self):
        """Draw the grid."""
        for tile in self.tiles:
            pygame.draw.rect(display, tile.color, (tile.x_coordinate, tile.y_coordinate, self.tile_size, self.tile_size))

    def find_tile(self, x, y):
        """Find the tile at a given (x, y) coordinate."""
        for tile in self.tiles:
            if mouse_collision([x, y], [tile.x_coordinate, tile.y_coordinate, self.tile_size, self.tile_size]):
                return tile
        return None

    def reset_hover_tiles(self):
        """Reset all 'mouse_hover' tiles to 'empty'."""
        for tile in self.tiles:
            if tile.status == "mouse_hover":
                tile.update_status("empty")

    def update_hover(self, active_tile):
        """Set active tile to 'mouse_hover' if empty."""
        self.reset_hover_tiles()
        if active_tile and active_tile.status == "empty":
            active_tile.update_status("mouse_hover")

# Game Actions

def flip_coin_action():
    """Flip a coin when the button is pressed."""
    global current_player
    current_player.flip_coin()



# Main Game Loop
def main():
    global current_player

    grid = Grid(GRID_SIZE, BOARD_SIZE, TILE_BUFFER)
    current_player = Player("player1")
    font = pygame.font.Font(None, 36)

    # List of buttons
    buttons = [
        Button(600, 120, 150, 50, "Flip Coin", BLUE, BLACK, LIGHT_GREY, flip_coin_action)
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        active_tile = grid.find_tile(mouse_pos[0], mouse_pos[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(mouse_pos)  # Handle button clicks

                if active_tile and (active_tile.status == "empty" or active_tile.status == "mouse_hover"):
                    active_tile.update_status(current_player.current_player)
                    current_player.current_turns -= 1  # Reduce turns

        # Update hover state
        grid.update_hover(active_tile)

        # Handle turn switching
        if current_player.current_turns == 0:
            current_player.switch_turn()

        # Drawing
        display.fill(BLACK)
        grid.draw()
        for button in buttons:
            button.is_hovering = button.is_hovered(mouse_pos)
            button.draw(display, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()