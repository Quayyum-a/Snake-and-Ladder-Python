import pygame
from model.dice import Dice

class GameController:
    def __init__(self, board, players, view):
        self.board = board
        self.players = players
        self.view = view
        self.dice = Dice()
        self.current_player_index = 0
        self.dice_result = None
        self.game_over = False
        self.show_instructions = True
        self.animation_timer = 0
        self.waiting_for_next_turn = False

    def update(self):
        # Handle game over state
        if self.game_over:
            self.view.draw_board()
            self.view.draw_snakes_ladders(self.board.snakes, self.board.ladders)
            self.view.draw_players(self.players)
            self.view.draw_message(f"{self.players[self.current_player_index].name} wins!")
            self.view.update()

            # Check for restart
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart_game()
            return

        # Draw the game board and elements
        self.view.draw_board()
        self.view.draw_snakes_ladders(self.board.snakes, self.board.ladders)
        self.view.draw_players(self.players)

        # Show current player's turn
        current_player = self.players[self.current_player_index]

        # Draw turn indicator even if dice haven't been rolled
        if not self.dice_result:
            self.view.draw_turn_indicator(current_player)
        else:
            self.view.draw_dice(self.dice_result, current_player)

        # Show instructions if needed
        if self.show_instructions:
            self.draw_instructions()

        self.view.update()

        # Handle waiting between turns
        if self.waiting_for_next_turn:
            self.animation_timer += 1
            if self.animation_timer > 60:  # Wait about 1 second
                self.animation_timer = 0
                self.waiting_for_next_turn = False
                self.dice_result = None
            return

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Roll dice if not already rolled
                    if not self.dice_result and not self.waiting_for_next_turn:
                        self.show_instructions = False
                        die1, die2, total = self.dice.roll()
                        self.dice_result = (die1, die2)

                        # Move player
                        current_player.move(total)

                        # Check for snakes and ladders
                        new_position = self.board.get_new_position(current_player.position)
                        if new_position != current_player.position:
                            # Player landed on a snake or ladder
                            current_player.position = new_position

                        # Check for win
                        if self.board.is_winning_position(current_player.position):
                            self.game_over = True
                        else:
                            # Set up for next turn
                            self.waiting_for_next_turn = True
                            self.current_player_index = (self.current_player_index + 1) % len(self.players)
                elif event.key == pygame.K_h:
                    # Toggle instructions
                    self.show_instructions = not self.show_instructions

    def draw_instructions(self):
        instructions = [
            "Snake and Ladder Game Instructions:",
            "1. Press SPACE to roll the dice",
            "2. Land on a ladder to climb up",
            "3. Land on a snake to slide down",
            "4. First player to reach 100 wins",
            "5. Press H to toggle instructions",
            "6. Press R to restart game when over"
        ]
        self.view.draw_instructions(instructions)

    def restart_game(self):
        # Reset game state
        for player in self.players:
            player.position = 1
        self.current_player_index = 0
        self.dice_result = None
        self.game_over = False
        self.show_instructions = True
        self.animation_timer = 0
        self.waiting_for_next_turn = False
