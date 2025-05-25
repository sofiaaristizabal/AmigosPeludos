import json
import csv
from base_de_datos import Data_Base
from appointment import Appointment
from owner import Owner
from pet import Pet
from logging_config import set_up_logger
import logging

logger: logging.Logger = set_up_logger(
        __name__,
        file_name="file_manager.log",
    )


class File_Manager():
    def __init__(self, path: str=".\\..\\Datos"):
        self.path: str = path
        self.appointment_folder: str = "appoinments"
        self.owners_file: str = "Owners.csv"
        self.pets_file: str = "Pets.csv"


    def save_database(self, database: Data_Base) -> None:
        logger.info("Started to save the database")
        self._save_pets(database.get_all_pets())
        self._save_appointments(database.get_appointments())
        self._save_owners(database.get_owners())
        logger.info("Database saved")


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
        logger.info("Saving the pets")
        # w because we want to reset the database each time
        try:
            with open(self.path + self.pets_file, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(pets[0].to_dict().keys())  # Set the column names
                for pet in pets:  # Enter all the objets
                    writer.writerow(pet.to_dict().values())
                    logger.debug(f"saved the pet with id: {pet.id}")
        except FileNotFoundError:
            logger.error("The CSV file for the pets couldn't be found, pets were not saved")


    def _save_appointments(self, appointments: list[Appointment]) -> None:
        logger.info("saving the appoinments")
        for appointment in appointments:
            json_val = self._convert_to_json(appointment)
            try: 
                with open(self.path + self.appointment_folder + f"\\apointment_{appointment.id}.json", "w") as file:
                    file.write(json_val)
                logger.debug(f"saved the appointment with id: {appointment.id}")
            except Exception as e:
                logger.error(f"Couldnt save appointment with id: {appointment.id}, error message: {e}")


    def _save_owners(self, owners: list[Owner]) -> None:
        logger.info("Saving the owners")
        # w because we want to reset the database each time
        try:
            with open(self.path + self.owners_file, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(owners[0].to_dict().keys())  # Set the column names
                for owner in owners:  # Enter all the objets
                    writer.writerow(owner.to_dict().values())
                    logger.debug(f"saved the owner with id: {owner.id}")
        except FileNotFoundError:
            logger.error("The CSV file for the owners couldn't be found, owners were not saved")
        
        except Exception as e:
            logger.error(f"Couldn't finish saving all the owners, error message: {e}")
    

    def _convert_to_json(self, object: dict) -> str:
        return json.dumps(object)
