
class Owner:
    def __init__(self, nombre:str, telefono: str, direccion: str, id: int):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.id = id


    def __str__(self):
        return f"Owner(nombre='{self.nombre}', telefono='{self.telefono}', direccion='{self.direccion}', id={self.id})"
    

    def to_dict(self):
        return dict({
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "id": self.id
        })

