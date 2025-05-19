from Modulos.base_de_datos import registered_pets, query_by_pet
from Modulos.clean_terminal import limpiar_terminal
from Modulos.checker import check_valid_option
import Modulos.menus as menus
import pyfiglet
import typer
from rich import print
from rich.table import Table
import time


def main():
    try:
        while True:
            limpiar_terminal()
            print("=" * 100)
            print(pyfiglet.figlet_format("MENU PRINCIPAL"))
            print("=" * 100)

            table = Table("Comando", "Descripción")
            table.add_row("1", "Registrar mascota")
            table.add_row("2", "Registrar consulta")
            table.add_row("3", "Listar mascotas")
            table.add_row("4", "Ver historial de consultas de una mascota específica")
            table.add_row("5", "Salir de la aplicación")

            print(table)
            print("=" * 100)

            user_input = typer.prompt("Seleccione una opción [1-5]")

            while not (selected_option := check_valid_option(user_input, 1, 5)):
                print("\nLa Opción seleccionada no es valida, vuelve a intentar")
                user_input = typer.prompt("Seleccione una opcion [1-5]")

            match selected_option:
                case 1:
                    try:
                        menus.registar_mascota()
                    except ValueError as e:
                        print(f"[bold red]\nSe ha producido un error: {e}[/bold red]")
                        print("Por favor vuelvalo a intentar")
                        time.sleep(2)
                case 2:
                    try:
                        menus.registar_consulta()
                    except ValueError as e:
                        print(f"[bold red]\nSe ha producido un error: {e}[/bold red]")
                        print("Por favor vuelvalo a intentar")
                        time.sleep(2)
                case 3:
                        menus.list_all_pets()
                    
                case 4:
                    try:
                        menus.pets_appointments()
                    except ValueError as e:
                        print(f"[bold red]\nSe ha producido un error: {e}[/bold red]")
                        print("Por favor vuelvalo a intentar")
                        time.sleep(2)

                case 5:
                    if typer.confirm("¿Está seguro de que desea salir?"):
                        raise typer.Exit(code = 1)
    except typer.Exit as e:
        print(f"[bold green]Salida exitosa[/bold green]")


if __name__ == "__main__":
    typer.run(main)