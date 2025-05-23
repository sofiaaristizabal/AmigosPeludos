import json
from base_de_datos import Data_Base

class File_Manager():
    def __init__(self, path=".\\..\\datos"):
        self.path = path
        self.appointment_folder = "appoinments"
        self.owner_folder = "owners"
        self.pet_folder = "pets"


    def save_database(self, database: Data_Base):
        self._save_pets(database.get_all_pets())
        self._save_appointments(database.get_appointments())
        self._save_owners(database.get_owners())


    def load_database(self):
        self._load_pets()
        self._load_appointments()
        self._load_owners()


    def _load_pets(self):
        pass


    def _load_appointments(self):
        pass


    def _load_owners(self):
        pass
    

    def _save_pets(self, pets):
        pass


    def _save_appointments(self, appointments):
        pass


    def _save_owners(self, appointments):
        pass
    