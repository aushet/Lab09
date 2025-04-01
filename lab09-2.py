import pygame
import random
import sys

# Инициализация
pygame.init()

# Размеры экрана и клетки
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Экран и таймер
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Levels")
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.SysFont("Arial", 20)

# Генерация еды с весом и таймером
def random_food(snake, walls):
    while True:
        x = random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE
        y = random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE
        if (x, y) not in snake and (x, y) not in walls:
            weight = random.choice([1, 2, 3])
            timer = 150  # Еда исчезнет через 150 тиков
            return {'pos': (x, y), 'weight': weight, 'timer': timer}

# Генерация стен
def create_walls(level):
    walls = set()
    if level >= 2:
        for i in range(10, 20):
            walls.add((i * CELL_SIZE, 10 * CELL_SIZE))
    if level >= 3:
        for i in range(5, 15):
            walls.add((20 * CELL_SIZE, i * CELL_SIZE))
    return walls

# Основная функция игры
def main():
    snake = [(100, 100), (80, 100)]
    direction = (CELL_SIZE, 0)
    level = 1
    score = 0
    speed = 10
    food_eaten = 0
    walls = create_walls(level)

    # Создание первой еды
    food = random_food(snake, walls)

    running = True
    while running:
        screen.fill(BLACK)

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
            direction = (0, -CELL_SIZE)
        elif keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        elif keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        elif keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        # Движение головы
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Проверка на проигрыш
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake or
            new_head in walls):
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Добавление новой головы
        snake.insert(0, new_head)

        # Проверка на поедание еды
        if new_head == food['pos']:
            score += food['weight']
            food_eaten += 1
            food = random_food(snake, walls)
        else:
            snake.pop()

        # Таймер еды уменьшается
        food['timer'] -= 1
        if food['timer'] <= 0:
            food = random_food(snake, walls)

        # Повышение уровня
        if food_eaten >= 3:
            level += 1
            speed += 2
            food_eaten = 0
            walls = create_walls(level)

        # Отрисовка змейки
        for block in snake:
            pygame.draw.rect(screen, GREEN, (*block, CELL_SIZE, CELL_SIZE))

        # Отрисовка еды (меняется размер в зависимости от веса)
        color = RED if food['weight'] == 1 else (255, 165, 0) if food['weight'] == 2 else (255, 255, 0)
        pygame.draw.rect(screen, color, (*food['pos'], CELL_SIZE, CELL_SIZE))

        # Отрисовка стен
        for wall in walls:
            pygame.draw.rect(screen, BLUE, (*wall, CELL_SIZE, CELL_SIZE))

        # Очки и уровень
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        timer_text = font.render(f"Food Timer: {food['timer']//10}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 30))
        screen.blit(timer_text, (10, 50))

        pygame.display.flip()
        clock.tick(speed)

# Запуск игры
main()
