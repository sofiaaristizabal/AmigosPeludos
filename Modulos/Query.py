
class Query:

    def __init__(self, fecha, motivo: str, diagnostico: str, mascota):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota = mascota

    def __str__(self):
        return f'\n Consulta para {self.mascota.nombre} con motivo de {self.motivo} el dia {self.fecha}. El diagnostico fue: {self.diagnostico} \n'