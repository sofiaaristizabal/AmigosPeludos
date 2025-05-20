
class Owner:
    def __init__(self, nombre:str, telefono: str, direccion: str):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return self.nombre

