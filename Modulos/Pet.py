from datetime import datetime, date
from Modulos.owner import Owner

class Pet:
    # Constructor
    def __init__(self, nombre: str, especie: str, fecha_de_nacimiento: str, raza: str, owner: Owner, id: int):
        self.nombre = nombre
        self.especie = especie
        self.fecha_de_nacimiento = fecha_de_nacimiento
        self.raza = raza
        self.owner = owner
        self.id = id

    """
    edad:
        1. Converts the birth date input into a date object
        2. gets today's date
        3. Checks if the pet's birthday has occured this year
            * If yes, substracts the birth year from the current year
            * If not, substracts one more year
        4. Returns the calculated age as an integer

    @property:
        Decorator used to define a method that can be accessed like an attribute
    """
    @property
    def age(self):
        fecha = datetime.strptime(self.fecha_de_nacimiento, "%d/%m/%Y").date()
        today = date.today()
        if (fecha.month,fecha.day) < (today.month, today.day):
            edad = today.year - fecha.year
        else:
            edad = today.year - fecha.year - 1

        return edad

    def __str__(self):
        return f'Mascota: {self.nombre}, edad:{self.age}, dueño: {self.owner.nombre} '

    """
    __eq__: Compares if two objects type Mascota are equal
                1. Verifies if the other is an instance of Mascota 
                2. Compares all attributes
            If all attributes are equal, returns True

            Returns True or False
    """
    def __eq__(self, other):
        if not isinstance(other, Pet):
            return False
        return (self.nombre == other.nombre and
                self.owner.nombre == other.owner.nombre and
                self.especie == other.especie and
                self.raza == other.raza and
                self.fecha_de_nacimiento == other.fecha_de_nacimiento)


    def to_dict(self):
        return dict({
            "nombre": self.nombre,
            "especie": self.especie,
            "fecha_de_nacimiento": self.fecha_de_nacimiento,
            "raza": self.raza,
            "owner": self.owner.id,
            "id": self.id,
        })
