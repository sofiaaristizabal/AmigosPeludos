import json
import sqlite3
from typing import List

from Modulos.owner import Owner
from Modulos.pet import Pet
from Modulos.appointment import Appointment
from logging_config import set_up_logger
import logging

logger: logging.Logger = set_up_logger(
    __name__,
    file_name="sqlite_manager.log",
)


class SQLite_Manager:
    def __init__(self, db_path: str = "Datos/amigosPeludos.db"):
        """Initialize SQLite database connection and create tables if they don't exist."""
        self.db_path = db_path
        # self._create_tables()
        logger.info("SQLite manager initialized")

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with proper error handling."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f'Error connecting to database: {e}')
            raise

    def _create_tables(self) -> None:
        """Create the necessary tables if they don't exist."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Create the table owners
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS owners(
                   id INTEGER PRIMARY KEY,
                   nombre TEXT NOT NULL
                   telefono TEXT NOT NULL
                   direccion TEXT NOT NULL
                )
                ''')

                # Create pets table
                cursor.execute('''
                     CREATE TABLE IF NOT EXISTS pets (
                            id INTEGER PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            especie TEXT NOT NULL,
                            fecha_de_nacimiento TEXT NOT NULL,
                            raza TEXT NOT NULL,
                            owner_id INTEGER NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (owner_id) REFERENCES owners (id)
                            )
                        ''')

                # Create appointments table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY,
                        fecha TEXT NOT NULL,
                        motivo TEXT NOT NULL,
                        diagnostico TEXT NOT NULL,
                        pet_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (pet_id) REFERENCES pets (id)
                    )
                ''')

        except sqlite3.Error as e:
            logger.error(f'Error creatig tables: {e}')
            raise

    def save_owner(self, owner: Owner) -> bool:
        """Save an owner to the database"""

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT OR REPLACE INTO owners (id, nombre, telefono, direccion)
                VALUES(?,?,?,?)
                ''', (owner.id, owner.nombre, owner.telefono, owner.direccion))

                conn.commit()
                logger.debug(f'Owner with id {owner.id} saved to SQLite')
                return True
        except sqlite3.Error as e:
            logger.error(f'Error saving owner {owner.id}: {e}')
            return False

    def save_pet(self, pet: Pet) -> bool:
        """Save a pet to the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO pets (id, nombre, especie, fecha_de_nacimiento, raza, owner_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (pet.id, pet.nombre, pet.especie, pet.fecha_de_nacimiento, pet.raza, pet.owner.id))

                conn.commit()
                logger.debug(f"Pet with id {pet.id} saved to SQLite")
                return True

        except sqlite3.Error as e:
            logger.error(f"Error saving pet {pet.id}: {e}")
            return False

    def save_appointment(self, appointment: Appointment) -> bool:
        """Save an appointment to the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO appointments (id, fecha, motivo, diagnostico, pet_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (appointment.id, appointment.fecha, appointment.motivo, appointment.diagnostico,
                      appointment.mascota.id))

                conn.commit()
                logger.debug(f"Appointment with id {appointment.id} saved to SQLite")
                return True

        except sqlite3.Error as e:
            logger.error(f"Error saving appointment {appointment.id}: {e}")
            return False

    def load_owners(self) -> List[Owner]:
        """Load all owners from the database"""
        owners = []

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, nombre, telefono, direccion FROM owners ORDER BY id')
                rows = cursor.fetchall()

                for row in rows:
                    owner = Owner(row['nombre'], row['telefono'], row['direccion'], row['id'])
                    owners.append(owner)
                    logger.debug(f'Owner with id {owner.id} loaded from SQLite')

                logger.info(f'Loaded {len(owners)} owners from sqlite')

        except sqlite3.Error as e:
            logger.error(f'Error loading owners: {e}')

        return owners

    def load_pets(self, owners_dict: dict) -> List[Pet]:
        """Load all pets from database."""
        pets =[]
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT id, nombre, especie, fecha_de_nacimiento, raza, owner_id
                FROM pets ORDER BY id
                ''')

                rows = cursor.fetchall()

                for row in rows:
                    try:
                        owner = owners_dict.get(row['owner_id'])
                        if owner is None:
                            logger.error(f"Owner with id {row['owner_id']} not found for pet {row['id']}")
                            continue
                        pet = Pet(
                            row['nombre'],
                            row['especie'],
                            row['fecha_de_nacimiento'],
                            row['raza'],
                            owner,
                            row['id']
                        )
                        pets.append(pet)
                        logger.debug(f"Pet with id {pet.id} loaded from SQLite")

                    except Exception as e:
                        logger.error(f"Error creating pet object for id {row['id']}: {e}")
                        continue

                logger.info(f"Loaded {len(pets)} pets from SQLite")

        except sqlite3.Error as e:
            logger.error(f'Error loading pets from SQLite')

        return pets

    def load_appointments(self, pets_dict: dict) -> List[Appointment]:
        """Load all appointments from the database."""
        appointments = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, fecha, motivo, diagnostico, pet_id 
                    FROM appointments ORDER BY id
                ''')
                rows = cursor.fetchall()

                for row in rows:
                    try:
                        pet = pets_dict.get(row['pet_id'])
                        if pet is None:
                            logger.error(f"Pet with id {row['pet_id']} not found for appointment {row['id']}")
                            continue

                        appointment = Appointment(
                            row['fecha'],
                            row['motivo'],
                            row['diagnostico'],
                            pet,
                            row['id']
                        )
                        appointments.append(appointment)
                        logger.debug(f"Appointment with id {appointment.id} loaded from SQLite")

                    except Exception as e:
                        logger.error(f"Error creating appointment object for id {row['id']}: {e}")
                        continue

                logger.info(f"Loaded {len(appointments)} appointments from SQLite")

        except sqlite3.Error as e:
            logger.error(f"Error loading appointments: {e}")

        return appointments

    def get_database_info(self) -> dict:
        """Get basic information about the database."""
        info = {
            'owners_count': 0,
            'pets_count': 0,
            'appointments_count': 0
        }

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Count owners
                cursor.execute('SELECT COUNT(*) FROM owners')
                info['owners_count'] = cursor.fetchone()[0]

                # Count pets
                cursor.execute('SELECT COUNT(*) FROM pets')
                info['pets_count'] = cursor.fetchone()[0]

                # Count appointments
                cursor.execute('SELECT COUNT(*) FROM appointments')
                info['appointments_count'] = cursor.fetchone()[0]

        except sqlite3.Error as e:
            logger.error(f"Error getting database info: {e}")

        return info

    def clear_all_tables(self) -> bool:
        """Clear all data from all tables (useful for testing)."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM appointments')
                cursor.execute('DELETE FROM pets')
                cursor.execute('DELETE FROM owners')
                conn.commit()
                logger.info("All tables cleared")
                return True

        except sqlite3.Error as e:
            logger.error(f"Error clearing tables: {e}")
            return False

    def backup_to_json(self, backup_path: str = "Datos/sqlite_backup.json") -> bool:
        """Create a JSON backup of the entire database."""
        try:
            backup_data = {
                'owners': [],
                'pets': [],
                'appointments': [],
                'backup_timestamp': None
            }

            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Backup owners
                cursor.execute('SELECT * FROM owners')
                owners_rows = cursor.fetchall()
                for row in owners_rows:
                    backup_data['owners'].append(dict(row))

                # Backup pets
                cursor.execute('SELECT * FROM pets')
                pets_rows = cursor.fetchall()
                for row in pets_rows:
                    backup_data['pets'].append(dict(row))

                # Backup appointments
                cursor.execute('SELECT * FROM appointments')
                appointments_rows = cursor.fetchall()
                for row in appointments_rows:
                    backup_data['appointments'].append(dict(row))

                # Add timestamp
                cursor.execute('SELECT datetime("now")')
                backup_data['backup_timestamp'] = cursor.fetchone()[0]

            # Write to JSON file
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Database backed up to {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False