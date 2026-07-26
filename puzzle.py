"""Puzzle System"""
import random
from constants import *

class Puzzle:
    """Base puzzle class"""
    def __init__(self, puzzle_id, description):
        self.puzzle_id = puzzle_id
        self.description = description
        self.solved = False

    def solve(self):
        """Solve puzzle"""
        self.solved = True

    def get_ui_text(self):
        """Get puzzle UI text"""
        return self.description


class MathPuzzle(Puzzle):
    """Math puzzle"""
    def __init__(self, puzzle_id="math1"):
        self.num1 = random.randint(5, 20)
        self.num2 = random.randint(5, 20)
        self.operation = random.choice(['+', '-', '*'])
        
        if self.operation == '+':
            self.answer = self.num1 + self.num2
        elif self.operation == '-':
            self.answer = self.num1 - self.num2
        else:
            self.answer = self.num1 * self.num2
        
        desc = f"Solve the math puzzle: {self.num1} {self.operation} {self.num2} = ?"
        super().__init__(puzzle_id, desc)
        self.user_answer = None

    def check_answer(self, answer):
        """Check if answer is correct"""
        try:
            num = int(answer)
            if num == self.answer:
                self.solve()
                return True
        except:
            pass
        return False


class SequencePuzzle(Puzzle):
    """Sequence puzzle - click buttons in correct order"""
    def __init__(self, puzzle_id="seq1"):
        super().__init__(puzzle_id, "Click the buttons in order: 1, 2, 3, 4")
        self.correct_sequence = [1, 2, 3, 4]
        self.user_sequence = []

    def add_click(self, button_num):
        """Add click to sequence"""
        self.user_sequence.append(button_num)
        
        # Check if correct so far
        if button_num != self.correct_sequence[len(self.user_sequence) - 1]:
            self.user_sequence = []
            return False
        
        # Check if complete
        if len(self.user_sequence) == len(self.correct_sequence):
            self.solve()
            return True
        
        return True

    def reset(self):
        """Reset sequence"""
        self.user_sequence = []


class MemoryPuzzle(Puzzle):
    """Memory puzzle - remember and repeat pattern"""
    def __init__(self, puzzle_id="mem1"):
        super().__init__(puzzle_id, "Repeat the pattern!")
        self.pattern = [random.randint(1, 4) for _ in range(4)]
        self.user_pattern = []

    def add_click(self, button_num):
        """Add click to pattern"""
        self.user_pattern.append(button_num)
        
        # Check if correct so far
        if button_num != self.pattern[len(self.user_pattern) - 1]:
            self.user_pattern = []
            return False
        
        # Check if complete
        if len(self.user_pattern) == len(self.pattern):
            self.solve()
            return True
        
        return True

    def reset(self):
        """Reset pattern"""
        self.user_pattern = []

    def get_display_pattern(self):
        """Get pattern to display"""
        return self.pattern


class DoorPuzzle:
    """Door that requires puzzle to open"""
    def __init__(self, x, y, width=40, height=100, puzzle=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.puzzle = puzzle
        self.opened = False
        self.color = GRAY

    def update(self, dt):
        """Update door"""
        if self.puzzle and self.puzzle.solved:
            self.opened = True
            self.color = GREEN

    def draw(self, surface):
        """Draw door"""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)

    def get_rect(self):
        """Get door rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def blocks_player(self, player_rect):
        """Check if door blocks player"""
        if not self.opened:
            return self.get_rect().colliderect(player_rect)
        return False

    def is_open(self):
        """Check if open"""
        return self.opened


# Puzzle factory
def create_puzzle(puzzle_type):
    """Create puzzle by type"""
    if puzzle_type == "math":
        return MathPuzzle()
    elif puzzle_type == "sequence":
        return SequencePuzzle()
    elif puzzle_type == "memory":
        return MemoryPuzzle()
    else:
        return MathPuzzle()
