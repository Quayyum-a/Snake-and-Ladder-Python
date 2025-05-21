from utils.constants import BOARD_SIZE, SNAKES, LADDERS

class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.snakes = SNAKES
        self.ladders = LADDERS

    def get_new_position(self, current_position):
        """Check if the position lands on a snake or ladder and return new position."""
        if current_position in self.snakes:
            return self.snakes[current_position]
        if current_position in self.ladders:
            return self.ladders[current_position]
        return current_position

    def is_winning_position(self, position):
        """Check if the position is the winning square."""
        return position >= self.size * self.size