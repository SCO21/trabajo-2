from letra_correcta import LetraCorrecta

class Wordle:
    
    intentos_maximos = 6
    
    def __init__(self, secret: str, longitud_palabra: int):
        self.secret: str = secret.upper()
        self.longitud_palabra = longitud_palabra
        self.intentos = []
        self.letras_secret = self.contar_secreto()

    def intento(self, palabra: str):
        palabra = palabra.upper()
        self.intentos.append(palabra)

    def guess(self, palabra: str):
        palabra = palabra.upper()
        result = []
        diccionario = self.contar_letras(palabra)
        for i in range(self.longitud_palabra):
            character = palabra[i]
            letra = LetraCorrecta(character)
            letra.esta_en_la_palabra = character in self.secret
            letra.esta_en_la_posicion = character == self.secret[i]
            if(not letra.esta_en_la_posicion and letra.esta_en_la_palabra):
                self.validarPosicion(character, letra, diccionario)
            result.append(letra)
        return result
    
    def validarPosicion(self,character, letra, diccionario):
        caracter_palabra = diccionario["palabra"][character]
        caracter_secreto = diccionario["secret"][character]
        if(caracter_palabra > caracter_secreto):
            letra.esta_en_la_palabra = False

    def contar_letras(self, palabra):
        dic_aux = {
            "secret": self.letras_secret,
            "palabra": {},
        }
        # Contar frecuencia de letras en palabra
        for character in palabra:
            if character not in dic_aux["palabra"]:
                dic_aux["palabra"][character] = 1
            else:
                dic_aux["palabra"][character] += 1

        return dic_aux
    
    def contar_secreto(self):
        dic_aux = {}
        for character in self.secret:
            if character not in dic_aux:
                dic_aux[character] = 1
            else:
                dic_aux[character] += 1
        return dic_aux
               
    
    @property
    def resuelto(self):
        return len(self.intentos) > 0 and self.intentos[-1] == self.secret
    
    @property
    def intentos_restantes(self) -> int:
         return self.intentos_maximos - len(self.intentos)

    @property
    def puede_intentar(self):
        return self.intentos_restantes > 0 and not self.resuelto
        