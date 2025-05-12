import pygame
import game.board as Board

class Player:
    def __init__(self, name, color=(0, 0, 255)):
        self.name = name
        self.position = 1
        self.color = color

    def move(self, steps, board):
        new_position = self.position + steps
        if new_position <= 100:
            self.position = board.check_snake_or_ladder(new_position)

    def get_coords(self):
        row = (self.position - 1) // 10
        col = (self.position - 1) % 10 if row % 2 == 0 else 9 - ((self.position - 1) % 10)
        x = col * 60 + 30  
        y = 540 - row * 60
        return x, y

    def draw(self, screen):
        x, y = self.get_coords()
        pygame.draw.circle(screen, self.color, (x, y), 15)
