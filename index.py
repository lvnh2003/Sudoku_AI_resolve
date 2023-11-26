import pygame
import random

# Định nghĩa màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
# Kích thước cửa sổ game
WINDOW_WIDTH = 580
WINDOW_HEIGHT = 680

# Kích thước và vị trí lưới Sudoku
GRID_SIZE = 60
GRID_ORIGIN_X = 20
GRID_ORIGIN_Y = 20

# Khởi tạo cửa sổ game
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku Solver")
grid = []
# Tạo một khung Sudoku ngẫu nhiên
# Vẽ nút "AI Resolve"
def draw_ai_resolve_button():
    pygame.draw.rect(window, GREEN, (WINDOW_WIDTH // 2 - 175, WINDOW_HEIGHT - 70, 150, 50))
    font = pygame.font.SysFont(None, 25)
    text = font.render("AI Resolve", True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 45)
    window.blit(text, text_rect)

# Vẽ nút "New Game"
def draw_new_game_button():
    pygame.draw.rect(window, BLACK, (WINDOW_WIDTH // 2 + 25, WINDOW_HEIGHT - 70, 150, 50))
    font = pygame.font.SysFont(None, 25)
    text = font.render("New Game", True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2 + 100, WINDOW_HEIGHT - 45)
    window.blit(text, text_rect)
def is_valid_move(grid, row, col, num):
    if num in grid[row] or num in [grid[i][col] for i in range(9)]:
        return False

    # Kiểm tra xem số đã tồn tại trong ô 3x3 chưa
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True
def generate_sudoku():
    global grid
    grid = [[0] * 9 for _ in range(9)]
    solve_sudoku(grid)

    # Loại bỏ một số ô để tạo ra trạng thái ban đầu của trò chơi
    for _ in range(random.randint(30, 65)):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while grid[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = 0
    return grid

# Vẽ lưới Sudoku


def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            line_thickness = 4
        else:
            line_thickness = 1

        pygame.draw.line(window, BLACK, (GRID_ORIGIN_X, GRID_ORIGIN_Y + i * GRID_SIZE),
                         (GRID_ORIGIN_X + 9 * GRID_SIZE, GRID_ORIGIN_Y + i * GRID_SIZE), line_thickness)
        pygame.draw.line(window, BLACK, (GRID_ORIGIN_X + i * GRID_SIZE, GRID_ORIGIN_Y),
                         (GRID_ORIGIN_X + i * GRID_SIZE, GRID_ORIGIN_Y + 9 * GRID_SIZE), line_thickness)

# Vẽ các ô số trong Sudoku
def draw_numbers():
    global grid
    font = pygame.font.SysFont(None, 40)

    for row in range(9):
        for col in range(9):
            number = grid[row][col]
            if number != 0:
                number_text = font.render(str(number), True, BLUE)
                x = GRID_ORIGIN_X + col * GRID_SIZE + GRID_SIZE // 2 - number_text.get_width() // 2
                y = GRID_ORIGIN_Y + row * GRID_SIZE + GRID_SIZE // 2 - number_text.get_height() // 2
                window.blit(number_text, (x, y))

# Hàm giải Sudoku
def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0  # backtrack if the solution is not valid
                return False
    return True
# Chạy game
def run_game():
    global grid
    sudoku_grid = generate_sudoku()
    solved = False
    all_solutions = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if WINDOW_WIDTH // 2 + 25 <= mouse_pos[0] <= WINDOW_WIDTH // 2 + 175 and WINDOW_HEIGHT - 80 <= mouse_pos[1] <= WINDOW_HEIGHT - 20:
                    sudoku_grid = generate_sudoku()
                    solved = False
                elif WINDOW_WIDTH // 2 - 175 <= mouse_pos[0] <= WINDOW_WIDTH // 2 - 25 and WINDOW_HEIGHT - 70 <= \
                        mouse_pos[1] <= WINDOW_HEIGHT - 20:
                    solve_sudoku(sudoku_grid)
                    # print_grid(sudoku_grid)


        window.fill(WHITE)
        draw_grid()
        draw_numbers()
        draw_ai_resolve_button()
        draw_new_game_button()
        pygame.display.update()

run_game()