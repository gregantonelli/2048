import numpy as np
from numpy.random import choice
import random
import pygame
from pygame.locals import *
from itertools import cycle


# Create empty board:
a = [0, 0, 0, 0]
b = [0, 0, 0, 0]
c = [0, 0, 0, 0]
d = [0, 0, 0, 0]

mega = [a, b, c, d]

# New number possibilities:
numbers = [2, 4]

# Define function to add new numbers to board. Function adds either a 2 (80% of the time) or a 4 (20%) if there is at
# least one empty spot. It chooses a random target on the board until it finds the empty spot. It prints target choices
# for debugging.

def new_number(board):
    counts = 1
    while counts < 2:
        if board[0].count(0) + board[1].count(0) + board[2].count(0) + board[3].count(0) >= 1:
            target1 = random.randint(0, 3)
            target2 = random.randint(0, 3)
            if board[target1][target2] == 0:
                board[target1][target2] = np.random.choice(numbers, p=[0.8, 0.2])
                print("Target: ", "row ", (target1 + 1), "col ", (target2 + 1))
                counts += 1
            else:
                print("Failed target: ", "row ", (target1 + 1), "col ", (target2 + 1))
        elif board.count(0) == 0:
            counts += 1

# Define starting score:
score = 0

# Define functions for moving in all four directions. Moving up and down rely on first flipping the board and then
# calling "move_left" or "move_right" as appropriate (then flipping back). All moves print the new board and update
# the score.

def move_right(board):
    global score
    def shift_right():
        for x in range(3):
            for row in board:
                ind = 0
                for x in range(3):
                    if row[ind+1] == 0:
                        row[ind+1] = row[ind]
                        row[ind] = 0
                    ind += 1
        print('Shifted right: ')
        print(mega[0])
        print(mega[1])
        print(mega[2])
        print(mega[3])

    def double_right():
        global score
        for row in board:
            for x in reversed(range(1,4)):
                if row[x] == row[x-1]:
                    row[x] *= 2
                    row[x-1] = 0
                    score += row[x]
        print('Doubled: ')
        print(mega[0])
        print(mega[1])
        print(mega[2])
        print(mega[3])
        print('Score: ', score)

    shift_right()
    double_right()
    shift_right()
def move_left(board):
    global score
    def shift_left():
        for x in range(3):
            for row in board:
                ind = 3
                for x in reversed(range(3)):
                    if row[ind-1] == 0:
                        row[ind-1] = row[ind]
                        row[ind] = 0
                    ind -= 1
        print('Shifted left: ')
        print(board[0])
        print(board[1])
        print(board[2])
        print(board[3])
    def double_left():
        global score
        for row in board:
            for x in range(3):
                if row[x] == row[x+1]:
                    row[x] *= 2
                    row[x+1] = 0
                    score += row[x]
        print('Doubled: ')
        print(board[0])
        print(board[1])
        print(board[2])
        print(board[3])
        print('Score: ', score)
    shift_left()
    double_left()
    shift_left()

def flip(board):
    global mega
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    flipped_mega = [row1, row2, row3, row4]
    for x in board:
        flipped_mega[0].append(x[3])
        flipped_mega[1].append(x[2])
        flipped_mega[2].append(x[1])
        flipped_mega[3].append(x[0])
    mega = flipped_mega
    print("Flipped: ")
    print(mega[0])
    print(mega[1])
    print(mega[2])
    print(mega[3])
def flip_back(board):
    global mega
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    flipped_back_mega = [row1,row2,row3,row4]
    for x in reversed(board):
        row1.append(x[0])
        row2.append(x[1])
        row3.append(x[2])
        row4.append(x[3])
    mega = flipped_back_mega
    print("Flipped back: ")
    print(mega[0])
    print(mega[1])
    print(mega[2])
    print(mega[3])

def move_up(board):
    flip(board)
    move_left(mega)
    flip_back(mega)
def move_down(board):
    flip(board)
    move_right(mega)
    flip_back(mega)

# Function that sets the initial board with two numbers (either 2 or 4, weighted 80%/20% respectively):
def sets_board(board):
    board[random.randint(0, 3)][random.randint(0, 3)] = np.random.choice(numbers, p=[0.8, 0.2])
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    if board[x][y] == 0:
        board[x][y] = 2
    else:
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        if board[x][y] == 0:
            board[x][y] = np.random.choice(numbers, p=[0.8, 0.2])
    print(mega[0])
    print(mega[1])
    print(mega[2])
    print(mega[3])

# Define functions to determine if the board is stuck in any direction so we know whether or not a move can be made in
# that direction.

stuck = False
def stuck_right(board):
    global stuck
    if stuck == False:
        for row in board:
            if row[0] != 0:
                if row[1] == 0 or row[2] == 0 or row[3] == 0 or row[0] == row[1] or row[1] == row[2] or row[2] == row[3]:
                    return False
            elif row[1] != 0:
                if row[2] == 0 or row[3] == 0 or row[1] == row[2] or row[2] == row[3]:
                    return False
            elif row[2] != 0:
                if row[3] == 0 or row[2] == row[3]:
                    return False
        return True
