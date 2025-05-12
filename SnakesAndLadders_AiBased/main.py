import pygame
from game.board import Board, draw_board
from game.player import Player
from game.ai_agent import AIPlayer
from game.dice import Dice

STORY_BOX_X = 0
STORY_BOX_Y = 600
STORY_BOX_WIDTH = 800
STORY_BOX_HEIGHT = 100
SCROLLBAR_WIDTH = 10
MAX_LINES_ON_SCREEN = 6
LINE_HEIGHT = 18

pygame.mixer.pre_init(44100, -16, 2, 512)  # Setup mixer before pygame.init()
pygame.init()
pygame.font.init()

dice_sound = pygame.mixer.Sound("sounds/dice_roll.wav")
snake_sound = pygame.mixer.Sound("sounds/snake.wav")
ladder_sound = pygame.mixer.Sound("sounds/ladder.wav")
win_sound = pygame.mixer.Sound("sounds/win.wav")


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 700))  # wider window for dice
    pygame.display.set_caption("AI Snakes and Ladders")
    import random

    challenge_questions = [
        {
            "question": "What is the capital of France?",
            "options": ["A. Paris", "B. Berlin", "C. Rome", "D. Madrid"],
            "answer": "A"
        },
        {
            "question": "What is 5 + 7?",
            "options": ["A. 10", "B. 12", "C. 14", "D. 11"],
            "answer": "B"
        }
    ]

    board = Board()
    dice = Dice()
    players = [Player("Human", color=(0, 0, 255)), AIPlayer("AI", color=(255, 0, 0))]

    story_log = []
    scroll_offset = 0
    MAX_LINES_ON_SCREEN = 6
    running = True

    # Define the story font
    story_font = pygame.font.SysFont('Arial', 18)
    board_updated_this_turn = False
    turn = 0
    turnCount = 0
    last_board_update_turn = -1
    waiting_for_roll = True

    def add_to_story(text):
        header = story_font.render("📜 Game Commentary", True, (80, 0, 80))
        screen.blit(header, (10, 590))
        if len(story_log) > 6:
          story_log.pop(0)
        story_log.append(text)

    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y  # Scroll up/down

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scroll_offset -= 1
                elif event.key == pygame.K_DOWN:
                    scroll_offset += 1

            scroll_offset = max(0, min(len(story_log) - MAX_LINES_ON_SCREEN, scroll_offset))

            if event.type == pygame.QUIT:
                running = False

            # Human turn
            if waiting_for_roll and turn % 2 == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                if dice.is_clicked(event.pos):
                    roll = dice.roll()
                    dice_sound.play()
                    old_pos = player.position
                    players[0].move(roll, board)
                    new_pos = player.position

                    if new_pos < old_pos:
                        add_to_story(f"🐍 {player.name} hit a snake! Slid to {new_pos}.")
                    elif new_pos > old_pos + roll:
                        add_to_story(f"🪜 {player.name} climbed a ladder to {new_pos}.")
                    
                    add_to_story(f"{players[turn % 2].name} rolled a {roll}.")
                    if board.get_power_up(players[turn % 2].position) == "boost":
                        add_to_story(f"{players[turn % 2].name} landed on a power boost and surged ahead!")
                    elif board.get_power_up(players[turn % 2].position) == "challenge":
                        add_to_story(f"{players[turn % 2].name} is facing a challenge...")

                    power_up = board.get_power_up(players[0].position)
                    if power_up == "challenge":
                        print("Challenge time!")
                        q = random.choice(challenge_questions)
                        print(q["question"])
                        for opt in q["options"]:
                            print(opt)
                        ans = input("Your answer (A/B/C/D): ").strip().upper()
                        if ans == q["answer"]:
                            print("Correct! You get a bonus roll.")
                            bonus_roll = dice.roll()
                            players[0].move(bonus_roll, board)
                        else:
                            print("Wrong! You lose your next turn.")
                            turn += 1  # Skip next turn
                    elif power_up == "boost":
                        add_to_story(f"⚡ {player.name} activated a power boost!")
                        players[0].move(5, board)
                    waiting_for_roll = False
                    if players[0].position >= 100:
                        win_sound.play()
                        add_to_story(f"🏆 {player.name} wins the game!")
                        running = False
                    else:
                        turn += 1
                        turnCount += 1
                        waiting_for_roll = True
                        board_updated_this_turn = False

        # AI turn
        if waiting_for_roll and turn % 2 == 1:
            pygame.time.delay(2000)
            roll = dice.roll()
            add_to_story(f"{player.name} rolled a {roll}.")
            dice_sound.play()
            old_pos = players[1].position
            players[1].move(roll, board)
            new_pos = players[1].position

            if new_pos < old_pos:
                add_to_story(f"🐍 {player.name} hit a snake! Slid to {new_pos}.")
            elif new_pos > old_pos + roll:
                add_to_story(f"🪜 {player.name} climbed a ladder to {new_pos}.")
        
            add_to_story(f"{player.name} moved to square {player.position}.")
            power_up = board.get_power_up(players[1].position)
            if power_up == "challenge":
                print("AI encountered a challenge... it failed and skips next turn.")
                turn += 1  # You can make AI smarter later
            elif power_up == "boost":
                print("AI got a power boost! Jumping ahead by +5.")
                players[1].move(5, board)
            if players[1].position >= 100:
                win_sound.play()
                add_to_story(f"🏆 {player.name} wins the game!")
                running = False
            else:
                turn += 1
                turnCount += 1
                waiting_for_roll = True
                board_updated_this_turn = False

        # Board update after every 3 turns
        if turnCount % 3 == 0 and turnCount != 0 and turnCount != last_board_update_turn:
            add_to_story("🔁 Snakes and ladders were repositioned!")
            board.generate_snakes_and_ladders()
            last_board_update_turn = turnCount

        draw_board(screen, board)

        for player in players:
            player.draw(screen)

        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Dice Roll:", True, (0, 0, 0))
        screen.blit(text, (620, 200))
        dice.draw(screen)

        # Draw story window box
        pygame.draw.rect(screen, (245, 245, 245), (0, 600, 800, 100))  # Light gray background
        pygame.draw.rect(screen, (0, 0, 0), (0, 600, 800, 100), 2)     

        start_idx = scroll_offset
        end_idx = min(len(story_log), scroll_offset + MAX_LINES_ON_SCREEN)

        # Render visible lines
        start_idx = scroll_offset
        end_idx = min(len(story_log), scroll_offset + MAX_LINES_ON_SCREEN)
        y = STORY_BOX_Y + 5
        for i in range(start_idx, end_idx):
            line = story_log[i]
            text = story_font.render(line, True, (0, 0, 0))
            screen.blit(text, (10, y))
            y += LINE_HEIGHT

        # Draw scrollbar
        total_lines = len(story_log)
        if total_lines > MAX_LINES_ON_SCREEN:
            track_height = STORY_BOX_HEIGHT
            thumb_height = max(int(track_height * (MAX_LINES_ON_SCREEN / total_lines)), 20)
            scroll_max = total_lines - MAX_LINES_ON_SCREEN
            scroll_ratio = scroll_offset / scroll_max if scroll_max > 0 else 0
            thumb_y = STORY_BOX_Y + int((track_height - thumb_height) * scroll_ratio)

            # Scroll track
            pygame.draw.rect(screen, (200, 200, 200), (STORY_BOX_WIDTH - SCROLLBAR_WIDTH, STORY_BOX_Y, SCROLLBAR_WIDTH, STORY_BOX_HEIGHT))

            # Scroll thumb
            pygame.draw.rect(screen, (100, 100, 100), (STORY_BOX_WIDTH - SCROLLBAR_WIDTH, thumb_y, SCROLLBAR_WIDTH, thumb_height))

        pygame.display.flip()

    pygame.time.delay(1000)

    pygame.quit()

if __name__ == "__main__":
    main()
