import json
import csv
import os
from .base_de_datos import Data_Base
from .appointment import Appointment
from .owner import Owner
from .pet import Pet
from logging_config import set_up_logger
import logging
from Custom_Exceptions.owner_not_found_error import Owner_Not_Found_Error

logger: logging.Logger = set_up_logger(
        __name__,
        file_name="file_manager.log",
    )


class File_Manager():
    def save_database(database: Data_Base) -> None:
        logger.info("Started to save the database")
        File_Manager._save_pets(database.get_pets())
        File_Manager._save_appointments(database.get_appointments())
        File_Manager._save_owners(database.get_owners())
        logger.info("Database saved")


    def load_database(database: Data_Base) -> None:
        File_Manager._load_owners(database)
        File_Manager._load_pets(database)
        File_Manager._load_appointments(database)


    def _load_pets(database: Data_Base, path: str="Datos", pets_file: str="\\Pets.csv") -> None:
        logger.info("Reading the pets into the database")
        try:
            with open(path + pets_file, 'r', newline='') as file:
                reader = csv.DictReader(file)

                number_pets_read: int = 0
                for row in reader:
                    try:
                        pet = Pet(
                            row.get("nombre"),
                            row.get("especie"),
                            row.get("fecha_de_nacimiento"),
                            row.get("raza"),
                            database.find_owner_by_id(int(row.get("owner"))),
                            int(row.get("id"))
                        )
                    except Owner_Not_Found_Error:
                        logger.error(f"The PET with id {row.get('id')} couldn't get loaded")
                        continue

                    database.add_pet(pet)
                    number_pets_read += 1
                    logger.debug(f"PET with id: {pet.id} LOADED")

            logger.info(f"PETS LOADED, count: {number_pets_read}")

        except FileNotFoundError:
            logger.error("PETS NOT READ, the CSV file for the pets couldn't be found")


    def _load_appointments(database: Data_Base, path: str="Datos", appointment_folder: str="\\appointments") -> None:
        number_appointment_count = 0
        for file_name in os.listdir(path + appointment_folder):
            if file_name == "placeholder.txt":
                continue

            with open(path + appointment_folder + "\\" + file_name, "r") as file:
                result = json.load(file)
                appointment = Appointment(
                    result["fecha"],
                    result["motivo"],
                    result["diagnostico"],
                    database.find_pet_by_id(int(result["id_mascota"])),
                    int(result["id"])
                )

                database.add_query(appointment)
                number_appointment_count += 1
                logger.debug(f"APPOINTMENT with id: {appointment.id} LOADED")

        logger.info(f"APPOINTMENTS LOADED, count: {number_appointment_count}")


    def _load_owners(database: Data_Base, path: str="Datos", owners_file: str="\\Owners.csv") -> None:
        logger.info("Reading the owners into the database")
        try:
            with open(path + owners_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                
                number_owners_read = 0

                for row in reader:
                    owner = Owner(
                        row.get("nombre"),
                        row.get("telefono"),
                        row.get("direccion"),
                        int(row.get("id"))
                    )

                    database.add_owner(owner)
                    number_owners_read += 1
                    logger.debug(f"owner with id: {owner.id}, has been loaded")

                logger.info(f"OWNERS LOADED, count: {number_owners_read}")
        
        except FileNotFoundError:
            logger.erro("OWNERS NOT READ, the CSV file for the owners couldn't be found")
    

    def _save_pets(pets: list[Pet], path: str="Datos", pets_file: str="\\Pets.csv") -> None:
        logger.info("Saving the pets")
        # w because we want to reset the database each time
        try:
            with open(path + pets_file, 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(pets[0].to_dict().keys())  # Set the column names
                for pet in pets:  # Enter all the objets
                    writer.writerow(pet.to_dict().values())
                    logger.debug(f"saved the pet with id: {pet.id}")
        except FileNotFoundError:
            logger.error("PETS NOT SAVED, the CSV file for the pets couldn't be found")


    def _save_appointments(appointments: list[Appointment], path: str="Datos", appointment_folder: str="\\appointments") -> None:
        logger.info("saving the appoinments")
        for appointment in appointments:
            json_val = File_Manager._convert_to_json(appointment.to_dict())
            try: 
                with open(path + appointment_folder + f"\\apointment_{appointment.id}.json", "w") as file:
                    file.write(json_val)
                logger.debug(f"saved the appointment with id: {appointment.id}")
            except Exception as e:
                logger.error(f"Couldn't save appointment with id: {appointment.id}, error message: {e}")


    def _save_owners(owners: list[Owner], path: str="Datos", owners_file: str="\\Owners.csv") -> None:
        logger.info("Saving the owners")
        # w because we want to reset the database each time
        try:
            with open(path + owners_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(owners[0].to_dict().keys())  # Set the column names
                for owner in owners:  # Enter all the objets
                    writer.writerow(owner.to_dict().values())
                    logger.debug(f"saved the owner with id: {owner.id}")
        except FileNotFoundError:
            logger.error("OWNERS NOT SAVED, the CSV file for the owners couldn't be found")
        
        except Exception as e:
            logger.error(f"Couldn't finish saving all the owners, error message: {e}")
    

    def _convert_to_json(object: dict) -> str:
        return json.dumps(object)