def stuck_left(board):
    global stuck
    if stuck == False:
        for row in board:
            if row[3] != 0:
                if row[2] == 0 or row[1] == 0 or row[0] == 0 or row[3] == row[2] or row[2] == row[1] or row[1] == row[0]:
                    return False
            elif row[2] != 0:
                if row[1] == 0 or row[0] == 0 or row[2] == row[1] or row[1] == row[0]:
                    return False
            elif row[1] != 0:
                if row[0] == 0 or row[1] == row[0]:
                    return False
        return True
def stuck_up(board):
    global stuck
    if stuck == False:
        for x in range(4):
            if board[3][x] != 0:
                if board[2][x] == 0 or board[1][x] == 0 or board[0][x] == 0 or board[3][x] == board[2][x] or board[2][x] == board[1][x] or board[1][x] == board[0][x]:
                    return False
            elif board[2][x] != 0:
                if board[1][x] == 0 or board[0][x] == 0 or board[2][x] == board[1][x] or board[1][x] == board[0][x]:
                    return False
            elif board[1][x] != 0:
                if board[0][x] == 0 or board[1][x] == board[0][x]:
                    return False
        return True
def stuck_down(board):
    global stuck
    if stuck == False:
        for x in range(4):
            if board[0][x] != 0:
                if board[1][x] == 0 or board[2][x] == 0 or board[3][x] == 0 or board[0][x] == board[1][x] or board[1][x] == board[2][x] or board[2][x] == board[3][x]:
                    return False
            elif board[1][x] != 0:
                if board[2][x] == 0 or board[3][x] == 0 or board[1][x] == board[2][x] or board[2][x] == board[3][x]:
                    return False
            elif board[2][x] != 0:
                if board[3][x] == 0 or board[2][x] == board[3][x]:
                    return False
        return True


# Define a function to freeze board in the event that the player has won:
def you_win():
    global stuck
    stuck = True
    print("You win!")

# Call sets_board:
sets_board(mega)

# Initialize the pygame
pygame.init()
pygame.mixer.init()

play_lose_sound = True
lose_sound = pygame.mixer.Sound("loser.mp3")

# Define function to play various sounds. Sound choice is heavily weighted to three regular swoosh sounds, but
# other occasional sound effects will play too:
def play_sound():
    sound = pygame.mixer.Sound("swipe.mp3")
    sound2 = pygame.mixer.Sound("woosh1.mp3")
    sound3 = pygame.mixer.Sound("woosh2.mp3")
    sound4 = pygame.mixer.Sound("fart.mp3")
    sound5 = pygame.mixer.Sound("chimp.mp3")
    sound6 = pygame.mixer.Sound("cartoon.mp3")
    sound7 = pygame.mixer.Sound("moo.mp3")
    sound_list = [sound, sound2, sound3, sound4, sound5, sound6, sound7]
    sound_list[np.random.choice([0, 1, 2, 3, 4, 5, 6], p=[0.34, 0.31, 0.31, 0.01, 0.01, 0.01, 0.01])].play()

# Create screen
screen = pygame.display.set_mode((800,800))

# Load icon / tiles:
pygame.display.set_caption("2048")
icon2 = pygame.image.load('NEW2.png')
icon4 = pygame.image.load('NEW4.png')
icon8 = pygame.image.load('NEW8.png')
icon16 = pygame.image.load('NEW16.png')
icon32 = pygame.image.load('NEW32.png')
icon64 = pygame.image.load('NEW64.png')
icon128 = pygame.image.load('NEW128.png')
icon256 = pygame.image.load('NEW256.png')
icon512 = pygame.image.load('NEW512.png')
icon1024 = pygame.image.load('NEW1024.png')
icon2048 = pygame.image.load('NEW2048.png')
tryagain = pygame.image.load('Try Again.png')
winner = pygame.image.load('You Win!.png')
cursor1 = pygame.image.load('cursor1.png')
cursor2 = pygame.image.load('cursor2.png')

# Determine visual position of tiles:
positions = [[(21,29),(210,29),(399,29),(588,29)], [(21,220),(210,220),(399,220),(588,220)], [(21,410),(210,410),(399,410),(588,410)], [(21,600),(210,600),(399,600),(588,600)]]

# Set icon to 2048 tile:
pygame.display.set_icon(icon2048)

# Board Image
boardImg = pygame.image.load('NEWboard.png')
boardX = 0
boardY = 0

# Load graphic board:
def board():
    screen.blit(boardImg, (boardX, boardY))

# Define various visual graphic themes:
theme = 'Standard'
themes =['Standard', 'Purple', 'Third']
theme_cycle = cycle(themes)

# Define function to change theme:
def themechange():
    global theme
    theme = next(theme_cycle)
    print("Theme change.")

