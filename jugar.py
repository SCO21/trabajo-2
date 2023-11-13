
from typing import List
from wordle import Wordle
from letra_correcta import LetraCorrecta
from colorama import Fore #sirve para cambiar el color del texto de la terminal
import random
print("Bienvenido a Wordle\n")
print("Ingresa la longitud de la palabra que quieres adivinar! (4 a 8)")
C = int(input())

#carga un conjunto (set) de palabras desde un archivo de texto especificado por la ruta path.     
def load_word_set(path: str):
    word_set = set()
    with open(path,"r") as f:
        for line in f.readlines():
            word = line.strip().upper()
            word_set.add(word)
    return word_set
def main():
    word_set = load_word_set("lema4.txt")  # Asigna un valor predeterminado a word_set
    wordle = None
    if C == 4:
        word_set = load_word_set("lema4.txt")
        secret = random.choice(list(word_set))
        wordle = Wordle(secret, C)
    elif C==5:
        word_set = load_word_set("lema5.txt")
        secret = random.choice(list(word_set))
        wordle = Wordle(secret, C)
    elif C==6:
        word_set = load_word_set("lema6.txt")
        secret = random.choice(list(word_set))
        wordle = Wordle(secret, C)
    elif C==7:
        word_set = load_word_set("lema7.txt")
        secret = random.choice(list(word_set))
        wordle = Wordle(secret, C)
    elif C==8:
        word_set = load_word_set("lema8.txt")
        secret = random.choice(list(word_set))
        wordle = Wordle(secret, C)  
        
    while wordle.puede_intentar:
        x = input("\nIngresa tu intento: ")
        x = x.upper()
        if len(x) != C:
            print(Fore.RED + f"La palabra debe ser de {C} letras" + Fore.RESET)
            continue
        if x not in word_set:
            print(Fore.RED + f"La palabra no esta en el lemario" + Fore.RESET)
            continue
        wordle.intento(x)
        resultados_en_pantalla(wordle)
        
    if wordle.resuelto:
        print("Palabra correcta")
    else:
        print("La palabra correcta era", secret)

def resultados_en_pantalla(wordle: Wordle):
    print(f"\ntienes {wordle.intentos_restantes} itentos restantes")
    
    lines = []
    for word in wordle.intentos:
        result = wordle.guess(word)
        color_final = convertir_a_color(result)
        lines.append(color_final)
    for _ in range (wordle.intentos_restantes):
        lines.append(" " .join( ["_"] * wordle.longitud_palabra))
    
    dibujar_borde(lines)



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

def dibujar_borde(lines: List[str], size:int = 2*C - 1, pad: int = 1):
    
    contenido_total = size + pad * 2
    borde_superior = "┌" + "─" *contenido_total + "┐"
    borde_inferior = "└" + "─" *contenido_total + "┘"
    print(borde_superior)
    
    for linea in lines:
        print("│", linea, "│")
        
    print(borde_inferior)




if __name__ == "__main__":
    main()