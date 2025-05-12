import pygame
import random

class Board:
    def __init__(self):
        self.snakes = {}
        self.ladders = {}
        self.generate_snakes_and_ladders()
        self.power_ups = {
            11: "challenge",
            26: "boost",
            45: "challenge",
            66: "boost",
            77: "challenge",
            88: "boost"}

    def generate_snakes_and_ladders(self, num_snakes=3, num_ladders=3):
        self.snakes.clear()
        self.ladders.clear()
        used_positions = set()

        while len(self.ladders) < num_ladders:
            start = random.randint(2, 90)
            end = start + random.randint(5, 20)
            if end > 100 or start in used_positions or end in used_positions:
                continue
            self.ladders[start] = end
            used_positions.update([start, end])

        while len(self.snakes) < num_snakes:
            head = random.randint(20, 98)
            tail = head - random.randint(5, 20)
            if tail < 1 or head in used_positions or tail in used_positions:
                continue
            self.snakes[head] = tail
            used_positions.update([head, tail])

    def check_snake_or_ladder(self, position):
        if position in self.snakes:
            pygame.mixer.Sound("sounds/snake.wav").play()
            return self.snakes[position]
        elif position in self.ladders:
            pygame.mixer.Sound("sounds/ladder.wav").play()
            return self.ladders[position]
        return position
    
    def get_power_up(self, position):
        return self.power_ups.get(position, None)

    
    
def draw_board(screen, board, cell_size = 60):
        font = pygame.font.SysFont('Arial', 16)
        screen.fill((255, 255, 255)) 

        rows, cols = 10, 10
        number = 1
 
        for row in range(rows):
            y = row * cell_size
            row_num = 9 - row 
            for col in range(cols):
                if row_num % 2 == 0:
                    x = col * cell_size
                    board_number = row_num * 10 + col + 1
                else:
                    x = (9 - col) * cell_size
                    board_number = row_num * 10 + col + 1
                pygame.draw.rect(screen, (200, 200, 200), (x, y, cell_size, cell_size), 1)
                number_text = font.render(str(board_number), True, (0, 0, 0))
                screen.blit(number_text, (x + 5, y + 5))

                if board_number in board.power_ups:
                    kind = board.power_ups[board_number]
                    color = (255, 215, 0) if kind == "challenge" else (0, 255, 0)
                    pygame.draw.circle(screen, color, (x + cell_size // 2, y + cell_size // 2), 8)

        # Draw snakes
        for start, end in board.snakes.items():
            start_x, start_y = get_cell_center(start, cell_size)
            end_x, end_y = get_cell_center(end, cell_size)
            pygame.draw.line(screen, (255, 0, 0), (start_x, start_y), (end_x, end_y), 5)
        
        # Draw ladders
        for start, end in board.ladders.items():
            start_x, start_y = get_cell_center(start, cell_size)
            end_x, end_y = get_cell_center(end, cell_size)
            pygame.draw.line(screen, (0, 255, 0), (start_x, start_y), (end_x, end_y), 5)


def get_cell_center(pos, cell_size=60):
    row = (pos - 1) // 10
    col = (pos - 1) % 10 if row % 2 == 0 else 9 - ((pos - 1) % 10)
    x = col * cell_size + cell_size // 2
    y = 540 - row * cell_size + cell_size // 2
    return x, y

