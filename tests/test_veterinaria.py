import unittest
import os
import json
import csv
import tempfile
import logging
from datetime import datetime
import Modulos.file_manager as file_manager_module
from Modulos.pet import Pet
from Modulos.owner import Owner
from Modulos.appointment import Appointment
from Modulos.validator import verify_date, verify_number, check_valid_option
from Modulos.base_de_datos import Data_Base
from Modulos.file_manager import File_Manager
from logging_config import set_up_logger
from Modulos.Custom_Exceptions.owner_not_found_error import Owner_Not_Found_Error
from Modulos.Custom_Exceptions.pet_not_found_error import Pet_Not_Found_Error

# Test Pet
class TestPet(unittest.TestCase):
    """Validate Creation, attributes, age and comparing from Pet"""

    def setUp(self):
        self.owner = Owner("Sofía", "3008123455", "Calle Bochornaise", id=1)
        self.pet = Pet("Dulce", "Perro", "01/01/2020", "Pekines", self.owner, id=42)

    def test_attributes(self):
        """Prove attributes are correctly assigned"""
        self.assertEqual(self.pet.nombre, "Dulce")
        self.assertEqual(self.pet.especie, "Perro")
        self.assertEqual(self.pet.raza, "Pekines")
        self.assertEqual(self.pet.owner, self.owner)
        self.assertEqual(self.pet.id, 42)
    
    def test_age(self):
        """Prove age property calculation"""
        today = datetime.now().date()
        birth = datetime.strptime(self.pet.fecha_de_nacimiento, "%d/%m/%Y").date()
        expected_age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        self.assertEqual(self.pet.age, expected_age)

    def test_eq_true(self):
        """Two pets with equal data must be the same"""
        other = Pet("Dulce", "Perro", "01/01/2020", "Pekines", self.owner, id=99)
        self.assertTrue(self.pet == other)

    def test_eq_false(self):
        """Las mascotas con nombres diferentes NO deben considerarse iguales."""
        other = Pet("Luna", "Perro", "01/01/2020", "Pekines", self.owner, id=42)
        self.assertFalse(self.pet == other)
        
# Test Owner
class TestOwner(unittest.TestCase):
    """Attributes and Serialization"""

    def setUp(self):
        self.owner = Owner("Luis", "3245657474", "Av Otraparte", id=2)

    def test_str(self):
        """Comprueba __str__ incluye nombre, teléfono y dirección."""
        s = str(self.owner)
        self.assertIn("Luis", s)
        self.assertIn("3245657474", s)
        self.assertIn("Av Otraparte", s)

    def test_to_dict(self):
        """Verify dict of serialization"""
        d = self.owner.to_dict()
        self.assertEqual(d["nombre"], "Luis")
        self.assertEqual(d["id"], 2)

# Test Appointment
class TestAppointment(unittest.TestCase):
    """Creation and to_dict"""
    
    def setUp(self):
        owner = Owner("Santiago", "3007654747", "Calle 78", id=3)
        pet = Pet("Copito", "Perro", "15/03/2019", "Pomeranian", owner, id=7)
        self.app = Appointment("15/05/2025", "Vacunación", "OK", pet, id=100)
    
    def test_attributes(self):
        """Prove basic attributes of an Appointment"""
        self.assertEqual(self.app.motivo, "Vacunación")
        self.assertEqual(self.app.mascota.nombre, "Copito")

    def test_to_dict(self):
        """Verify dict for JSON"""
        d = self.app.to_dict()
        self.assertEqual(d["id"], 100)
        self.assertEqual(d["id_mascota"], 7)

# Validators and options management
class TestValidator(unittest.TestCase):
    """Try verify_number, verify_date and check_valid_option"""

    def test_verify_number_valid(self):
        self.assertTrue(verify_number("+573008152042"))
        self.assertTrue(verify_number("12345678901"))
        self.assertTrue(verify_number("3208654747"))
    
    def test_verify_number_invalid(self):
        self.assertFalse(verify_number("abc"))
    
    def test_verify_date_valid(self):
        self.assertTrue(verify_date("31/12/2024"))

    def test_verify_date_invalid(self):
        self.assertFalse(verify_date("31-12-2024"))
    
    def test_check_valid_option(self):
        self.assertEqual(check_valid_option("3", 1, 5), 3)
        self.assertFalse(check_valid_option("x", 1, 5))
        self.assertFalse(check_valid_option("6", 1, 5))

