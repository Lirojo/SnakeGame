import pygame
import time
import random

# Inicjalizacja Pygame
pygame.init()

# Definiowanie kolorów
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Wymiary ekranu
dis_width = 800
dis_height = 600

# Utworzenie okna gry
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Gra Snake')

# Ustawienie zegara
clock = pygame.time.Clock()

# Ustawienia węża
snake_block = 10
snake_speed = 15

# Definicja czcionki dla tekstu
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Funkcja wyświetlająca wynik
def your_score(score):
    value = score_font.render("Twój wynik: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# Funkcja rysująca węża
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Funkcja łamania tekstu na linie
def draw_text(text, font, color, surface, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_surface = font.render(word, True, color)
        word_width = word_surface.get_width()
        # Jeśli bieżąca linia + nowe słowo przekroczy maksymalną szerokość, przenosimy na nową linię
        if current_width + word_width >= max_width:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width
        else:
            current_line.append(word)
            current_width += word_width + font.size(' ')[0]  # dodajemy szerokość spacji

    lines.append(' '.join(current_line))  # Dodaj ostatnią linię

    # Wyświetl linie na ekranie
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (x, y + i * font.get_height()))

# Funkcja wyświetlająca komunikaty
def message(msg, color):
    draw_text(msg, font_style, color, dis, dis_width / 6, dis_height / 3, dis_width * 2 / 3)

# Główna funkcja gry
def gameLoop():
    game_over = False
    game_close = False

    # Początkowa pozycja węża
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Zmienne kierunku węża
    x1_change = 0
    y1_change = 0

    # Lista segmentów węża
    snake_list = []
    length_of_snake = 1

    # Losowanie pozycji jedzenia
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("Przegrałeś! Naciśnij Q, aby zakończyć, lub C, aby zagrać ponownie", red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        # Rysowanie jedzenia
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Dodawanie nowego segmentu do węża
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Sprawdzenie kolizji z własnym ciałem
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        # Rysowanie węża
        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)

        pygame.display.update()

        # Sprawdzenie, czy wąż zjadł jedzenie
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        # Ustawienie szybkości węża
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Uruchomienie gry
gameLoop()
