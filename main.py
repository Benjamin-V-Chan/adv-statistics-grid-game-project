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

def flatten_list(l, master_list):
    for element in l:
        if isinstance(element, list):
            flatten_list(element, master_list)
        else:
            master_list.append(element)
    return master_list

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
        self.post_roll_frames = 0

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
            if self.post_roll_frames >= 30:
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
    def __init__(self, x, y, tile_size, tile_buffer, status="empty"):
        self.x = x
        self.y = y
        self.status = status
        self.tile_size = tile_size
        self.tile_buffer = tile_buffer
        self.x_coordinate = (x * tile_size) + ((x + 1) * tile_buffer)
        self.y_coordinate = (y * tile_size) + ((y + 1) * tile_buffer)
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
        self.tiles = [[Tile(x, y, self.tile_size, tile_buffer)
                       for y in range(grid_size)]
                      for x in range(grid_size)]

    def calculate_tile_size(self, total_length):
        return (total_length - ((self.grid_size + 1) * self.tile_buffer)) / self.grid_size

    def draw(self):
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(display, tile.color,
                                 (tile.x_coordinate, tile.y_coordinate,
                                  self.tile_size, self.tile_size))

    def reset_hover_tiles(self):
        for tile in flatten_list(self.tiles, []):
            if tile.status == "mouse_hover":
                tile.update_status("empty")

    def update_hover(self, active_tile):
        self.reset_hover_tiles()
        if active_tile and active_tile.status == "empty":
            active_tile.update_status("mouse_hover")

    def find_tile(self, x, y):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                tile = self.tiles[row][col]
                if mouse_collision([x, y],
                                     [tile.x_coordinate, tile.y_coordinate,
                                      self.tile_size, self.tile_size]):
                    return tile
        return None

#TODO Optimize Flood Fill Check function (no brute force)
# Brute-Force Flood Fill Check for Any Closed Rectangle
    def flood_fill_player(self, player):
        """
        Iterates over every possible rectangle on the grid. If a rectangle's boundary
        (its top, bottom, left, and right edges) is completely filled with the player's tile,
        then the entire interior of that rectangle is updated to that player's tile.
        """
        for x1 in range(self.grid_size):
            for y1 in range(self.grid_size):
                for x2 in range(x1 + 1, self.grid_size):
                    for y2 in range(y1 + 1, self.grid_size):
                        complete = True
                        # Check top edge
                        for x in range(x1, x2 + 1):
                            if self.tiles[x][y1].status != player:
                                complete = False
                                break
                        if not complete:
                            continue
                        # Check bottom edge
                        for x in range(x1, x2 + 1):
                            if self.tiles[x][y2].status != player:
                                complete = False
                                break
                        if not complete:
                            continue
                        # Check left edge
                        for y in range(y1, y2 + 1):
                            if self.tiles[x1][y].status != player:
                                complete = False
                                break
                        if not complete:
                            continue
                        # Check right edge
                        for y in range(y1, y2 + 1):
                            if self.tiles[x2][y].status != player:
                                complete = False
                                break
                        if not complete:
                            continue
                        # If we get here, the boundary is complete.
                        for x in range(x1 + 1, x2):
                            for y in range(y1 + 1, y2):
                                self.tiles[x][y].update_status(player)

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
    dice_roller.start_roll()  # Start the first dice roll

    running = True
    while running:
        flattened_list_tiles = flatten_list(grid.tiles, [])
        mouse_pos = pygame.mouse.get_pos()
        active_tile = grid.find_tile(mouse_pos[0], mouse_pos[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not dice_roller.rolling and current_player.current_turns > 0:
                    if active_tile and active_tile.status in ["empty", "mouse_hover"]:
                        active_tile.update_status(current_player.current_player)
                        # Check the entire grid for any closed rectangles for the current player.
                        grid.flood_fill_player(current_player.current_player)
                        current_player.current_turns -= 1
                if flip_coin_button.enabled:
                    flip_coin_button.check_click(mouse_pos)

        dice_roller.update()

        if not dice_roller.rolling and current_player.current_turns == 0 and not dice_roller.final_numbers:
            current_player.switch_turn()
            dice_roller.start_roll()
            flip_coin_button.enabled = False

        if not dice_roller.rolling:
            grid.update_hover(active_tile)
            if dice_roller.final_numbers:
                current_player.current_turns = sum(dice_roller.final_numbers)
                flip_coin_button.enabled = True

        flip_coin_button.is_hovering = flip_coin_button.is_hovered(mouse_pos)

        display.fill(BLACK)
        game_info.draw(sum(tile.status == "player1" for tile in flattened_list_tiles),
                       sum(tile.status == "player2" for tile in flattened_list_tiles),
                       current_player.current_player,
                       current_player.current_turns)
        flip_coin_button.draw(display, font)
        grid.draw()
        dice_roller.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main()