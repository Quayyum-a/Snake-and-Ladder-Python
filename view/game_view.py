import pygame
from utils.constants import WINDOW_SIZE, SQUARE_SIZE, COLORS, BOARD_SIZE

class GameView:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1] + 100))  # Extra space for UI elements
        pygame.display.set_caption("Snake and Ladder Game")
        self.font = pygame.font.SysFont("arial", 20)
        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.dice_images = self.load_dice_images()

    def draw_board(self):
        self.screen.fill(COLORS["WHITE"])

        # Draw title
        title = self.title_font.render("Snake and Ladder Game", True, COLORS["BLUE"])
        self.screen.blit(title, (WINDOW_SIZE[0] // 2 - 150, WINDOW_SIZE[1] + 10))

        # Draw board with alternating colors
        for row in range(10):
            for col in range(10):
                number = 100 - (row * 10 + (9 - col) if row % 2 == 0 else row * 10 + col)
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE

                # Alternating colors for squares
                if (row + col) % 2 == 0:
                    color = COLORS["LIGHT_BLUE"]
                else:
                    color = COLORS["LIGHT_YELLOW"]

                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(self.screen, COLORS["BLACK"], (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)

                # Draw number
                text = self.font.render(str(number), True, COLORS["BLACK"])
                self.screen.blit(text, (x + 10, y + 10))

    def draw_players(self, players):
        for i, player in enumerate(players):
            row, col = self.get_position_coordinates(player.position)
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2

            # Draw a more appealing player token
            pygame.draw.circle(self.screen, player.color, (x, y), 15)
            pygame.draw.circle(self.screen, COLORS["BLACK"], (x, y), 15, 2)

            # Add player number inside the token
            player_num = self.font.render(str(i+1), True, COLORS["WHITE"])
            self.screen.blit(player_num, (x - 5, y - 8))

    def draw_dice(self, dice_result, current_player):
        # Draw player turn indicator
        turn_text = self.font.render(f"{current_player.name}'s Turn", True, current_player.color)
        self.screen.blit(turn_text, (20, WINDOW_SIZE[1] + 50))

        # Draw dice images
        die1, die2 = dice_result

        # Draw first die
        self.screen.blit(self.dice_images[die1-1], (WINDOW_SIZE[0] // 2 - 60, WINDOW_SIZE[1] + 40))

        # Draw second die
        self.screen.blit(self.dice_images[die2-1], (WINDOW_SIZE[0] // 2 + 10, WINDOW_SIZE[1] + 40))

        # Draw total
        total_text = self.font.render(f"Total: {die1 + die2}", True, COLORS["BLACK"])
        self.screen.blit(total_text, (WINDOW_SIZE[0] // 2 - 30, WINDOW_SIZE[1] + 10))

    def draw_snakes_ladders(self, snakes, ladders):
        # Draw snakes as curved lines with a head
        for start, end in snakes.items():
            start_row, start_col = self.get_position_coordinates(start)
            end_row, end_col = self.get_position_coordinates(end)

            start_x = start_col * SQUARE_SIZE + SQUARE_SIZE // 2
            start_y = start_row * SQUARE_SIZE + SQUARE_SIZE // 2
            end_x = end_col * SQUARE_SIZE + SQUARE_SIZE // 2
            end_y = end_row * SQUARE_SIZE + SQUARE_SIZE // 2

            # Draw a wavy snake line
            control_x = (start_x + end_x) // 2 + 20
            control_y = (start_y + end_y) // 2

            # Draw snake body (curved line)
            points = []
            for t in range(0, 101, 5):
                t = t / 100
                # Quadratic Bezier curve
                x = (1-t)**2 * start_x + 2*(1-t)*t*control_x + t**2 * end_x
                y = (1-t)**2 * start_y + 2*(1-t)*t*control_y + t**2 * end_y
                points.append((x, y))

            if len(points) > 1:
                pygame.draw.lines(self.screen, COLORS["RED"], False, points, 4)

            # Draw snake head
            pygame.draw.circle(self.screen, COLORS["RED"], (end_x, end_y), 8)
            pygame.draw.circle(self.screen, COLORS["BLACK"], (end_x - 3, end_y - 3), 2)
            pygame.draw.circle(self.screen, COLORS["BLACK"], (end_x + 3, end_y - 3), 2)

        # Draw ladders as two parallel lines with rungs
        for start, end in ladders.items():
            start_row, start_col = self.get_position_coordinates(start)
            end_row, end_col = self.get_position_coordinates(end)

            start_x = start_col * SQUARE_SIZE + SQUARE_SIZE // 2
            start_y = start_row * SQUARE_SIZE + SQUARE_SIZE // 2
            end_x = end_col * SQUARE_SIZE + SQUARE_SIZE // 2
            end_y = end_row * SQUARE_SIZE + SQUARE_SIZE // 2

            # Calculate ladder sides
            angle = pygame.math.Vector2(end_x - start_x, end_y - start_y).normalize()
            perpendicular = pygame.math.Vector2(-angle.y, angle.x) * 8

            # Draw ladder sides
            pygame.draw.line(self.screen, COLORS["ORANGE"],
                            (start_x + perpendicular.x, start_y + perpendicular.y),
                            (end_x + perpendicular.x, end_y + perpendicular.y), 3)
            pygame.draw.line(self.screen, COLORS["ORANGE"],
                            (start_x - perpendicular.x, start_y - perpendicular.y),
                            (end_x - perpendicular.x, end_y - perpendicular.y), 3)

            # Draw ladder rungs
            length = pygame.math.Vector2(end_x - start_x, end_y - start_y).length()
            num_rungs = int(length / 20)
            for i in range(num_rungs):
                t = i / (num_rungs - 1) if num_rungs > 1 else 0
                rung_x = start_x + (end_x - start_x) * t
                rung_y = start_y + (end_y - start_y) * t
                pygame.draw.line(self.screen, COLORS["ORANGE"],
                                (rung_x + perpendicular.x, rung_y + perpendicular.y),
                                (rung_x - perpendicular.x, rung_y - perpendicular.y), 2)

    def draw_message(self, message):
        # Create a semi-transparent overlay
        overlay = pygame.Surface(WINDOW_SIZE)
        overlay.set_alpha(180)
        overlay.fill(COLORS["BLACK"])
        self.screen.blit(overlay, (0, 0))

        # Draw message in a box
        message_box = pygame.Surface((400, 100))
        message_box.fill(COLORS["LIGHT_BLUE"])
        pygame.draw.rect(message_box, COLORS["BLUE"], (0, 0, 400, 100), 4)

        # Render message text
        text = self.title_font.render(message, True, COLORS["BLUE"])
        message_box.blit(text, (200 - text.get_width() // 2, 50 - text.get_height() // 2))

        # Display the message box
        self.screen.blit(message_box, (WINDOW_SIZE[0] // 2 - 200, WINDOW_SIZE[1] // 2 - 50))

    def get_position_coordinates(self, position):
        row = 9 - (position - 1) // 10
        col = (position - 1) % 10 if row % 2 == 0 else 9 - (position - 1) % 10
        return row, col

    def load_dice_images(self):
        # Create simple dice images
        dice_images = []
        for i in range(1, 7):
            # Create a surface for the die
            die_surface = pygame.Surface((50, 50))
            die_surface.fill(COLORS["WHITE"])
            pygame.draw.rect(die_surface, COLORS["BLACK"], (0, 0, 50, 50), 2)

            # Draw dots based on die value
            if i == 1:
                pygame.draw.circle(die_surface, COLORS["BLACK"], (25, 25), 5)
            elif i == 2:
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 15), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 35), 5)
            elif i == 3:
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 15), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (25, 25), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 35), 5)
            elif i == 4:
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 15), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 35), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 15), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 35), 5)
            elif i == 5:
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 15), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 35), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (25, 25), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 15), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 35), 5)
            elif i == 6:
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 15), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 25), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (15, 35), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 15), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 25), 5)
                pygame.draw.circle(die_surface, COLORS["BLACK"], (35, 35), 5)

            dice_images.append(die_surface)
        return dice_images

    def draw_turn_indicator(self, current_player):
        # Draw a box showing whose turn it is
        pygame.draw.rect(self.screen, COLORS["LIGHT_GREEN"], 
                         (20, WINDOW_SIZE[1] + 40, 200, 40))
        pygame.draw.rect(self.screen, current_player.color, 
                         (20, WINDOW_SIZE[1] + 40, 200, 40), 3)

        # Draw text
        turn_text = self.font.render(f"{current_player.name}'s Turn", True, COLORS["BLACK"])
        self.screen.blit(turn_text, (30, WINDOW_SIZE[1] + 50))

        # Draw prompt
        prompt = self.font.render("Press SPACE to roll dice", True, COLORS["BLACK"])
        self.screen.blit(prompt, (WINDOW_SIZE[0] - 220, WINDOW_SIZE[1] + 50))

    def draw_instructions(self, instructions):
        # Create a semi-transparent overlay
        overlay = pygame.Surface(WINDOW_SIZE)
        overlay.set_alpha(200)
        overlay.fill(COLORS["BLACK"])
        self.screen.blit(overlay, (0, 0))

        # Draw instructions box
        box_width, box_height = 500, 300
        instruction_box = pygame.Surface((box_width, box_height))
        instruction_box.fill(COLORS["LIGHT_BLUE"])
        pygame.draw.rect(instruction_box, COLORS["BLUE"], (0, 0, box_width, box_height), 4)

        # Draw title
        title = self.title_font.render(instructions[0], True, COLORS["BLUE"])
        instruction_box.blit(title, (box_width // 2 - title.get_width() // 2, 20))

        # Draw instructions
        for i, line in enumerate(instructions[1:]):
            text = self.font.render(line, True, COLORS["BLACK"])
            instruction_box.blit(text, (30, 70 + i * 30))

        # Display the instruction box
        self.screen.blit(instruction_box, (WINDOW_SIZE[0] // 2 - box_width // 2, 
                                          WINDOW_SIZE[1] // 2 - box_height // 2))

    def update(self):
        pygame.display.flip()
