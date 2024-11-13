import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set display dimensions
width = 600
height = 400
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Game settings
snake_block = 10
snake_speed = 15

# Initialize clock
clock = pygame.time.Clock()

# Define font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# High score file path
high_score_file = "high_score.txt"


def load_high_score():
    # Load high score from a file, or set it to 0 if the file doesn't exist
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as f:
            return int(f.read())
    return 0


def save_high_score(high_score):
    # Save the high score to a file
    with open(high_score_file, 'w') as f:
        f.write(str(high_score))


# Display current score
def display_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


# Display high score
def display_high_score(high_score):
    value = score_font.render("High Score: " + str(high_score), True, yellow)
    dis.blit(value, [width - 200, 0])


# Function to draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color, pos):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, pos)


# Main menu screen
def main_menu():
    dis.fill(blue)
    message("Welcome to Snake Game!", yellow, [width / 3, height / 4])
    message("Press P to Play", white, [width / 3, height / 2])
    message("Press Q to Quit", white, [width / 3, height / 1.5])
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Start game
                    gameLoop()
                elif event.key == pygame.K_q:  # Quit game
                    pygame.quit()
                    quit()


def gameLoop():
    # Load high score
    high_score = load_high_score()

    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    score = 0

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red, [width / 6, height / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()  # Restart the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        display_score(score)
        display_high_score(high_score)  # Display the high score

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 10

            # Update high score if the current score is higher
            if score > high_score:
                high_score = score
                save_high_score(high_score)  # Save the new high score

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game with the main menu
main_menu()
