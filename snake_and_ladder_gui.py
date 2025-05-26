#!/usr/bin/env python3
import pygame
import random
import sys
import os
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = 500
GRID_SIZE = 10
CELL_SIZE = BOARD_SIZE // GRID_SIZE
DICE_SIZE = 80
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
BOARD_COLOR = (240, 230, 200)
GRID_COLOR = (200, 180, 150)
SNAKE_COLOR = (50, 150, 50)
LADDER_COLOR = (150, 100, 50)

# Player colors
PLAYER_COLORS = [RED, BLUE, GREEN, YELLOW]

class SnakeAndLadderGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake and Ladder Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        self.large_font = pygame.font.SysFont('Arial', 32)
        
        # Game state
        self.board_size = 100
        self.total_players = 2  # Default
        self.player_positions = {i+1: 0 for i in range(self.total_players)}
        self.current_player = 1
        self.dice_value = 1
        self.dice_rolling = False
        self.roll_start_time = 0
        self.game_over = False
        self.winner = None
        self.animation_in_progress = False
        self.animation_start_time = 0
        self.animation_from = 0
        self.animation_to = 0
        self.animation_player = 0
        self.show_menu = True
        
        # Define snakes (head: tail)
        self.snakes = {
            17: 7,
            54: 34,
            62: 19,
            64: 60,
            87: 36,
            93: 73,
            95: 75,
            98: 79
        }
        
        # Define ladders (bottom: top)
        self.ladders = {
            1: 38,
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            51: 67,
            72: 91,
            80: 99
        }
        
        # Load images
        self.load_images()
        
        # Board position
        self.board_x = 50
        self.board_y = 50
        
    def load_images(self):
        # Create dice images
        self.dice_images = []
        for i in range(1, 7):
            dice_img = pygame.Surface((DICE_SIZE, DICE_SIZE))
            dice_img.fill(WHITE)
            pygame.draw.rect(dice_img, BLACK, (0, 0, DICE_SIZE, DICE_SIZE), 2)
            
            # Draw dots based on dice value
            if i == 1:
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
            elif i == 2:
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            elif i == 3:
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            elif i == 4:
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            elif i == 5:
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//2, DICE_SIZE//2), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
            elif i == 6:
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, DICE_SIZE//2), 8)
                pygame.draw.circle(dice_img, BLACK, (DICE_SIZE//4, 3*DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, DICE_SIZE//4), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, DICE_SIZE//2), 8)
                pygame.draw.circle(dice_img, BLACK, (3*DICE_SIZE//4, 3*DICE_SIZE//4), 8)
                
            self.dice_images.append(dice_img)
    
    def get_cell_position(self, cell_number):
        """Convert cell number (1-100) to pixel coordinates on the board."""
        if cell_number <= 0:
            return None  # Player not on board yet
            
        # Calculate row and column (0-indexed)
        row = (cell_number - 1) // GRID_SIZE
        row = GRID_SIZE - 1 - row  # Invert row (bottom to top)
        
        # Column depends on row direction (zigzag pattern)
        if (GRID_SIZE - 1 - row) % 2 == 0:  # Even rows go left to right
            col = (cell_number - 1) % GRID_SIZE
        else:  # Odd rows go right to left
            col = GRID_SIZE - 1 - ((cell_number - 1) % GRID_SIZE)
            
        # Calculate pixel position (center of cell)
        x = self.board_x + col * CELL_SIZE + CELL_SIZE // 2
        y = self.board_y + row * CELL_SIZE + CELL_SIZE // 2
        
        return (x, y)
    
    def draw_board(self):
        """Draw the game board with cells, snakes, and ladders."""
        # Draw board background
        pygame.draw.rect(self.screen, BOARD_COLOR, 
                        (self.board_x, self.board_y, BOARD_SIZE, BOARD_SIZE))
        
        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            # Horizontal lines
            pygame.draw.line(self.screen, GRID_COLOR, 
                            (self.board_x, self.board_y + i * CELL_SIZE),
                            (self.board_x + BOARD_SIZE, self.board_y + i * CELL_SIZE), 2)
            # Vertical lines
            pygame.draw.line(self.screen, GRID_COLOR, 
                            (self.board_x + i * CELL_SIZE, self.board_y),
                            (self.board_x + i * CELL_SIZE, self.board_y + BOARD_SIZE), 2)
        
        # Draw cell numbers
        for cell in range(1, 101):
            pos = self.get_cell_position(cell)
            if pos:
                # Alternate cell colors for better visibility
                row = (cell - 1) // GRID_SIZE
                col = (cell - 1) % GRID_SIZE
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.screen, (230, 220, 190), 
                                    (self.board_x + col * CELL_SIZE, 
                                     self.board_y + (GRID_SIZE - 1 - row) * CELL_SIZE, 
                                     CELL_SIZE, CELL_SIZE))
                
                # Draw cell number
                text = self.font.render(str(cell), True, BLACK)
                text_rect = text.get_rect(center=pos)
                self.screen.blit(text, text_rect)
        
        # Draw ladders (before snakes so snakes appear on top)
        for bottom, top in self.ladders.items():
            start_pos = self.get_cell_position(bottom)
            end_pos = self.get_cell_position(top)
            if start_pos and end_pos:
                # Draw ladder (two parallel lines with rungs)
                offset = 5  # Offset for parallel lines
                
                # Calculate angle and offsets
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                angle = math.atan2(dy, dx)
                
                # Perpendicular offsets
                perp_x = math.sin(angle) * offset
                perp_y = -math.cos(angle) * offset
                
                # Draw the two sides of the ladder
                pygame.draw.line(self.screen, LADDER_COLOR, 
                                (start_pos[0] + perp_x, start_pos[1] + perp_y),
                                (end_pos[0] + perp_x, end_pos[1] + perp_y), 4)
                pygame.draw.line(self.screen, LADDER_COLOR, 
                                (start_pos[0] - perp_x, start_pos[1] - perp_y),
                                (end_pos[0] - perp_x, end_pos[1] - perp_y), 4)
                
                # Draw rungs
                length = math.sqrt(dx*dx + dy*dy)
                num_rungs = int(length / 20)  # One rung every 20 pixels
                for i in range(1, num_rungs):
                    t = i / num_rungs
                    rung_x = start_pos[0] + dx * t
                    rung_y = start_pos[1] + dy * t
                    pygame.draw.line(self.screen, LADDER_COLOR, 
                                    (rung_x + perp_x, rung_y + perp_y),
                                    (rung_x - perp_x, rung_y - perp_y), 2)
        
        # Draw snakes
        for head, tail in self.snakes.items():
            start_pos = self.get_cell_position(head)
            end_pos = self.get_cell_position(tail)
            if start_pos and end_pos:
                # Calculate control points for curve
                ctrl_pt1 = (
                    (start_pos[0] + end_pos[0]) // 2 + random.randint(-50, 50),
                    (start_pos[1] + end_pos[1]) // 2 + random.randint(-50, 50)
                )
                
                # Draw snake body (curved line)
                points = []
                for t in range(0, 101, 5):  # Interpolate points along curve
                    t_float = t / 100.0
                    # Quadratic Bezier curve
                    x = (1-t_float)**2 * start_pos[0] + 2*(1-t_float)*t_float * ctrl_pt1[0] + t_float**2 * end_pos[0]
                    y = (1-t_float)**2 * start_pos[1] + 2*(1-t_float)*t_float * ctrl_pt1[1] + t_float**2 * end_pos[1]
                    points.append((int(x), int(y)))
                
                # Draw snake body
                if len(points) > 1:
                    pygame.draw.lines(self.screen, SNAKE_COLOR, False, points, 5)
                
                # Draw snake head
                pygame.draw.circle(self.screen, RED, start_pos, 8)
                
                # Draw snake tail
                pygame.draw.circle(self.screen, SNAKE_COLOR, end_pos, 5)
    
    def draw_players(self):
        """Draw player tokens on the board."""
        for player, position in self.player_positions.items():
            if position > 0:  # Only draw if player is on the board
                pos = self.get_cell_position(position)
                if pos:
                    # Calculate offset to avoid overlapping players
                    offset_x = ((player - 1) % 2) * 10 - 5
                    offset_y = ((player - 1) // 2) * 10 - 5
                    
                    # Draw player token
                    pygame.draw.circle(self.screen, PLAYER_COLORS[player-1], 
                                      (pos[0] + offset_x, pos[1] + offset_y), 10)
                    
                    # Draw player number
                    text = self.font.render(str(player), True, WHITE)
                    text_rect = text.get_rect(center=(pos[0] + offset_x, pos[1] + offset_y))
                    self.screen.blit(text, text_rect)
    
    def draw_dice(self):
        """Draw the dice and roll button."""
        # Dice position
        dice_x = 600
        dice_y = 150
        
        # Draw dice
        self.screen.blit(self.dice_images[self.dice_value - 1], (dice_x, dice_y))
        
        # Draw roll button
        button_x = dice_x
        button_y = dice_y + DICE_SIZE + 20
        pygame.draw.rect(self.screen, GREEN if not self.animation_in_progress else (150, 150, 150), 
                        (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        # Button text
        button_text = self.font.render("Roll Dice", True, BLACK)
        text_rect = button_text.get_rect(center=(button_x + BUTTON_WIDTH//2, button_y + BUTTON_HEIGHT//2))
        self.screen.blit(button_text, text_rect)
        
        return pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    def draw_player_info(self):
        """Draw player information."""
        info_x = 600
        info_y = 300
        
        # Title
        title_text = self.font.render("Player Information", True, BLACK)
        self.screen.blit(title_text, (info_x, info_y))
        
        # Player positions
        for player, position in self.player_positions.items():
            color = PLAYER_COLORS[player-1]
            status = "Not started" if position == 0 else f"Position: {position}"
            
            # Highlight current player
            if player == self.current_player:
                pygame.draw.rect(self.screen, (240, 240, 200), 
                                (info_x - 5, info_y + 30 + (player-1)*30 - 5, 200, 30))
            
            # Player color indicator
            pygame.draw.circle(self.screen, color, (info_x + 10, info_y + 30 + (player-1)*30 + 10), 10)
            
            # Player text
            player_text = self.font.render(f"Player {player}: {status}", True, BLACK)
            self.screen.blit(player_text, (info_x + 25, info_y + 30 + (player-1)*30))
    
    def draw_game_message(self):
        """Draw game messages."""
        message_x = 600
        message_y = 450
        
        if self.game_over:
            message = f"Player {self.winner} wins!"
            color = PLAYER_COLORS[self.winner-1]
        elif self.animation_in_progress:
            message = "Moving..."
            color = BLACK
        else:
            message = f"Player {self.current_player}'s turn"
            color = PLAYER_COLORS[self.current_player-1]
        
        # Draw message
        message_text = self.font.render(message, True, color)
        self.screen.blit(message_text, (message_x, message_y))
        
        # Draw restart button if game is over
        if self.game_over:
            button_x = message_x
            button_y = message_y + 40
            pygame.draw.rect(self.screen, BLUE, 
                            (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
            
            # Button text
            button_text = self.font.render("Play Again", True, WHITE)
            text_rect = button_text.get_rect(center=(button_x + BUTTON_WIDTH//2, button_y + BUTTON_HEIGHT//2))
            self.screen.blit(button_text, text_rect)
            
            return pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        return None
    
    def draw_menu(self):
        """Draw the main menu."""
        # Fill background
        self.screen.fill((230, 230, 250))
        
        # Title
        title_text = self.large_font.render("Snake and Ladder Game", True, PURPLE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Player selection text
        select_text = self.font.render("Select number of players:", True, BLACK)
        select_rect = select_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(select_text, select_rect)
        
        # Player number buttons
        buttons = []
        for i in range(4):
            button_x = SCREEN_WIDTH//2 - 175 + i * 100
            button_y = 250
            button_width = 80
            button_height = 50
            
            # Highlight selected player count
            color = GREEN if i+1 == self.total_players else BLUE
            
            pygame.draw.rect(self.screen, color, 
                            (button_x, button_y, button_width, button_height))
            
            # Button text
            button_text = self.font.render(f"{i+1}", True, WHITE)
            text_rect = button_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
            self.screen.blit(button_text, text_rect)
            
            buttons.append((pygame.Rect(button_x, button_y, button_width, button_height), i+1))
        
        # Start game button
        start_button_x = SCREEN_WIDTH//2 - BUTTON_WIDTH//2
        start_button_y = 350
        pygame.draw.rect(self.screen, GREEN, 
                        (start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        # Button text
        start_text = self.font.render("Start Game", True, BLACK)
        start_text_rect = start_text.get_rect(center=(start_button_x + BUTTON_WIDTH//2, start_button_y + BUTTON_HEIGHT//2))
        self.screen.blit(start_text, start_text_rect)
        
        return buttons, pygame.Rect(start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    def roll_dice_animation(self):
        """Animate dice rolling."""
        if self.dice_rolling:
            current_time = pygame.time.get_ticks()
            if current_time - self.roll_start_time > 1000:  # Roll for 1 second
                self.dice_rolling = False
                return True  # Finished rolling
            else:
                # Show random dice face during animation
                self.dice_value = random.randint(1, 6)
                return False  # Still rolling
        return True  # Not rolling
    
    def move_player_animation(self):
        """Animate player movement."""
        if self.animation_in_progress:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.animation_start_time
            
            if elapsed > 1000:  # Animation duration
                self.animation_in_progress = False
                
                # Check if player landed on a snake or ladder
                if self.animation_to in self.snakes:
                    # Start snake animation
                    self.animation_in_progress = True
                    self.animation_start_time = current_time
                    self.animation_from = self.animation_to
                    self.animation_to = self.snakes[self.animation_to]
                    return False
                
                elif self.animation_to in self.ladders:
                    # Start ladder animation
                    self.animation_in_progress = True
                    self.animation_start_time = current_time
                    self.animation_from = self.animation_to
                    self.animation_to = self.ladders[self.animation_to]
                    return False
                
                # Update player position after animation
                self.player_positions[self.animation_player] = self.animation_to
                
                # Check win condition
                if self.animation_to >= 100:
                    self.game_over = True
                    self.winner = self.animation_player
                    return True
                
                # Move to next player if current player didn't roll a 6
                if self.dice_value != 6:
                    self.current_player = (self.current_player % self.total_players) + 1
                
                return True  # Animation finished
            
            # During animation, update the visual position
            # For simplicity, we'll just update the actual position
            # A more complex animation could interpolate between positions
            self.player_positions[self.animation_player] = self.animation_from
            
            return False  # Animation still in progress
        
        return True  # No animation in progress
    
    def handle_dice_roll(self):
        """Handle dice roll logic."""
        # Start dice rolling animation
        self.dice_rolling = True
        self.roll_start_time = pygame.time.get_ticks()
        
        # Get final dice value
        self.dice_value = random.randint(1, 6)
        
        # Handle player movement based on dice roll
        current_pos = self.player_positions[self.current_player]
        
        # Player needs a 6 to start
        if current_pos == 0 and self.dice_value != 6:
            # Player stays at position 0
            self.current_player = (self.current_player % self.total_players) + 1
            return
        
        # Player gets to enter the board with a 6
        if current_pos == 0 and self.dice_value == 6:
            new_pos = 1
        else:
            new_pos = current_pos + self.dice_value
            
            # Check if player overshoots the board
            if new_pos > 100:
                new_pos = current_pos  # Stay in place if overshooting
        
        # Start movement animation
        self.animation_in_progress = True
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_from = current_pos
        self.animation_to = new_pos
        self.animation_player = self.current_player
    
    def reset_game(self):
        """Reset the game state."""
        self.player_positions = {i+1: 0 for i in range(self.total_players)}
        self.current_player = 1
        self.dice_value = 1
        self.game_over = False
        self.winner = None
        self.animation_in_progress = False
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.show_menu:
                        # Handle menu clicks
                        player_buttons, start_button = self.draw_menu()
                        
                        # Check player number buttons
                        for button, num_players in player_buttons:
                            if button.collidepoint(mouse_pos):
                                self.total_players = num_players
                                self.player_positions = {i+1: 0 for i in range(self.total_players)}
                        
                        # Check start button
                        if start_button.collidepoint(mouse_pos):
                            self.show_menu = False
                            self.reset_game()
                    
                    else:
                        # Handle game clicks
                        if not self.animation_in_progress:
                            # Check dice roll button
                            roll_button = self.draw_dice()
                            if roll_button.collidepoint(mouse_pos) and not self.game_over:
                                self.handle_dice_roll()
                            
                            # Check restart button if game is over
                            restart_button = self.draw_game_message()
                            if restart_button and restart_button.collidepoint(mouse_pos):
                                self.reset_game()
            
            # Clear screen
            self.screen.fill(WHITE)
            
            if self.show_menu:
                self.draw_menu()
            else:
                # Update animations
                dice_done = self.roll_dice_animation()
                move_done = self.move_player_animation()
                
                # Draw game elements
                self.draw_board()
                self.draw_players()
                self.draw_dice()
                self.draw_player_info()
                self.draw_game_message()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeAndLadderGUI()
    game.run()
