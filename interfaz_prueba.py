from typing import List
from wordle import Wordle
from letra_correcta import LetraCorrecta
from colorama import Fore #sirve para cambiar el color del texto de la terminal

import pygame
import sys
import random

pygame.init()

window_width = 600
window_height = 580  
cell_size = 50
spacing = 10
ACIERTOS = 0
FALLOS = 0



def load_word_set(path: str):
    word_set = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            word = line.strip().upper()
            word_set.add(word)
    return word_set


# Obtener el número de columnas del usuario
def get_columns():
    columns = None
    while columns not in range(4, 9):
        try:
            columns = int(input("Ingrese el número de columnas (entre 4 y 8): "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
    return columns

# Obtener el número de columnas
columns = get_columns()

word_set = load_word_set(f"lema{columns}.txt")
wordle = Wordle(random.choice(list(word_set)), columns)

print(wordle.secret)

# Asegurarse de que siempre haya 6 filas
grid_rows = 6

# Calcular el tamaño total de la cuadrícula y el espacio alrededor
grid_size = (grid_rows, columns)
grid_width = grid_size[1] * cell_size + (grid_size[1] - 1) * spacing
grid_height = grid_size[0] * cell_size + (grid_size[0] - 1) * spacing

# Calcular la posición para centrar la cuadrícula en la ventana
start_x = (window_width - grid_width) // 2
start_y = 70  # Cambiamos la posición para incluir el título

# Definir colores
white = (255, 255, 255)
black = (0, 0, 0)
blue = (100, 150, 255)
gray = (200, 200, 200)

# Cambia la inicialización de letter_grid para considerar las filas y columnas
letter_grid = [[' ' for _ in range(grid_size[1])] for _ in range(grid_size[0])]


# Texto de entrada
input_text = ''
input_rect = pygame.Rect(50, window_height - 70, 300, 40)
font = pygame.font.Font(None, 32)
active = False

# Botón para ingresar la palabra
button_rect = pygame.Rect(380, window_height - 70, 150, 40)
button_color = gray
button_text = font.render('Ingresar Palabra', True, black)
button_text_rect = button_text.get_rect(center=button_rect.center)
# Nuevo botón "Jugar de nuevo" (que reemplaza el input y el botón anterior)
play_again_rect = pygame.Rect(200, window_height - 70, 200, 40)
play_again_color = gray
play_again_text = font.render('Jugar de nuevo', True, black)
play_again_text_rect = play_again_text.get_rect(center=play_again_rect.center)

# Botones "Sí" y "No"
yes_rect = pygame.Rect(200, window_height - 120, 80, 40)
yes_color = gray
yes_text = font.render('Sí', True, black)
yes_text_rect = yes_text.get_rect(center=yes_rect.center)

no_rect = pygame.Rect(320, window_height - 120, 80, 40)
no_color = gray
no_text = font.render('No', True, black)
no_text_rect = no_text.get_rect(center=no_rect.center)

# Configurar la ventana
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Interfaz estilo Wordle')

# Lógica para manejar el ingreso de letras
current_row = 0
current_column = 0

# Variables adicionales para manejar el mensaje de error
error_font = pygame.font.Font(None, 24)
error_color = (255, 0, 0)  # Color rojo para el mensaje de error

show_error_message_word_set = False
guessed =False
show_exit_message = False

def restart_game():
    global guessed, input_text, show_error_message, show_error_message_word_set
    guessed = False
    input_text = ''
    show_error_message = False
    show_error_message_word_set = False

# Función para dibujar el mensaje de error si es necesario
def draw_error_message(error_message):
    global input_text, show_error_message
    if show_error_message:
        error_surface = error_font.render(error_message, True, error_color)
        error_rect = error_surface.get_rect(midtop=(window_width // 2, input_rect.y - 35))
        window.blit(error_surface, error_rect)
    elif show_error_message_word_set:
        error_surface = error_font.render("La palabra no está en el conjunto de palabras.", True, error_color)
        error_rect = error_surface.get_rect(midtop=(window_width // 2, input_rect.y - 35))
        window.blit(error_surface, error_rect)

# Función para manejar la distribución de la palabra en la cuadrícula
def distribute_word():
    global input_text, current_row, current_column, show_error_message, show_error_message_word_set, guessed
    if len(input_text) != grid_size[1]:
        show_error_message = True
    elif input_text.upper() not in word_set:  
        show_error_message_word_set = True  
        show_error_message = False  
    else:
        show_error_message_word_set = False  
        show_error_message = False
        for letter in input_text.upper():
            if current_row < grid_size[0] and current_column < grid_size[1]:
                letter_grid[current_row][current_column] = letter
                current_column += 1
                if current_column >= grid_size[1]:
                    current_row += 1
                    current_column = 0
        if input_text.upper() == wordle.secret:
            guessed = True
            guessed_font = pygame.font.Font(None, 32)
            guessed_text = guessed_font.render('¡Has adivinado la palabra!', True, (0, 128, 0))
            guessed_rect = guessed_text.get_rect(center=(window_width // 2, window_height - 130))
            window.blit(guessed_text, guessed_rect)
    input_text = ''


show_input_button = True 

show_error_message = False

while True:
    window.fill(white)  # Rellenar la ventana con blanco

    # Dibujar el título "Wordle"
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render('Wordle', True, black)
    title_rect = title_text.get_rect(center=(window_width // 2, 30))  # Posicionamos el título
    window.blit(title_text, title_rect)

    if show_input_button:
        # Dibujar las cuadrículas para mostrar las letras ingresadas
        # Iterar sobre las filas y columnas de la cuadrícula
        for y in range(grid_size[0]):
            for x in range(grid_size[1]):
                rect_x = start_x + x * (cell_size + spacing)
                rect_y = start_y + y * (cell_size + spacing)
                pygame.draw.rect(window, black, (rect_x, rect_y, cell_size, cell_size), 1)

                # Dibujar las letras correspondientes en las cuadrículas
                text_surface = font.render(letter_grid[y][x], True, black)
                text_rect = text_surface.get_rect(center=(rect_x + cell_size // 2, rect_y + cell_size // 2))
                window.blit(text_surface, text_rect)

        # Dibujar el área de entrada de texto
        pygame.draw.rect(window, blue if active else black, input_rect, 2)
        text_surface = font.render(input_text, True, black)
        window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # Dibujar el botón
        pygame.draw.rect(window, button_color, button_rect)
        window.blit(button_text, button_text_rect)
        # Dibuja el mensaje de error
        draw_error_message("La longitud de la palabra no coincide con el número de columnas.")

    else:
        # Dibujar los botones "Jugar de nuevo", "Sí" y "No"
        pygame.draw.rect(window, play_again_color, play_again_rect)
        window.blit(play_again_text, play_again_text_rect)
        pygame.draw.rect(window, yes_color, yes_rect)
        window.blit(yes_text, yes_text_rect)
        pygame.draw.rect(window, no_color, no_rect)
        window.blit(no_text, no_text_rect)

    # Dibujar las cuadrículas para mostrar las letras ingresadas
    # Iterar sobre las filas y columnas de la cuadrícula
    for y in range(grid_size[0]):
        for x in range(grid_size[1]):
            rect_x = start_x + x * (cell_size + spacing)
            rect_y = start_y + y * (cell_size + spacing)
            pygame.draw.rect(window, black, (rect_x, rect_y, cell_size, cell_size), 1)

            # Dibujar las letras correspondientes en las cuadrículas
            text_surface = font.render(letter_grid[y][x], True, black)
            text_rect = text_surface.get_rect(center=(rect_x + cell_size // 2, rect_y + cell_size // 2))
            window.blit(text_surface, text_rect)

    # Dibujar el área de entrada de texto
    pygame.draw.rect(window, blue if active else black, input_rect, 2)
    text_surface = font.render(input_text, True, black)
    window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # Dibujar el botón
    pygame.draw.rect(window, button_color, button_rect)
    window.blit(button_text, button_text_rect)
    # Dibuja el mensaje de error
    draw_error_message("La longitud de la palabra no coincide con el número de columnas.")

    if guessed:
        # Si se adivina la palabra, se ocultan el área de ingreso de texto y el botón "Ingresar Palabra"
        show_input_button = False

        # Mostrar un mensaje de éxito
        guessed_font = pygame.font.Font(None, 32)
        guessed_text = guessed_font.render('¡Has adivinado la palabra!', True, (0, 128, 0))
        guessed_rect = guessed_text.get_rect(center=(window_width // 2, window_height - 130))
        window.blit(guessed_text, guessed_rect)

     # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_input_button:
                if input_rect.collidepoint(event.pos):
                    active = True
                elif button_rect.collidepoint(event.pos):
                    distribute_word()
                elif play_again_rect.collidepoint(event.pos) and guessed:
                    restart_game()
                elif yes_rect.collidepoint(event.pos) and guessed:
                    restart_game()
                elif no_rect.collidepoint(event.pos) and guessed:
                    show_exit_message = True
                else:
                    active = False
            else:
                if play_again_rect.collidepoint(event.pos):
                    restart_game()
                elif yes_rect.collidepoint(event.pos):
                    restart_game()
                elif no_rect.collidepoint(event.pos):
                    show_exit_message = True

        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    distribute_word()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isalpha():  # Acepta solo letras
                        if len(input_text) < grid_size[0] * grid_size[1]:
                            input_text += event.unicode

        elif event.type == pygame.MOUSEMOTION:
            if show_input_button:
                if button_rect.collidepoint(event.pos):
                    button_color = gray
                else:
                    button_color = white
            else:
                if play_again_rect.collidepoint(event.pos):
                    play_again_color = gray
                else:
                    play_again_color = white
                if yes_rect.collidepoint(event.pos):
                    yes_color = gray
                else:
                    yes_color = white
                if no_rect.collidepoint(event.pos):
                    no_color = gray
                else:
                    no_color = white

    if show_exit_message:
        exit_font = pygame.font.Font(None, 32)
        exit_text = exit_font.render('¡Gracias por jugar!', True, (0, 0, 255))
        exit_rect = exit_text.get_rect(center=(window_width // 2, window_height - 180))
        window.blit(exit_text, exit_rect)

    pygame.display.flip()
