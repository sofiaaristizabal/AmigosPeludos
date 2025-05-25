from Modulos.clean_terminal import limpiar_terminal
import pyfiglet
from rich.table import Table
import typer
from rich.console import Console
from Modulos.owner import Owner
from Modulos.pet import Pet
from Modulos.appointment import Appointment
from Modulos.checker import verify_date, verify_number
from Modulos.base_de_datos import Data_Base
from Modulos.checker import check_valid_option
from rich import print
import time
from logging_config import set_up_logger
from Modulos.file_manager import File_Manager

menus_time_logger = set_up_logger("time_spent_logger", file_name="menus_time_spent.log")
general_logger = set_up_logger(__name__, file_name="run_time_logger.log")

class Menus():
    def __init__(self):
        self.database = Data_Base()
        File_Manager.load_database(self.database)  # Load the database at the start

    def execute_function(self,function):
        try:
            function()
        except ValueError as e:
            print(f"[bold red]\nSe ha producido un error: {e}[/bold red]")
            print("Por favor vuelvalo a intentar")
            time.sleep(2)
            general_logger.error(e)
        

    def main_menu(self,):
        start_time = time.perf_counter()
        limpiar_terminal()
        print("=" * 100)
        print(pyfiglet.figlet_format("MENU PRINCIPAL"))
        print("=" * 100)

        table = Table("Comando", "Descripción")
        table.add_row("1", "Registrar mascota")
        table.add_row("2", "Registrar consulta")
        table.add_row("3", "Listar mascotas")
        table.add_row("4", "Ver historial de consultas de una mascota específica")
        table.add_row("5", "Guardar los datos")
        table.add_row("6", "Salir de la aplicación")

        print(table)
        print("=" * 100)

        user_input = typer.prompt("Seleccione una opción [1-6]")

        while not (selected_option := check_valid_option(user_input, 1, 6)):
            print("\nLa opción seleccionada no es valida, vuelve a intentar")
            general_logger.warning("User selected a wrong option")
            user_input = typer.prompt("Seleccione una opcion [1-5]")

        menus_time_logger.info(f"time spent in main_menu: {format(time.perf_counter() - start_time, '.3f')}")
        match selected_option:
            case 1:
                self.execute_function(self.registar_mascota)
                
            case 2:
                self.execute_function(self.registar_consulta)
                
            case 3:
                self.execute_function(self.list_all_pets)
                
            case 4:
                self.execute_function(self.pets_appointments)

            case 5:
                print("[bold]Guardando base de datos[/bold]")
                File_Manager.save_database(self.database)
                print("[bold green]La base de datos fue exitosamente guardada[/bold green]")
                time.sleep(1.3)

            case 6:
                if typer.confirm("¿Está seguro de que desea salir?"):
                    File_Manager.save_database(self.database)  # Always save the database at the end
                    raise typer.Exit(code = 1)
        

    def list_all_pets(self,):
        start_time = time.perf_counter()
        limpiar_terminal()

        print("=" * 100)
        print(pyfiglet.figlet_format("Listado de Mascotas"))
        print("=" * 100)

        pets_table = Table("Nombre", "Especie", "Fecha de nacimiento", "Raza", "Dueño")
        for pet in self.database.get_pets():
            pets_table.add_row(pet.nombre, pet.especie, pet.fecha_de_nacimiento, pet.raza, pet.owner.nombre)
        
        console = Console()
        console.print(pets_table)

        menus_time_logger.info(f"time spent in list_all_pets: {format(time.perf_counter() - start_time, '.3f')}")
        typer.prompt("Escriba cualquier cosa para volver al menu principal")


    def registrar_dueno(self,) -> Owner:
        start_time = time.perf_counter()
        print("=" * 100)
        print(pyfiglet.figlet_format("Registro de dueno"))
        print("=" * 100)

        print("Recuerde que la informacion de los dueños tiene la siguiente estructura: ")
        tabla_dueno = Table("Nombre", "Telefono", "Direccion")
        print(tabla_dueno)
        print("=" * 100)

        nombre = typer.prompt('\nIngrese el nombre del dueño de la mascota')
        numero = typer.prompt('\nIngrese el numero telefonico del dueño de la mascota')
        if not verify_number(numero):
            raise ValueError('Número de celular invalido')
        
        direccion = typer.prompt('\nIngrese la direccion del dueño de la mascota')

        print("Asi quedó la informacion del dueno:")
        tabla_dueno.add_row(nombre, numero, direccion)
        print(tabla_dueno)

        owner = Owner(nombre, numero, direccion, self.database.get_next_owner_id())
        self.database.add_owner(owner)
        general_logger.info(f"An owner has been registered: {owner}")
        menus_time_logger.info(f"time spent in registrar_dueno: {format(time.perf_counter() - start_time, '.3f')}")
        return owner


    def registar_mascota(self,):
        start_time = time.perf_counter()
        limpiar_terminal()

        print("=" * 100)
        print(pyfiglet.figlet_format("Registro de mascotas"))
        print("=" * 100)

        print("Recuerde que la informacion de las mascotas tiene la siguiente estructura: ")
        tabla_mascota = Table("Nombre", "Fecha de nacimiento", "Especie", "Raza", "Dueño")
        print(tabla_mascota)
        print("=" * 100)

        nombre_mascota = typer.prompt('\nIngrese el nombre de la mascota')

        fecha_de_nacimiento = typer.prompt('\nIngrese la fecha de nacimiento de la mascota en formatio dd/mm/yyyy')
        if not verify_date(fecha_de_nacimiento):
            raise ValueError("Fecha invalida")
        
        especie = typer.prompt('\nIngrese la especie de la mascota')
        raza = typer.prompt('\nIngrese la raza de la mascota')

        user_input = typer.prompt('\nSi el dueño ya esta registrado previamente presione 1, si el dueño aún no esta registrado presione 2')
        
        while not (selected_option := check_valid_option(user_input, 1, 2)):
            print('La opcion seleccionada no es valida')
            user_input = typer.prompt('\nSi el dueño ya esta registrado previamente presione 1, si el dueño aun no esta registrado presione 2')

        match selected_option:
            case 1:
                nombre = typer.prompt('\nIngrese el nombre del dueño de la mascota')
                telefono = typer.prompt('\nIngrese el numero de telefono del dueño de la mascota')
                owner = self.database.find_owner(nombre, telefono)

                if owner is None:
                    print("Dueño no encontrado. No se pudo registrar la mascota.")
                    return

            case 2:
                print("\n" * 2)
                owner = self.database.registrar_dueno()
                print("\n" * 2)

        tabla_mascota.add_row(nombre_mascota, fecha_de_nacimiento, especie, raza, owner.nombre)
        print()
        print("=" * 100)
        print("Asi quedó la mascota a ingresar")
        print(tabla_mascota)
        
        if not typer.confirm("\nEsta seguro de ingresar la mascota?"):
            print("[/bold red]No se realizo el registro de la mascota[/bold red]")
            return
        
        mascota = Pet(nombre_mascota, especie, fecha_de_nacimiento, 
                      raza, owner, self.database.get_next_pet_id())
        self.database.add_pet(mascota)
        general_logger.info(f"A mascot has been registered: {mascota}")
        print("[bold green]Se realizo exitosamente el registro de la mascota[/bold green]")
        time.sleep(2)
        menus_time_logger.info(f"time spent in registrar_mascota: {format(time.perf_counter() - start_time, '.3f')}")


    def registar_consulta(self,):
        start_time = time.perf_counter()
        limpiar_terminal()

        print("=" * 100)
        print(pyfiglet.figlet_format("Registro de consulta"))
        print("=" * 100)

        print("Recuerde que la informacion de las consultas tiene la siguiente estructura: ")
        tabla_consulta = Table("Mascota", "Fecha", "Motivo", "Diagnostico", "Nombre de la Mascota")
        print(tabla_consulta)
        print("=" * 100)

        nombre_mascota = typer.prompt('Ingrese el nombre de la mascota')
        nombre_owner = typer.prompt('Ingrese el nombre de su dueño')
        
        mascota = self.database.find_pet(nombre_mascota, nombre_owner)
        if mascota is None:
            print("Mascota no encontrada")
            return

        fecha = typer.prompt('Ingrese la fecha de la consulta (dd/mm/aaaa)')
        if not verify_date(fecha):
            raise ValueError('Fecha invalida')
        
        motivo = typer.prompt('Ingrese el motivo de la consulta')
        diagnostico = typer.prompt('Ingrese el diagnostico de la mascota')

        tabla_consulta = Table("Mascota", "Nombre Dueno", "Fecha", "Motivo", "Diagnostico")
        tabla_consulta.add_row(mascota.nombre, mascota.owner.nombre, fecha, motivo, diagnostico)

        print()
        print("=" * 100)
        print("Asi quedo la consulta a ingresar")
        print(tabla_consulta)
        
        if not typer.confirm("\nEsta seguro de ingresar la consulta?"):
            print("[/bold red]No se realizo el registro de la consulta[/bold red]")
            return

        consulta = Appointment(fecha, motivo, diagnostico, mascota, self.database.get_next_appointment_id())
        self.database.add_query(consulta)
        general_logger.info(f"An appointment has been registered {consulta}")
        print("[bold green]Se realizo exitosamente el registro de la consulta[/bold green]")
        time.sleep(2)
        menus_time_logger.info(f"time spent in registrar consulta: {format(time.perf_counter() - start_time, '.3f')}")


    def pets_appointments(self,):
        start_time = time.perf_counter()
        limpiar_terminal()

        print("=" * 100)
        print(pyfiglet.figlet_format("Registro de consulta"))
        print("=" * 100)

        nombre_mascota = typer.prompt("\nIngrese el nombre de la mascota")
        nombre_owner = typer.prompt("\nIngrese el nombre del dueño")

        tabla_consulta = Table("Mascota", "Nombre Dueno", "Fecha", "Motivo", "Diagnostico")
        appointments = self.database.query_by_pet(nombre_mascota, nombre_owner)

        if len(appointments) == 0:
            print("La mascota no tiene consultas registradas")
        else:
            for consulta in appointments:
                tabla_consulta.add_row(consulta.mascota.nombre, consulta.mascota.owner.nombre, consulta.fecha, consulta.motivo, consulta.diagnostico)

            print("\n")
            print(tabla_consulta)

        typer.prompt("Escriba cualquier cosa para volver al menu principal")
        menus_time_logger.info(f"time spent in pets_appointments: {format(time.perf_counter() - start_time, '.3f')}")
