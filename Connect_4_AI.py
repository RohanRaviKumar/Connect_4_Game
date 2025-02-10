import pygame
import sys
import math
import random

SANDAL = (215, 179, 140)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 222, 33)


def create_board():
    return [[0 for j in range(7)] for i in range(6)]


def fill_column(board, turn, column, cols):
    if cols[column] >= 0:
        board[cols[column]][column] = turn + 1
        cols[column] -= 1


def display_board(board):
    for i in board:
        print(i)


def is_over(board):
    for i in board:
        for box in i:
            if box == 0:
                return 0
    return 1


def wins(board):
    for r in range(6):
        for c in range(4):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][
                    c + 3] != 0:
                return board[r][c]

    for c in range(7):
        for r in range(3):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[
                    r + 3][c] != 0:
                return board[r][c]

    for r in range(3):
        for c in range(4):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][
                    c + 2] == board[r + 3][c + 3] != 0:
                return board[r][c]

    for r in range(3, 6):
        for c in range(4):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][
                    c + 2] == board[r - 3][c + 3] != 0:
                return board[r][c]

    return 0


def evaluate(board):
    score = 0
    for r in range(6):
        for c in range(7):
            if board[r][c] == 1:
                score += 1
            elif board[r][c] == 2:
                score -= 1
    return score

def imminent_win(board, player, cols_filled):
    for col in range(7):
        if board[0][col] == 0:
            temp_board = [row[:] for row in board]
            temp_cols = list(cols_filled)
            fill_column(temp_board, player, col, temp_cols)
            if wins(temp_board) == player + 1:
                return col
    return -1

def best_move(board, cols_filled):
    best_value = -math.inf
    best_col = -1 

    player_win_move = imminent_win(board, 0, cols_filled)
    if player_win_move != -1:
        return player_win_move

    ai_win_move = imminent_win(board, 1, cols_filled)
    if ai_win_move != -1:
        return ai_win_move

    for col in range(7):
        if board[0][col] == 0:
            new_board = [row[:] for row in board]
            cols = list(cols_filled)
            fill_column(new_board, 0, col, cols)
            move_value = minimax(new_board, 3, -math.inf, math.inf, False)
            if move_value > best_value:
                best_value = move_value
                best_col = col

    return best_col

def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or wins(board) != 0 or is_over(board):
        return evaluate(board)

    if maximizingPlayer:
        maxEval = -math.inf
        for col in range(7):
            if board[0][col] == 0:
                new_board = [row[:] for row in board]
                cols = [5 for _ in range(7)]
                fill_column(new_board, 0, col, cols)
                eval = minimax(new_board, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return maxEval
    else:
        minEval = math.inf
        for col in range(7):
            if board[0][col] == 0:
                new_board = [row[:] for row in board]
                cols = [5 for _ in range(7)]
                fill_column(new_board, 1, col, cols)
                eval = minimax(new_board, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval

def draw_board(board):
    for r in range(6):
        for c in range(7):
            pygame.draw.rect(screen, SANDAL, (c * ss, (r + 1) * ss, ss, ss))
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED,
                                   (c * ss + ss // 2, (r + 1) * ss + ss // 2),
                                   radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   (c * ss + ss // 2, (r + 1) * ss + ss // 2),
                                   radius)
            else:
                pygame.draw.circle(screen, BLACK,
                                   (c * ss + ss // 2, (r + 1) * ss + ss // 2),
                                   radius)


board = create_board()
turn = 0
cols_filled = [5 for _ in range(7)]

pygame.init()
ss = 100
width = 7 * ss
height = 7 * ss
radius = ss // 2 - 5

size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 65)
turn = 0
cols_filled = [5 for _ in range(7)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, ss))
            pos_x = event.pos[0]
            if turn == 1:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(ss / 2)), radius)
            else:
                pygame.draw.circle(screen, RED, (pos_x, int(ss / 2)), radius)
            pygame.display.update()
        
        if turn == 0:
            ai_column = best_move(board, cols_filled)
            if ai_column != -1 and cols_filled[ai_column] >= 0:
                fill_column(board, turn, ai_column, cols_filled)
                draw_board(board)
                pygame.display.update()

                win = wins(board)
                if win != 0:
                    if win == 1:
                        print("AI wins!")
                        label = myfont.render("AI wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                    elif win == 2:
                        print("You win!")
                        label = myfont.render("You win!", 1, RED)
                        screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(8000)
                    sys.exit()
                    
                if is_over(board):
                    print("The game is a draw!")
                    label = myfont.render("Draw!", 1, BLUE)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(8000)
                    sys.exit()
            turn = (turn + 1) % 2
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
                
            pygame.draw.rect(screen, BLACK, (0, 0, width, ss))
            pos_x = event.pos[0]
            column = pos_x // ss

            if 0 <= column < 7 and cols_filled[column] >= 0:
                fill_column(board, turn, column, cols_filled)
                draw_board(board)
                pygame.display.update()

                win = wins(board)
                if win != 0:
                    if win == 1:
                        print("AI wins!")
                        label = myfont.render("AI wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                    elif win == 2:
                        print("You win!")
                        label = myfont.render("You win!", 1, RED)
                        screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(8000)
                    sys.exit()

                if is_over(board):
                    print("The game is a draw!")
                    label = myfont.render("Draw!", 1, BLUE)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(8000)
                    sys.exit()

            turn = (turn + 1) % 2
pygame.quit()