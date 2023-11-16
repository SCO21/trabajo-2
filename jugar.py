from typing import List
from wordle import Wordle
from letra_correcta import LetraCorrecta
from colorama import Fore #sirve para cambiar el color del texto de la terminal
import random
print("Bienvenido a Wordle\n")

ACIERTOS = 0
FALLOS = 0

def load_word_set(path: str):
    word_set = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            word = line.strip().upper()
            word_set.add(word)
    return word_set

def main():
    global ACIERTOS, FALLOS
    print("Ingresa la longitud de la palabra que quieres adivinar! (4 a 8)")

    while True:
        try:
            C = int(input())
            break
        except ValueError:
            print(Fore.RED + "Error: Ingresa un número entero válido." + Fore.RESET)

    word_set = load_word_set(f"lema{C}.txt")
    wordle = Wordle(random.choice(list(word_set)), C)

    while wordle.puede_intentar:
        x = input("\nIngresa tu intento: ").upper()
        if len(x) != C:
            print(Fore.RED + f"La palabra debe ser de {C} letras" + Fore.RESET)
            continue
        if x not in word_set:
            print(Fore.RED + "La palabra no está en el lemario" + Fore.RESET)
            continue
        wordle.intento(x)
        resultados_en_pantalla(wordle)

    if wordle.resuelto:
        print("Palabra correcta")
        ACIERTOS += 1
    else:
        print("La palabra correcta era", wordle.secret)
        FALLOS += 1

    print("\n" + Fore.GREEN + "Aciertos " + Fore.RESET + f"{ACIERTOS}" + Fore.RED + " Fallos " + Fore.RESET + f"{FALLOS}")

    volver_a_jugar = input("\n¿Quieres volver a jugar? Y/N: ")
    if volver_a_jugar.lower() == "y":
        main()
    else:
        print("\n¡Gracias por jugar!")


def resultados_en_pantalla(wordle: Wordle):
    print(f"\ntienes {wordle.intentos_restantes} intentos restantes")
    lines = []
    for word in wordle.intentos:
        result = wordle.guess(word)
        color_final = convertir_a_color(result)
        lines.append(color_final)
    for _ in range(wordle.intentos_restantes):
        lines.append(" " .join(["_"] * wordle.longitud_palabra))
    dibujar_borde(lines, wordle.longitud_palabra)


def convertir_a_color(result: List[LetraCorrecta]):
    resultado_coloreado = []
    for letra in result:
        if letra.esta_en_la_posicion:
            color = Fore.GREEN
        elif letra.esta_en_la_palabra:
            color = Fore.YELLOW
        else:
            color = Fore.WHITE
        letra_coloreada = color + letra.character + Fore.RESET
        resultado_coloreado.append(letra_coloreada)
    return " ".join(resultado_coloreado)


def dibujar_borde(lines: List[str], longitud_palabra: int, pad: int = 1):
    contenido_total = 2 * longitud_palabra - 1 + pad * 2
    borde_superior = "┌" + "─" * contenido_total + "┐"
    borde_inferior = "└" + "─" * contenido_total + "┘"
    print(borde_superior)
    for linea in lines:
        print("│", linea, "│")
    print(borde_inferior)


if __name__ == "__main__":
    main()