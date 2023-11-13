class LetraCorrecta:
    def __init__(self, charcater: str):
        self.character: str = charcater
        self.esta_en_la_palabra: bool = False
        self.esta_en_la_posicion: bool = False
        pass
    
    #metodo que permite devolver una representacion legible de los atributos del objeto e informacion relevante
    #en este caso lo usamos para que nos devuelva un true o false dependiendo si la letra esta en la palabra y la posicion correcta
    
    def __repr__(self):
        return f"[{self.character} esta_en_la_palabra: {self.esta_en_la_palabra} esta_en_la_posicion: {self.esta_en_la_posicion} ]"
         