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
    def save_database(database: Data_Base) -> None:
        logger.info("Started to save the database")
        File_Manager._save_pets(database.get_all_pets())
        File_Manager._save_appointments(database.get_appointments())
        File_Manager._save_owners(database.get_owners())
        logger.info("Database saved")


    def load_database(database: Data_Base) -> None:
        File_Manager._load_pets()
        File_Manager._load_appointments()
        File_Manager._load_owners()


    def _load_pets(database: Data_Base) -> None:
        pass


    def _load_appointments(database: Data_Base) -> None:
        pass


    def _load_owners(database: Data_Base) -> None:
        pass
    

    def _save_pets(pets: list[Pet], path: str=".\\..\\Datos", pets_file: str="Pets.csv") -> None:
        logger.info("Saving the pets")
        # w because we want to reset the database each time
        try:
            with open(path + pets_file, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(pets[0].to_dict().keys())  # Set the column names
                for pet in pets:  # Enter all the objets
                    writer.writerow(pet.to_dict().values())
                    logger.debug(f"saved the pet with id: {pet.id}")
        except FileNotFoundError:
            logger.error("The CSV file for the pets couldn't be found, pets were not saved")


    def _save_appointments(appointments: list[Appointment], path: str=".\\..\\Datos", appointment_folder: str="appoinments") -> None:
        logger.info("saving the appoinments")
        for appointment in appointments:
            json_val = File_Manager._convert_to_json(appointment)
            try: 
                with open(path + appointment_folder + f"\\apointment_{appointment.id}.json", "w") as file:
                    file.write(json_val)
                logger.debug(f"saved the appointment with id: {appointment.id}")
            except Exception as e:
                logger.error(f"Couldnt save appointment with id: {appointment.id}, error message: {e}")


    def _save_owners(owners: list[Owner], path: str=".\\..\\Datos", owners_file: str="Owners.csv") -> None:
        logger.info("Saving the owners")
        # w because we want to reset the database each time
        try:
            with open(path + owners_file, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(owners[0].to_dict().keys())  # Set the column names
                for owner in owners:  # Enter all the objets
                    writer.writerow(owner.to_dict().values())
                    logger.debug(f"saved the owner with id: {owner.id}")
        except FileNotFoundError:
            logger.error("The CSV file for the owners couldn't be found, owners were not saved")
        
        except Exception as e:
            logger.error(f"Couldn't finish saving all the owners, error message: {e}")
    

    def _convert_to_json(object: dict) -> str:
        return json.dumps(object)
