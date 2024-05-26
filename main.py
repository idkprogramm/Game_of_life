from pygame import *

font.init()

age = 0


class Cell(sprite.Sprite):
    def __init__(self, x, y, size, is_alive=False):
        super().__init__()

        self.image = Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.is_alive = is_alive

    def update(self):
        fill_color = (50, 50, 50)
        if self.is_alive:
            fill_color = (0, 255, 0)

        self.image.fill(fill_color)
        win.blit(self.image, self.rect)


def update_state_cells(matrix: list[list[Cell]]):
    len_col = len(matrix)
    len_row = len(matrix[0])  # используем 0, так как предполагаем, что все строки одной длины

    next_state = [[cell.is_alive for cell in row] for row in matrix]

    for i in range(len_col):
        for j in range(len_row):
            count = sum([
                matrix[(i - 1) % len_col][(j - 1) % len_row].is_alive,
                matrix[i % len_col][(j - 1) % len_row].is_alive,
                matrix[(i + 1) % len_col][(j - 1) % len_row].is_alive,
                matrix[(i - 1) % len_col][j % len_row].is_alive,
                matrix[(i + 1) % len_col][j % len_row].is_alive,
                matrix[(i - 1) % len_col][(j + 1) % len_row].is_alive,
                matrix[i % len_col][(j + 1) % len_row].is_alive,
                matrix[(i + 1) % len_col][(j + 1) % len_row].is_alive
            ])

            if matrix[i][j].is_alive:
                next_state[i][j] = count == 2 or count == 3
            else:
                next_state[i][j] = count == 3

    for i in range(len_col):
        for j in range(len_row):
            matrix[i][j].is_alive = next_state[i][j]


def clear_board(matrix: list[list[Cell]]):
    for row in matrix:
        for cell in row:
            cell.is_alive = False


def count_alive_cells(matrix: list[list[Cell]]) -> int:
    sells = 0
    for row in matrix:
        for cell in row:
            sells += cell.is_alive
    return sells


width, height = 500, 500
cell_size = 14
margin = 1
FPS = 10

win = display.set_mode((width, height))
display.set_caption("Game of life")
win.fill((255, 255, 255))

game, pause = True, True

cells = []
for i in range(height // (cell_size + margin)):
    row = []
    y = (cell_size + margin) * i
    for j in range(width // (cell_size + margin)):
        row.append(Cell((cell_size + margin) * j, y, cell_size))
    cells.append(row)

len_col = len(cells)
len_row = len(cells[-1])

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_p:
                pause = not pause
            elif e.key == K_r:
                clear_board(cells)
            elif e.key == K_EQUALS:
                FPS = FPS + 1
            elif e.key == K_MINUS:
                FPS = max(FPS - 1, 1)
        if e.type == MOUSEBUTTONDOWN and e.button == BUTTON_LEFT:
            col = min(e.pos[1] // (cell_size + margin), len_col)
            row = min(e.pos[0] // (cell_size + margin), len_row)
            cells[col][row].is_alive = not cells[col][row].is_alive

    win.fill((255, 255, 255))

    for row in cells:
        for cell in row:
            cell.update()

    if not pause:
        update_state_cells(cells)
    else:
        win.blit(
            font.SysFont('Arial', 30).render(
                "Press P to start", True, (255, 255, 0)
            ), ((width//2)-45, height//2)
        )

    if count_alive_cells(cells) == 0:
        pause = True
    elif count_alive_cells(cells) >= 1 and not pause:
        age += 1
        win.blit(
            font.SysFont('Arial', 30).render(
                "Generation:", age, True, (255, 255, 0)
            ), ((width // 2) - 45, height // 2)
        )

    display.update()
    time.Clock().tick(FPS)