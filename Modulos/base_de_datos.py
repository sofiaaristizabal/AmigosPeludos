from Modulos.pet import Pet
from Modulos.owner import Owner
from Modulos.appointment import Query
from logging_config import set_up_logger

general_logger = set_up_logger(__name__, file_name="run_time_logger.log")

class Data_Base():
    def __init__(self):
        self._owners: list[Owner] = [
            Owner('Santiago Yepes', '3757353838', 'Siao Paulinho'),
            Owner('Sofia Aristizabal', '3454757474', 'Ilo durado'),
            Owner('Simon Gomez', '3758456363', 'Il Polles imeraldinha')
        ]

        self._pets: list[Pet] = [
            Pet('Lucas', 'French Poodle', '11/02/2013', 'French Poodle', self._owners[0]),
            Pet('Ilo', 'Golden Retriever', '05/07/2018', 'Golden Retriever', self._owners[1]),
            Pet('Pollo', 'Bulldog', '23/09/2020', 'Bulldog', self._owners[2])
        ]

        self._appointments: list[Query] = [
            Query('11/02/15', 'Vaccination', 'Teeth infection', self._pets[2]),
            Query('12/03/16', 'General Checkup', 'Healthy', self._pets[0]),
            Query('15/04/17', 'Deworming', 'Mild worms', self._pets[1]),
            Query('20/05/18', 'Vaccination', 'Allergic reaction', self._pets[2]),
            Query('22/06/19', 'Dental Cleaning', 'Tartar buildup', self._pets[0]),
            Query('30/07/20', 'Surgery', 'Neutering', self._pets[1]),
            Query('10/08/21', 'X-ray', 'Limping', self._pets[2]),
            Query('14/09/22', 'Blood Test', 'Routine check', self._pets[0]),
            Query('18/10/23', 'Vaccination', 'Healthy', self._pets[1]),
            Query('25/11/24', 'General Checkup', 'Minor cold', self._pets[2])
        ]

    def get_owners(self,):
        return self._owners.copy()

    def get_pets(self,):
        return self._pets.copy()

    def get_appointments(self,):
        return self._appointments.copy()

    def add_pet(self,mascota):
        self._pets.append(mascota)

    def add_owner(self,owner):
        self._owners.append(owner)

    def add_query(self,queries):
        self._appointments.append(queries)

    def find_pet(self,nombre_mascota, nombre_owner):
        for mascota in self._pets:
            if nombre_mascota == mascota.nombre and nombre_owner == mascota.owner.nombre:
                return mascota

        return None

    def find_owner(self,nombre_owner, telefono) -> Owner | None:
        for owner in self._owners:
            if owner.nombre == nombre_owner and owner.telefono == telefono:
                return owner

        return None

    def query_by_pet(self,nombre_mascota, nombre_owner):
        mascota = self.find_pet(nombre_mascota, nombre_owner)
        if not mascota:
            raise ValueError(f"Mascota con nombre '{nombre_mascota}' y dueno '{nombre_owner}' no encontrada")
        
        return [consulta for consulta in self._appointments if consulta.mascota == mascota]

    def registered_pets(self,):
        print('\n'.join(str(mascota) for mascota in self._pets))

    def get_all_pets(self,):
        return self._pets.copy()

    def get_next_pet_id(self,):
        pass  # TODO

    def get_next_owner_id(self,):
        pass  # TODO
