import random
import time
import os

# Game window constants
SCREEN_HEIGHT = 20
SCREEN_WIDTH = 70

# Pipe constants
pipe_cap_def = '==='
pipe_cap = '='
pipe_side = '|'
pipe_middle = ' '
pipe_width = len(pipe_cap_def)
max_height = 11 # max_height - 10 is how many pipe_sides can print on top pipe at max height
min_height = 3 # min_height - 1 is how many pipe_sides can print at minimum
GAP_HEIGHT = 7 # Vertical cap between top and bottom pipes
PIPE_SPACING = 15 # Space in between consecutively generated pipes
TIME_STEP = .12 # Framerate of the game
GAME_TIME = 20 # seconds long the game runs

class Pipe:
    def __init__(self, x_position):
        self.bottom_height = random.randint(min_height, max_height)
        self.gap = GAP_HEIGHT
        self.top_height = SCREEN_HEIGHT - self.bottom_height - self.gap - 2
        self.x = x_position
        self.width = pipe_width

    def move(self):
        self.x -= 1

    def get_visible_columns(self):
        columns = []

        for i in range(pipe_width):
            global_x = self.x + i
            if 0 <= global_x < SCREEN_WIDTH:
                col = [' '] * SCREEN_HEIGHT

                # Bottom pipe
                bottom_start = SCREEN_HEIGHT - self.bottom_height - 1
                for y in range(bottom_start, SCREEN_HEIGHT - 1):
                    if i == 0 or i == 2:
                        col[y] = pipe_side
                    elif i == 1:
                        col[y] = pipe_middle
                if bottom_start - 1 >= 1:
                    col[bottom_start - 1] = pipe_cap

                # Top pipe
                top_end = self.top_height + 1
                for y in range(0, top_end + 1):
                    if i == 0 or i == 2:
                        col[y] = pipe_side
                    elif i == 1:
                        col[y] = pipe_middle
                if top_end < SCREEN_HEIGHT - 1:
                    col[top_end] = pipe_cap

                columns.append((global_x, col))

        return columns

# Create empty screen
def create_empty_screen():
    screen = []
    screen.append('#' * SCREEN_WIDTH)
    for _ in range(SCREEN_HEIGHT - 2):
        screen.append('#' + ' ' * (SCREEN_WIDTH - 2) + '#')
    screen.append('#' * SCREEN_WIDTH)
    return screen

# Inject pipes into screen
def draw_pipe_on_screen(screen, pipe):
    screen_chars = [list(row) for row in screen] # convert to lists of lists for easy editing
    pipe_columns = pipe.get_visible_columns()

    for x, col in pipe_columns:
        for y in range(SCREEN_HEIGHT):
            if 0 <= y + 1 < SCREEN_HEIGHT - 1: #account for top and bottom of the boarder
                screen_chars[y + 1][x] = col[y]

    return [''.join(row) for row in screen_chars]

pipes = [Pipe(x_position=SCREEN_WIDTH)]
start_time = time.time()
duration = GAME_TIME # seconds

while time.time() - start_time < duration:
    for pipe in pipes:
        pipe.move()

    # Remove pipes that have moved off screen
    pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

    # Add new pipe if the last one is far enough away
    if not pipes or pipes[-1].x <= SCREEN_WIDTH - PIPE_SPACING - pipe_width:
        pipes.append(Pipe(x_position=SCREEN_WIDTH))

    # Build screen
    screen = create_empty_screen()
    for pipe in pipes:
        screen = draw_pipe_on_screen(screen, pipe)

    os.system('cls' if os.name =='nt' else 'clear') # clears terminal
    for line in screen: # Render
        print(line)

    time.sleep(TIME_STEP)



#pipe_height = random.randint(min_height, max_height)

# Draw a pipe into game window

# print('#' * SCREEN_WIDTH)
# for i in range(1,SCREEN_HEIGHT,1):
#     if pipe_row == false:
#         print('#' + ' ' * (SCREEN_WIDTH - 2) + '#')
# print('#' * SCREEN_WIDTH)


#| |
#| |
#===



#===
#| |
#| |
#| |





#------------------------------------------------------------------------------

# class Background:
#     def __init__(self):
#         self.inner_height = SCREEN_HEIGHT - 2  # account for top and bottom border
#         self.inner_width = SCREEN_WIDTH - 2   # account for left and right border
#         self.pipes = []

#     def add_pipe(self):
#         height = random.randint(3, 6)
#         self.pipes.append(Pipe(self.inner_width - PIPE_WIDTH, height))

#     def update(self):
#         # Create empty interior grid
#         self.screen = [[' ' for _ in range(self.inner_width)] for _ in range(self.inner_height)]

#         # Update pipe positions and draw them
#         for pipe in self.pipes:
#             pipe.x -= 1
#             if pipe.x + PIPE_WIDTH > 0:
#                 pipe.draw(self.screen)

#     def render(self):
#         # Build full frame with borders
#         top_border = ['#' * SCREEN_WIDTH]
#         middle_rows = [
#             '#' + ''.join(row) + '#' for row in self.screen
#         ]
#         bottom_border = ['#' * SCREEN_WIDTH]
#         return '\n'.join(top_border + middle_rows + bottom_border)
