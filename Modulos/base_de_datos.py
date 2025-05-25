from Modulos.pet import Pet
from Modulos.owner import Owner
from Modulos.appointment import Appointment
from logging_config import set_up_logger
from Custom_Exceptions.owner_not_found_error import Owner_Not_Found_Error
from Custom_Exceptions.pet_not_found_error import Pet_Not_Found_Error

general_logger = set_up_logger(__name__, file_name="run_time_logger.log")

class Data_Base():
    def __init__(self):
        self._owners: list[Owner] = [
            Owner('Santiago Yepes', '3757353838', 'Siao Paulinho', 1),
            Owner('Sofia Aristizabal', '3454757474', 'Ilo durado', 2),
            Owner('Simon Gomez', '3758456363', 'Il Polles imeraldinha', 3)
        ]

        self._pets: list[Pet] = [
            Pet('Lucas', 'French Poodle', '11/02/2013', 'French Poodle', self._owners[0], 1),
            Pet('Ilo', 'Golden Retriever', '05/07/2018', 'Golden Retriever', self._owners[1], 2),
            Pet('Pollo', 'Bulldog', '23/09/2020', 'Bulldog', self._owners[2], 3)
        ]

        self._appointments: list[Appointment] = [
            Appointment('11/02/15', 'Vaccination', 'Teeth infection', self._pets[2], 1),
            Appointment('12/03/16', 'General Checkup', 'Healthy', self._pets[0], 2),
            Appointment('15/04/17', 'Deworming', 'Mild worms', self._pets[1], 3),
            Appointment('20/05/18', 'Vaccination', 'Allergic reaction', self._pets[2], 4),
            Appointment('22/06/19', 'Dental Cleaning', 'Tartar buildup', self._pets[0], 5),
            Appointment('30/07/20', 'Surgery', 'Neutering', self._pets[1], 6),
            Appointment('10/08/21', 'X-ray', 'Limping', self._pets[2], 7),
            Appointment('14/09/22', 'Blood Test', 'Routine check', self._pets[0], 8),
            Appointment('18/10/23', 'Vaccination', 'Healthy', self._pets[1], 9),
            Appointment('25/11/24', 'General Checkup', 'Minor cold', self._pets[2], 10)
        ]

    def find_owner_by_id(self, id: int):
        for owner in self._owners:
            if owner.id == id:
                return owner
            
        raise Owner_Not_Found_Error(id)
    
    def find_pet_by_id(self, id: int):
        for pet in self._pets:
            if pet.id == id:
                return pet
            
        raise Pet_Not_Found_Error(id)

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

    def get_next_pet_id(self,):
        if len(self._pets) == 0:
            return 1

        max_id = float("-inf")
        for pet in self._pets:
            if pet.id > max_id:
                max_id = pet.id

        return max_id + 1


    def get_next_owner_id(self,):
        if len(self._owners) == 0:
            return 1
        
        max_id = float("-inf")
        for owner in self._owners:
            if owner.id > max_id:
                max_id = owner.id

        return max_id + 1

    def get_next_appointment_id(self):
        if len(self._appointments) == 0:
            return 1
        
        max_id = float("-inf")
        for appointment in self._appointments:
            if appointment.id > max_id:
                max_id = appointment.id

        return max_id + 1