# Prove Data_Base in memory
class TestDataBase(unittest.TestCase):
    """Tests: 1) Add, 2) Query, 3) Exceptions"""
    def setUp(self):
        self.db = Data_Base()
    
    def test_owner_add_find(self):
        owner = Owner("Juliana", "3007653424", "Calle X", id=1)
        self.db.add_owner(owner)
        found = self.db.find_owner("Juliana", "3007653424")
        self.assertIsNotNone(found)
        with self.assertRaises(Owner_Not_Found_Error):
            self.db.find_owner_by_id(999)
    
    def test_pet_add_find_and_next_id(self):
        owner = Owner("Luciana", "3000001111", "Calle 81", id=2)
        self.db.add_owner(owner)
        pet = Pet("Toby", "Perro", "10/10/2020", "Labrador", owner, id=5)
        self.db.add_pet(pet)
        self.assertEqual(self.db.find_pet("Toby", "Luciana"), pet)
        self.assertEqual(self.db.get_next_pet_id(), 6)

    def test_query_by_pet_no_exist(self):
        with self.assertRaises(ValueError):
            self.db.query_by_pet("NoExiste", "NadieExiste")

    def test_find_pet_by_id_error(self):
        """find_pet_by_id con id inexistente lanza Pet_Not_Found_Error"""
        with self.assertRaises(Pet_Not_Found_Error):
            self.db.find_pet_by_id(999)

# Try Serialization and Deserialization (CSV/JSON)
class TestFileManager(unittest.TestCase):
    """Tests on saving and loading for File_Manager using tempfiles"""

    def setUp(self):
        self.db = Data_Base()
        o = Owner("Test", "+570000000000", "Dir", id=1)
        p = Pet("Adi", "Gato", "01/02/2021", "Mestizo", o, id=1)
        a = Appointment("02/03/2022", "Chequeo", "Bien", p, id=1)
        self.db.add_owner(o); self.db.add_pet(p); self.db.add_query(a)

        self.tempdir = tempfile.TemporaryDirectory()
        self.base = self.tempdir.name
        os.makedirs(os.path.join(self.base, "Datos", "appointments"))

    def tearDown(self):
        self.tempdir.cleanup()
    
    def test_save_and_load_csv_json(self):
        File_Manager._save_owners(self.db.get_owners(), path=os.path.join(self.base, "Datos"))
        File_Manager._save_pets(self.db.get_pets(), path=os.path.join(self.base, "Datos"))
        File_Manager._save_appointments(self.db.get_appointments(), path=os.path.join(self.base, "Datos"))

        db2 = Data_Base()
        File_Manager._load_owners(db2, path=os.path.join(self.base, "Datos"))
        File_Manager._load_pets(db2, path=os.path.join(self.base, "Datos"))
        File_Manager._load_appointments(db2, path=os.path.join(self.base, "Datos"))

        self.assertEqual(len(db2.get_owners()), 1)
        self.assertEqual(len(db2.get_pets()), 1)
        self.assertEqual(len(db2.get_appointments()), 1)

    def test_load_pets_file_not_found_logs_error(self):
        """Si la ruta de pets no existe, loguea FileNotFoundError"""
        log_path = os.path.join(self.base, "fm.log")
        temp_logger = logging.getLogger("fm_test")
        for h in temp_logger.handlers: temp_logger.removeHandler(h)
        fh = logging.FileHandler(log_path, mode="w")
        temp_logger.addHandler(fh)
        file_manager_module.logger = temp_logger
        File_Manager._load_pets(self.db, path=os.path.join(self.base, "NoExiste"))
        fh.flush()
        with open(log_path, 'r') as f:
            content = f.read()
        self.assertIn("couldn't be found", content)
        temp_logger.removeHandler(fh)
        fh.close()

    def test_save_pets_file_not_found_logs_error(self):
        """Si la ruta de pets no existe, loguea FileNotFoundError en save"""
        log_path = os.path.join(self.base, "fm_save.log")
        temp_logger = logging.getLogger("fm_save_test")
        for h in temp_logger.handlers: temp_logger.removeHandler(h)
        fh = logging.FileHandler(log_path, mode="w")
        temp_logger.addHandler(fh)
        file_manager_module.logger = temp_logger
        File_Manager._save_pets(self.db.get_pets(), path=os.path.join(self.base, "NoExiste"))
        fh.flush()
        with open(log_path, 'r') as f:
            content = f.read()
        self.assertIn("couldn't be found", content)
        temp_logger.removeHandler(fh)
        fh.close()

# Test logging_config file writing
class TestLoggingConfig(unittest.TestCase):
    """Pruebas de set_up_logger: escritura en handler adicional"""

    def test_logging_writes_to_extra_handler(self):
        os.environ["LOGGING_LEVEL"] = "INFO"
        tmp = tempfile.TemporaryDirectory()
        log_path = os.path.join(tmp.name, "test.log")
        fh = logging.FileHandler(log_path, mode="w")
        logger = set_up_logger("testwrite", fh, file_name="unused.log")
        logger.info("MensajeDePrueba")
        fh.flush()
        with open(log_path, 'r') as f:
            content = f.read()
        self.assertIn("MensajeDePrueba", content)
        logger.removeHandler(fh)
        fh.close()
        tmp.cleanup()

if __name__ == '__main__':
    unittest.main()
