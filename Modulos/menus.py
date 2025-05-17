from Modulos.clean_terminal import limpiar_terminal
import Modulos.base_de_datos
import pyfiglet
from rich.table import Table
import typer
from rich.console import Console

def list_all_pets():
    limpiar_terminal()

    print("=" * 100)
    print(pyfiglet.figlet_format("Listado de Mascotas"))
    print("=" * 100)

    pets_table = Table("Nombre", "Especie", "Fecha de nacimiento", "Raza", "Dueño")
    for pet in Modulos.base_de_datos.get_all_pets():
        pets_table.add_row(pet.nombre, pet.especie, pet.fecha_de_nacimiento, pet.raza, pet.owner.nombre)
    
    console = Console()
    console.print(pets_table)

    typer.prompt("Escriba cualquier cosa para volver al menu principal")