running = True
while running:
    # Change icons if theme is altered:
    if theme == 'Standard':
        screen.fill((255, 229, 204))
        icon2 = pygame.image.load('NEW2.png')
        icon4 = pygame.image.load('NEW4.png')
        icon8 = pygame.image.load('NEW8.png')
        icon16 = pygame.image.load('NEW16.png')
        icon32 = pygame.image.load('NEW32.png')
        icon64 = pygame.image.load('NEW64.png')
        icon128 = pygame.image.load('NEW128.png')
        icon256 = pygame.image.load('NEW256.png')
        icon512 = pygame.image.load('NEW512.png')
        icon1024 = pygame.image.load('NEW1024.png')
        icon2048 = pygame.image.load('NEW2048.png')
        boardImg = pygame.image.load('NEWboard.png')
        pygame.display.set_icon(icon2048)
    if theme == 'Purple':
        screen.fill((123, 134, 188))
        icon2 = pygame.image.load('ALT2.png')
        icon4 = pygame.image.load('ALT4.png')
        icon8 = pygame.image.load('ALT8.png')
        icon16 = pygame.image.load('ALT16.png')
        icon32 = pygame.image.load('ALT32.png')
        icon64 = pygame.image.load('ALT64.png')
        icon128 = pygame.image.load('ALT128.png')
        icon256 = pygame.image.load('ALT256.png')
        icon512 = pygame.image.load('ALT512.png')
        icon1024 = pygame.image.load('ALT1024.png')
        icon2048 = pygame.image.load('ALT2048.png')
        boardImg = pygame.image.load('ALTboard.png')
        pygame.display.set_icon(pygame.image.load('ALT2048.png'))
    if theme == 'Third':
        screen.fill((244, 253, 255))
        icon2 = pygame.image.load('2.png')
        icon4 = pygame.image.load('4.png')
        icon8 = pygame.image.load('8.png')
        icon16 = pygame.image.load('16.png')
        icon32 = pygame.image.load('32.png')
        icon64 = pygame.image.load('64.png')
        icon128 = pygame.image.load('128.png')
        icon256 = pygame.image.load('256.png')
        icon512 = pygame.image.load('512.png')
        icon1024 = pygame.image.load('1024.png')
        icon2048 = pygame.image.load('2048.png')
        boardImg = pygame.image.load('NewBoard4.png')
        pygame.display.set_icon(pygame.image.load('2048.png'))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        # If conditions are suitable and keystroke is made, play sound, make move, add new numbers:
        if event.type == KEYDOWN and event.key == K_RIGHT and stuck_right(mega) == False:
            play_sound()
            move_right(mega)
            new_number(mega)
        if event.type == KEYDOWN and event.key == K_LEFT and stuck_left(mega) == False:
            play_sound()
            move_left(mega)
            new_number(mega)
        if event.type == KEYDOWN and event.key == K_UP and stuck_up(mega) == False:
            play_sound()
            move_up(mega)
            new_number(mega)
        if event.type == KEYDOWN and event.key == K_DOWN and stuck_down(mega) == False:
            play_sound()
            move_down(mega)
            new_number(mega)
        # Space bar changes theme:
        if event.type == KEYDOWN and event.key == K_SPACE:
            themechange()
        # "Escape" to quit:
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display icons matching internal game logic:
    lx = 0
    for x in mega:
        ly = 0
        for b in x:
            loc = (lx, ly)
            if b == 2:
                screen.blit(icon2,positions[lx][ly])
            elif b == 4:
                screen.blit(icon4, positions[lx][ly])
            elif b == 8:
                screen.blit(icon8, positions[lx][ly])
            elif b == 16:
                screen.blit(icon16, positions[lx][ly])
            elif b == 32:
                screen.blit(icon32, positions[lx][ly])
            elif b == 64:
                screen.blit(icon64, positions[lx][ly])
            elif b == 128:
                screen.blit(icon128, positions[lx][ly])
            elif b == 256:
                screen.blit(icon256, positions[lx][ly])
            elif b == 512:
                screen.blit(icon512, positions[lx][ly])
            elif b == 1024:
                screen.blit(icon1024, positions[lx][ly])
            elif b == 2048:
                screen.blit(icon2048, positions[lx][ly])
            ly += 1
        lx += 1

    board()

    # Determine if 2048 tile is present. If so, game is over. Win condition is met so board freezes; winner graphic is
    # displayed.
    if 2048 in mega[0] or 2048 in mega[1] or 2048 in mega[2] or 2048 in mega[3]:
        you_win()
        screen.blit(winner, (40, 313))

    # Determine if board is jammed and condition for lose is met. If so, display "try again" graphic (clickable)
    # and lose audio.
    if stuck_down(mega) and stuck_up(mega) and stuck_left(mega) and stuck_right(mega) == True:
        screen.blit(tryagain, (40, 313))
        if play_lose_sound == True:
            lose_sound.play()
            play_lose_sound = False
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                mega = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
                sets_board(mega)
                play_lose_sound = True
                print('Reset board...')
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] > 59 and pos[0] < 746 and pos[1] > 343 and pos[1] < 450:
                    mega = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                    sets_board(mega)
                    play_lose_sound = True
                    print('Reset board...')
            if event.type == KEYDOWN and event.key == K_SPACE:
                themechange()
    pygame.display.update()



