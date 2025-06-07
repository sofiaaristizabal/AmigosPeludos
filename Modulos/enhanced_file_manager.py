import json
import csv
import os
from .base_de_datos import Data_Base
from .appointment import Appointment
from .owner import Owner
from .pet import Pet
from .sqlite_manager import SQLite_Manager
from logging_config import set_up_logger
import logging
from Modulos.Custom_Exceptions.owner_not_found_error import Owner_Not_Found_Error

logger: logging.Logger = set_up_logger(
    __name__,
    file_name="file_manager.log",
)


class Enhanced_File_Manager:
    def __init__(self):
        """Initialize the enhanced file manager with SQLite support."""
        try:
            self.sqlite_manager = SQLite_Manager()
            logger.info("Enhanced File Manager initialized with SQLite support")
        except Exception as e:
            logger.error(f"Failed to initialize SQLite manager: {e}")
            self.sqlite_manager = None

    @staticmethod
    def save_database(database: Data_Base) -> None:
        """Save database to both file formats and SQLite."""
        logger.info("Started to save the database")

        # Save to SQLite
        try:
            sqlite_manager = SQLite_Manager()
            Enhanced_File_Manager._save_to_sqlite(database, sqlite_manager)
        except Exception as e:
            logger.error(f"Failed to save to SQLite: {e}")

        # Save to traditional formats (CSV/JSON)
        Enhanced_File_Manager._save_pets(database.get_pets())
        Enhanced_File_Manager._save_appointments(database.get_appointments())
        Enhanced_File_Manager._save_owners(database.get_owners())

        logger.info("Database saved to all formats")


    @staticmethod
    def load_database(database: Data_Base) -> None:
        """Load database from SQLite first, then fall back to CSV/JSON if needed."""
        logger.info("Starting to load database")

        try:
            sqlite_manager = SQLite_Manager()
            if Enhanced_File_Manager._load_from_sqlite(database, sqlite_manager):
                logger.info("Database loaded successfully from SQLite")
                return
            else:
                logger.warning("SQLite load failed, falling back to CSV/JSON")
        except Exception as e:
            logger.error(f"SQLite loading error: {e}, falling back to CSV/JSON")
            # Fall back to traditional loading
            Enhanced_File_Manager._load_owners(database)
            Enhanced_File_Manager._load_pets(database)
            Enhanced_File_Manager._load_appointments(database)
            logger.info("Database loaded from CSV/JSON files")

    @staticmethod
    def _save_to_sqlite(database: Data_Base, sqlite_manager: SQLite_Manager) -> bool:
        """Save all data to SQLite database."""
        try:
            success_count = 0
            total_operations = 0

            # Save owners first (due to foreign key relationships)
            owners = database.get_owners()
            for owner in owners:
                total_operations += 1
                if sqlite_manager.save_owner(owner):
                    success_count += 1

            # Save pets (they reference owners)
            pets = database.get_pets()
            for pet in pets:
                total_operations += 1
                if sqlite_manager.save_pet(pet):
                    success_count += 1

            # Save appointments (they reference pets)
            appointments = database.get_appointments()
            for appointment in appointments:
                total_operations += 1
                if sqlite_manager.save_appointment(appointment):
                    success_count += 1

            logger.info(f"SQLite save completed: {success_count}/{total_operations} operations successful")
            return success_count == total_operations

        except Exception as e:
            logger.error(f"Error saving to SQLite: {e}")
            return False

    @staticmethod
    def _load_from_sqlite(database: Data_Base, sqlite_manager: SQLite_Manager) -> bool:
        """Load all data from SQLite database."""
        try:
            # Load owners first
            owners = sqlite_manager.load_owners()
            if not owners:
                logger.warning("No owners found in SQLite database")
                return False

            # Create owners dictionary for reference
            owners_dict = {owner.id: owner for owner in owners}

            # Add owners to database
            for owner in owners:
                database.add_owner(owner)

            # Load pets
            pets = sqlite_manager.load_pets(owners_dict)
            pets_dict = {pet.id: pet for pet in pets}

            # Add pets to database
            for pet in pets:
                database.add_pet(pet)

            # Load appointments
            appointments = sqlite_manager.load_appointments(pets_dict)

            # Add appointments to database
            for appointment in appointments:
                database.add_query(appointment)

            logger.info(
                f"SQLite load completed: {len(owners)} owners, {len(pets)} pets, {len(appointments)} appointments")
            return True

        except Exception as e:
            logger.error(f"Error loading from SQLite: {e}")
            return False

    @staticmethod
    def get_database_status() -> dict:
        """Get status information about all database formats."""
        status = {
            'sqlite': {'available': False, 'info': {}},
            'csv_files': {'owners': False, 'pets': False},
            'json_files': {'appointments_count': 0}
        }

        # Check SQLite status
        try:
            sqlite_manager = SQLite_Manager()
            status['sqlite']['available'] = True
            status['sqlite']['info'] = sqlite_manager.get_database_info()
        except Exception as e:
            logger.error(f"Error checking SQLite status: {e}")

        # Check CSV files
        try:
            status['csv_files']['owners'] = os.path.exists("Datos/Owners.csv")
            status['csv_files']['pets'] = os.path.exists("Datos/Pets.csv")
        except Exception as e:
            logger.error(f"Error checking CSV files: {e}")

        # Check JSON appointment files
        try:
            appointment_path = "Datos/appointments"
            if os.path.exists(appointment_path):
                files = [f for f in os.listdir(appointment_path) if f.endswith('.json')]
                status['json_files']['appointments_count'] = len(files)
        except Exception as e:
            logger.error(f"Error checking JSON files: {e}")

        return status

    @staticmethod
    def sync_databases(database: Data_Base) -> bool:
        """Synchronize data between SQLite and CSV/JSON formats."""
        try:
            logger.info("Starting database synchronization")

            # Save to all formats
            Enhanced_File_Manager.save_database(database, use_sqlite=True)

            # Verify synchronization by comparing counts
            status = Enhanced_File_Manager.get_database_status()
            sqlite_info = status.get('sqlite', {}).get('info', {})

            owners_count = len(database.get_owners())
            pets_count = len(database.get_pets())
            appointments_count = len(database.get_appointments())

            sqlite_owners = sqlite_info.get('owners_count', 0)
            sqlite_pets = sqlite_info.get('pets_count', 0)
            sqlite_appointments = sqlite_info.get('appointments_count', 0)

            sync_success = (
                    owners_count == sqlite_owners and
                    pets_count == sqlite_pets and
                    appointments_count == sqlite_appointments
            )

            if sync_success:
                logger.info("Database synchronization completed successfully")
            else:
                logger.warning(
                    f"Synchronization mismatch - Memory: {owners_count}/{pets_count}/{appointments_count}, SQLite: {sqlite_owners}/{sqlite_pets}/{sqlite_appointments}")

            return sync_success

        except Exception as e:
            logger.error(f"Error during database synchronization: {e}")
            return False

    # Keep all the original methods for backward compatibility
    @staticmethod
    def _load_pets(database: Data_Base, path: str = "Datos", pets_file: str = "\\Pets.csv") -> None:
        logger.info("Reading the pets into the database")
        try:
            with open(path + pets_file, 'r', newline='') as file:
                reader = csv.DictReader(file)

                number_pets_read: int = 0
                for row in reader:
                    try:
                        ####################Solución a typos############################
                        # Verificar owner
                        owner_id = row.get("owner")
                        if owner_id is None:
                            logger.error(f"Pet with id {row.get('id')} has no owner id")
                            continue
                        try:
                            owner_id_int = int(owner_id)
                        except ValueError:
                            logger.error(f"Owner id '{owner_id}' is not a valid integer")
                            continue
                        # Fin de nueva verif

                        # Verificar Pet id
                        pet_id = row.get("id")
                        if pet_id is None:
                            logger.error(f"Pet row is missing 'id': {row}")
                            continue
                        try:
                            pet_id_int = int(pet_id)
                        except ValueError:
                            logger.error(f"Pet id '{pet_id}' is not a valid integer")
                            continue
                        # Fin de nueva verif 2
                        ###############################################################
                        pet = Pet(
                            row.get("nombre") or "",
                            row.get("especie") or "",
                            row.get("fecha_de_nacimiento") or "",
                            row.get("raza") or "",
                            database.find_owner_by_id(owner_id_int),
                            pet_id_int
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

    @staticmethod
    def _load_appointments(database: Data_Base, path: str = "Datos",
                           appointment_folder: str = "\\appointments") -> None:
        logger.info("Reading the appointments into the database")
        number_appointment_count = 0

        try:
            for file_name in os.listdir(path + appointment_folder):
                if file_name == "placeholder.txt":
                    continue

                try:
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

                except Exception as e:
                    logger.error(f"Error loading appointment from {file_name}: {e}")
                    continue

            logger.info(f"APPOINTMENTS LOADED, count: {number_appointment_count}")

        except FileNotFoundError:
            logger.error("APPOINTMENTS NOT READ, the appointments folder couldn't be found")
        except Exception as e:
            logger.error(f"Error reading appointments directory: {e}")

    @staticmethod
    def _load_owners(database: Data_Base, path: str = "Datos", owners_file: str = "\\Owners.csv") -> None:
        logger.info("Reading the owners into the database")
        try:
            with open(path + owners_file, 'r', newline='') as file:
                reader = csv.DictReader(file)

                number_owners_read = 0

                for row in reader:
                    # Validate owner id
                    owner_id = row.get("id")
                    if owner_id is None:
                        logger.error(f"Owner row is missing 'id': {row}")
                        continue
                    try:
                        owner_id_int = int(owner_id)
                    except ValueError:
                        logger.error(f"Owner id '{owner_id}' is not a valid integer")
                        continue

                    owner = Owner(
                        row.get("nombre") or "",
                        row.get("telefono") or "",
                        row.get("direccion") or "",
                        owner_id_int
                    )

                    database.add_owner(owner)
                    number_owners_read += 1
                    logger.debug(f"owner with id: {owner.id}, has been loaded")

                logger.info(f"OWNERS LOADED, count: {number_owners_read}")

        except FileNotFoundError:
            logger.error("OWNERS NOT READ, the CSV file for the owners couldn't be found")

    @staticmethod
    def _save_pets(pets: list[Pet], path: str = "Datos", pets_file: str = "\\Pets.csv") -> None:
        logger.info("Saving the pets")
        # w because we want to reset the database each time
        try:
            if len(pets) == 0:
                logger.warning("No pets to save")
                return

            with open(path + pets_file, 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(pets[0].to_dict().keys())
                for pet in pets:
                    writer.writerow(pet.to_dict().values())
                    logger.debug(f"saved the pet with id: {pet.id}")
        except FileNotFoundError:
            logger.error("PETS NOT SAVED, the CSV file for the pets couldn't be found")
        except Exception as e:
            logger.error(f"Error saving pets: {e}")

    @staticmethod
    def _save_appointments(appointments: list[Appointment], path: str = "Datos",
                           appointment_folder: str = "\\appointments") -> None:
        logger.info("saving the appointments")
        for appointment in appointments:
            json_val = Enhanced_File_Manager._convert_to_json(appointment.to_dict())
            try:
                with open(path + appointment_folder + f"\\appointment_{appointment.id}.json", "w") as file:
                    file.write(json_val)
                logger.debug(f"saved the appointment with id: {appointment.id}")
            except Exception as e:
                logger.error(f"Couldn't save appointment with id: {appointment.id}, error message: {e}")

    @staticmethod
    def _save_owners(owners: list[Owner], path: str = "Datos", owners_file: str = "\\Owners.csv") -> None:
        logger.info("Saving the owners")
        try:
            if len(owners) == 0:
                logger.warning("No owners to save")
                return

            with open(path + owners_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(owners[0].to_dict().keys())
                for owner in owners:
                    writer.writerow(owner.to_dict().values())
                    logger.debug(f"saved the owner with id: {owner.id}")
        except FileNotFoundError:
            logger.error("OWNERS NOT SAVED, the CSV file for the owners couldn't be found")
        except Exception as e:
            logger.error(f"Couldn't finish saving all the owners, error message: {e}")

    @staticmethod
    def _convert_to_json(object: dict) -> str:
        return json.dumps(object)
