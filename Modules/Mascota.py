from datetime import datetime, date

class Mascota:

    def __init__(self, nombre, especie, fecha_de_nacimiento, raza, owner):
        self.nombre = nombre
        self.especie = especie
        self.fecha_de_nacimiento = fecha_de_nacimiento
        self.raza = raza
        self.owner = owner

    #Creamos un metodo edad que calcula la edad de la mascota a partir de su fecha de nacimiento y utilizamos un built-in decorator para convertir el metodo en atributo
    @property
    def edad(self):
        fecha = datetime.strptime(self.fecha_de_nacimiento, "%d/%m/%Y").date()
        today = date.today()
        if (fecha.month,fecha.day) < (today.month, today.day):
            edad = today.year - fecha.year
        else:
            edad = today.year - fecha.year - 1

        return edad

    def __str__(self):
        return f'Mascota: {self.nombre}, edad:{self.edad}, dueño: {self.owner.nombre} '

    def __eq__(self, other):
        if not isinstance(other, Mascota):
            return False
        return (self.nombre == other.nombre and
                self.owner.nombre == other.owner.nombre and
                self.especie == other.especie and
                self.raza == other.raza and
                self.fecha_de_nacimiento == other.fecha_de_nacimiento)


