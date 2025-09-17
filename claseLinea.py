class Linea:
    def __init__(self, numero, texto):
        self.numero = numero
        self.texto = texto

    def __repr__(self):
        return f"{self.numero}: {self.texto}"

    def __str__(self):
        return f"{self.numero}: {self.texto}"
