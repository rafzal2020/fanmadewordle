import pygame
import random

import words

pygame.init()

#  Game settings with color and resolution
white = (255,255,255)
black = (0,0,0)
green = (83,141,78)
yellow = (181,159,59)
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")
turn = 0
"""A matrix of the 6 rows of 5-word-columns."""
board = [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "]]

fps = 60
timer = pygame.time.Clock()
title_font = pygame.font.Font('freesansbold.ttf', 56)
status_font = pygame.font.Font('freesansbold.ttf', 40)
secret_word = words.WORD[random.randint(0, len(words.WORD) - 1)].upper()
game_over = False
letters = 0
turn_active = True

def draw_board():
    global turn
    global board
    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(screen, white, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 5)
            piece_text = title_font.render(board[row][col], True, white)
            screen.blit(piece_text, (col * 100 + 25, row * 100 + 25))
    pygame.draw.rect(screen, green, [5, turn * 100 + 5, WIDTH - 10, 90], 3, 5)

def check_words():
    global turn
    global board
    global secret_word
    for col in range(0, 5):
        for row in range(0, 6):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(screen, green, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)
            elif board[row][col] in secret_word and turn > row:
                pygame.draw.rect(screen, yellow, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 5)
            

running = True
while running:
    timer.tick(fps)
    screen.fill(black)
    check_words()
    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            entry = event.__getattribute__('text')
            board[turn][letters] = entry.title()
            letters += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letters > 0:
                board[turn][letters - 1] = ' '
                letters -= 1
            if event.key == pygame.K_RETURN and letters == 5 and not game_over :
                turn += 1
                letters = 0
               

            if event.key == pygame.K_RETURN and game_over:
                turn = 0
                letters = 0
                game_over = False
                secret_word = words.WORD[random.randint(0, len(words.WORD) - 1)].upper()
                board = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]
            

    for row in range(0,6):
        guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
        if guess == secret_word and row < turn:
            game_over = True

    if letters == 5:
        turn_active = False
    if letters < 5:
        turn_active = True

    if turn == 6 and guess != secret_word:
        game_over = True
        game_over_text = status_font.render(f"The word was {secret_word.title()}.", True, white)
        screen.blit(game_over_text, (20, 610))
    
    if game_over and turn < 6 or (turn == 6 and guess == secret_word):
        winner_text = title_font.render("Good job!", True, white)
        screen.blit(winner_text, (110, 610))

    pygame.display.flip()
pygame.quit()
    



