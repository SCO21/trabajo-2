from letra_correcta import LetraCorrecta

class Wordle:
    
    intentos_maximos = 6
    
    def __init__(self, secret: str, longitud_palabra: int):
        self.secret: str = secret.upper()
        self.longitud_palabra = longitud_palabra
        self.intentos = []

    def intento(self, palabra: str):
        palabra = palabra.upper()
        self.intentos.append(palabra)

    def guess(self, palabra: str):
        palabra = palabra.upper()
        result = []
        for i in range(self.longitud_palabra):
            character = palabra[i]
            letra = LetraCorrecta(character)
            letra.esta_en_la_palabra = character in self.secret
            letra.esta_en_la_posicion = character == self.secret[i]
            result.append(letra)
        return result
    
    @property
    def resuelto(self):
        return len(self.intentos) > 0 and self.intentos[-1] == self.secret
    
    @property
    def intentos_restantes(self) -> int:
         return self.intentos_maximos - len(self.intentos)
         
    @property
    def puede_intentar(self):
        return self.intentos_restantes > 0 and not self.resuelto
        