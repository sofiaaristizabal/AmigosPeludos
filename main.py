from Modulos.registrations import registar_mascota, registar_consulta
from Modulos.base_de_datos import registered_pets, query_by_pet
from Modulos.clean_terminal import limpiar_terminal
from Modulos.checker import check_valid_option
from Modulos.menus import list_all_pets
import pyfiglet
import typer
from rich import print
from rich.table import Table


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

            # user_input = input('Numero: ') 
            user_input = typer.prompt("Seleccione una opción [1-5]")
            user_input = check_valid_option(user_input, 1, 5)

            while not user_input:
                print("La Opción seleccionada no es valida, vuelve a intentar")
                user_input = typer.prompt("Seleccione una opcion [1-5]")

            match user_input:
                case 1:
                    registar_mascota()
                    print(registered_pets())
                case 2:
                    registar_consulta()
                case 3:
                    list_all_pets()
                case 4:
                    print('Ingrese el nombre de la mascota')
                    nombre_mascota = input()
                    print('Ingrese el nombre del dueño')
                    nombre_owner = input()
                    query_by_pet(nombre_mascota, nombre_owner)

                case 5:
                    if typer.confirm("¿Está seguro de que desea salir?"):
                        raise typer.Exit(code = 1)
    except typer.Exit as e:
        print(f"[bold green]Salida exitosa[/bold green]")


if __name__ == "__main__":
    typer.run(main)