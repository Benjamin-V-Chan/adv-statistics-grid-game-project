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


# Game Info Display Class
class GameInfoDisplay:
    def __init__(self, width, height, split_offset):
        self.width = width
        self.height = height
        self.split_offset = split_offset
        self.font = pygame.font.Font(None, 36)

    def draw(self, player1_tiles, player2_tiles, current_player, turns_left):
        """Draw the game information display with a diagonal split and border highlight."""
        # Split diagonal points
        left_split = screen_width // 2 - self.split_offset
        right_split = screen_width // 2 + self.split_offset

        pygame.draw.polygon(display, RED, [(0, BOARD_SIZE), (0, screen_height), (left_split, screen_height)])
        pygame.draw.polygon(display, BLUE, [(screen_width, BOARD_SIZE), (screen_width, screen_height),
                                            (right_split, screen_height)])

        # Highlight the current player's side with a border
        border_width = 5
        if current_player == "player1":
            pygame.draw.polygon(display, HIGHLIGHT_YELLOW, [(0, BOARD_SIZE), (0, screen_height), 
                                                             (left_split, screen_height)], border_width)
        else:
            pygame.draw.polygon(display, HIGHLIGHT_YELLOW, [(screen_width, BOARD_SIZE), (screen_width, screen_height), 
                                                             (right_split, screen_height)], border_width)

        # Display player tile counts
        p1_text = self.font.render(f"P1 Tiles: {player1_tiles}", True, WHITE)
        display.blit(p1_text, (40, BOARD_SIZE + 50))

        p2_text = self.font.render(f"P2 Tiles: {player2_tiles}", True, WHITE)
        display.blit(p2_text, (screen_width - 170, BOARD_SIZE + 50))

        # Display current player's turn & turns left
        if current_player == "player1":
            turn_text = self.font.render(f"Turns Left: {turns_left}", True, WHITE)
            display.blit(turn_text, (40, BOARD_SIZE + 90))
        else:
            turn_text = self.font.render(f"Turns Left: {turns_left}", True, WHITE)
            display.blit(turn_text, (screen_width - 170, BOARD_SIZE + 90))

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

# Dice Rolling System
class DiceRoller:
    def __init__(self):
        self.rolling = False
        self.roll_frames = 0
        self.current_numbers = [random.randint(1, DICE_SIDES) for _ in range(NUMBER_OF_DICE)]
        self.final_numbers = []
        self.dice_size = 200
        self.spacing = self.dice_size // 5
        self.border_thickness = self.dice_size // 20
        self.font = pygame.font.Font(None, self.dice_size // 2)
        self.post_roll_frames = 0  # Delay frames after final roll before allowing actions

    def start_roll(self):
        """Starts the dice rolling animation."""
        self.rolling = True
        self.roll_frames = 0
        self.final_numbers = []
        self.post_roll_frames = 0
        self.current_numbers = [random.randint(1, DICE_SIDES) for _ in range(NUMBER_OF_DICE)]

    def update(self):
        """Updates the rolling animation."""
        if self.rolling:
            if self.roll_frames % (ROLL_ANIMATION_FRAMES // ROLL_CHANGES) == 0:
                self.current_numbers = [random.randint(1, DICE_SIDES) for _ in range(NUMBER_OF_DICE)]
            self.roll_frames += 1

            if self.roll_frames >= ROLL_ANIMATION_FRAMES:
                self.rolling = False
                self.final_numbers = self.current_numbers[:]
        elif self.final_numbers:
            self.post_roll_frames += 1
            if self.post_roll_frames >= 30:  # Delay before enabling actions
                self.final_numbers = []

    def draw(self):
        """Draws the dice in the middle of the screen with dynamic borders and spacing."""
        if self.rolling or self.final_numbers:
            total_width = (NUMBER_OF_DICE * self.dice_size) + ((NUMBER_OF_DICE - 1) * self.spacing)
            start_x = (screen_width - total_width) // 2
            y_position = screen_height // 2 - self.dice_size // 2

            for i, number in enumerate(self.current_numbers):
                x = start_x + i * (self.dice_size + self.spacing)
                pygame.draw.rect(display, WHITE, (x, y_position, self.dice_size, self.dice_size), border_radius=10)
                pygame.draw.rect(display, BLACK, (x, y_position, self.dice_size, self.dice_size), self.border_thickness, border_radius=10)
                text = self.font.render(str(number), True, BLACK)
                text_rect = text.get_rect(center=(x + self.dice_size // 2, y_position + self.dice_size // 2))
                display.blit(text, text_rect)

# Player Class
class Player:
    def __init__(self, player):
        self.current_player = player
        self.current_turns = 0
        self.color = PLAYER_COLORS[player]

    def switch_turn(self):
        """Switch player and prepare for new turn."""
        self.current_player = "player2" if self.current_player == "player1" else "player1"
        self.color = PLAYER_COLORS[self.current_player]
        self.current_turns = 0

    def flip_coin(self):
        """Doubles turns on heads, but loses all turns if tails."""
        if random.randint(1, 2) == 1:
            self.current_turns *= 2
        else:
            self.current_turns = 0

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
    def __init__(self, grid_size, board_size, tile_buffer):
        self.grid_size = grid_size
        self.tile_buffer = tile_buffer
        self.tile_size = self.calculate_tile_size(board_size)
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

# Main Game Loop
def main():
    global current_player

    current_player = Player("player1")

    grid = Grid(GRID_SIZE, BOARD_SIZE, TILE_BUFFER)
    game_info = GameInfoDisplay(screen_width, GAME_INFO_DISPLAY_HEIGHT, SPLIT_OFFSET)

    font = pygame.font.Font(None, 36)

    # Flip Coin Button (Centered)
    button_width, button_height = 150, 50
    button_x = (screen_width // 2) - (button_width // 2)
    button_y = BOARD_SIZE + (GAME_INFO_DISPLAY_HEIGHT // 2) - (button_height // 2)
    flip_coin_button = Button(button_x, button_y, button_width, button_height,
                              "Flip Coin", LIGHT_GREY, BLACK, WHITE, current_player.flip_coin)

    dice_roller = DiceRoller()

    # Start first dice roll
    dice_roller.start_roll()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        active_tile = grid.find_tile(mouse_pos[0], mouse_pos[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle normal actions only after rolling
                if not dice_roller.rolling and current_player.current_turns > 0:
                    if active_tile and active_tile.status in ["empty", "mouse_hover"]:
                        active_tile.update_status(current_player.current_player)
                        current_player.current_turns -= 1
                if flip_coin_button.enabled:
                    flip_coin_button.check_click(mouse_pos)

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