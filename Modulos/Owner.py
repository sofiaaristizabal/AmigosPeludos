
class Owner:
    def __init__(self, nombre:str, telefono: str, direccion: str, id: int):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.id = id  # TODO when creating an Owner add a way to get the id of the owner


    def __str__(self):
        return self.nombre
    

    def to_dict(self):
        return dict({
            "nombre": self.nombre,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "id": self.id
        })

