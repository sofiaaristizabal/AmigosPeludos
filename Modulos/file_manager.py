import json
from base_de_datos import Data_Base
from appointment import Appointment
from owner import Owner
from pet import Pet

class File_Manager():
    def __init__(self, path=".\\..\\datos"):
        self.path = path
        self.appointment_folder = "appoinments"
        self.owner_folder = "owners"
        self.pet_folder = "pets"


    def save_database(self, database: Data_Base) -> None:
        self._save_pets(database.get_all_pets())
        self._save_appointments(database.get_appointments())
        self._save_owners(database.get_owners())


    def load_database(self, database: Data_Base) -> None:
        self._load_pets()
        self._load_appointments()
        self._load_owners()


    def _load_pets(self, database: Data_Base) -> None:
        pass


    def _load_appointments(self, database: Data_Base) -> None:
        pass


    def _load_owners(self, database: Data_Base) -> None:
        pass
    

    def _save_pets(self, pets: list[Pet]) -> None:
        pass


    def _save_appointments(self, appointments: list[Appointment]) -> None:
        pass


    def _save_owners(self, owners: list[Owner]) -> None:
        pass
    