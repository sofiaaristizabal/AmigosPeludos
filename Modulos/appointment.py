from Modulos.pet import Pet

class Appointment:
    def __init__(self, fecha, motivo: str, diagnostico: str, mascota: Pet, id: int):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota = mascota
        self.id = id


    def __str__(self):
        return f'\n Consulta para {self.mascota.nombre} con motivo de {self.motivo} el dia {self.fecha}. El diagnostico fue: {self.diagnostico} \n'
    

    def to_dict(self):
        return dict({
            "fecha": self.fecha,
            "motivo": self.motivo,
            "diagnostico": self.diagnostico,
            "id_mascota": self.mascota.id,
        })