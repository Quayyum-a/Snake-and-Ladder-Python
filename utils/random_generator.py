import random

class RandomGenerator:
    def get_number(self, min_val, max_val):
        return random.randint(min_val, max_val)