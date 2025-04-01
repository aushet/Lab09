import pygame
import sys
import math

pygame.init()

# Размер экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint App")

clock = pygame.time.Clock()
screen.fill((255, 255, 255))

# Цвет и начальные настройки
current_color = (0, 0, 0)
tool = "brush"
radius = 5

# Палитра цветов
color_options = [
    ((0, 0, 0), (10, 10, 30, 30)),      # чёрный
    ((255, 0, 0), (50, 10, 30, 30)),    # красный
    ((0, 255, 0), (90, 10, 30, 30)),    # зелёный
    ((0, 0, 255), (130, 10, 30, 30))    # синий
]

font = pygame.font.SysFont("Arial", 18)

# UI: рисование кнопок и текста
def draw_ui():
    for color, rect in color_options:
        pygame.draw.rect(screen, color, rect)
    screen.blit(font.render(f"Tool: {tool}", True, (0, 0, 0)), (10, 50))

# Рисование квадрата
def draw_square(start, end, color):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(screen, color, rect, 2)

# Рисование прямоугольного треугольника (вправо-вниз)
def draw_right_triangle(start, end, color):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(screen, color, points, 2)

# Рисование равностороннего треугольника
def draw_equilateral_triangle(start, end, color):
    x1, y1 = start
    x2, y2 = end
    side = math.dist(start, end)
    center = ((x1 + x2) / 2, (y1 + y2) / 2)
    height = (3**0.5 / 2) * side
    # точки треугольника (вниз)
    points = [
        (center[0], center[1] - 2/3 * height),
        (center[0] - side/2, center[1] + height/3),
        (center[0] + side/2, center[1] + height/3)
    ]
    pygame.draw.polygon(screen, color, points, 2)

# Рисование ромба
def draw_rhombus(start, end, color):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    dx = abs(x2 - x1) // 2
    dy = abs(y2 - y1) // 2
    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(screen, color, points, 2)

running = True
drawing = False
start_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Переключение инструментов
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_s:
                tool = "square"
            elif event.key == pygame.K_t:
                tool = "right_triangle"
            elif event.key == pygame.K_q:
                tool = "equilateral"
            elif event.key == pygame.K_h:
                tool = "rhombus"

        # Выбор цвета или начало рисования
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for color, rect in color_options:
                if pygame.Rect(rect).collidepoint(mx, my):
                    current_color = color
            drawing = True
            start_pos = event.pos

        # Отпускание мыши — рисуем фигуру
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == "rect":
                pygame.draw.rect(screen, current_color, pygame.Rect(*start_pos, end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), 2)
            elif tool == "circle":
                radius = int(math.dist(start_pos, end_pos) / 2)
                center = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
                pygame.draw.circle(screen, current_color, center, radius, 2)
            elif tool == "square":
                draw_square(start_pos, end_pos, current_color)
            elif tool == "right_triangle":
                draw_right_triangle(start_pos, end_pos, current_color)
            elif tool == "equilateral":
                draw_equilateral_triangle(start_pos, end_pos, current_color)
            elif tool == "rhombus":
                draw_rhombus(start_pos, end_pos, current_color)

    # Brush/eraser — рисование при зажатии
    if drawing and tool in ["brush", "eraser"]:
        mx, my = pygame.mouse.get_pos()
        color = current_color if tool == "brush" else (255, 255, 255)
        pygame.draw.circle(screen, color, (mx, my), radius)

    draw_ui()
    pygame.display.flip()
    clock.tick(60)
