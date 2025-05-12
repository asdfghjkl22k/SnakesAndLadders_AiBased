import random
import pygame
import os

class Dice:
    def __init__(self):
        self.last_roll = 1
        self.dice_images = []
        self.dice_rect = pygame.Rect(620, 250, 80, 80) 
        for i in range(1, 7):
            path = os.path.join("assets", "dice_faces", f"{i}.png")
            self.dice_images.append(pygame.image.load(path))

    def roll(self):
        self.last_roll = random.randint(1, 6)
        print(f"Dice rolled: {self.last_roll}")
        return self.last_roll

    def draw(self, screen):
        image = self.dice_images[self.last_roll - 1]
        image = pygame.transform.scale(image, (80, 80))
        screen.blit(image, self.dice_rect.topleft)

    def is_clicked(self, mouse_pos):
        return self.dice_rect.collidepoint(mouse_pos)
