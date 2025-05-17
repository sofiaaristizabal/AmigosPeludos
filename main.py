from Modules.Cuestionario import registar_mascota, registar_consulta
from Modules.base_de_datos import mascotas_registradas, consulta_por_mascota
from Modules.clean_terminal import limpiar_terminal
import pyfiglet
import typer
from rich import print
from rich.table import Table
import cowsay


while True:
    limpiar_terminal()
    print("==" * 100)
    print(pyfiglet.figlet_format("MENU PRINCIPAL"))
    print("==" * 100)

    table = Table("Comando", "Descripción")
    table.add_row("1", "Registrar mascota")
    table.add_row("2", "Registrar consulta")
    table.add_row("3", "Listar mascotas")
    table.add_row("4", "Ver historial de consultas de una mascota específica")
    table.add_row("5", "Salir de la aplicación")

    print(table)
    print("==" * 100)

    # user_input = input('Numero: ') 
    user_input = typer.prompt("Seleccione una opción [1-5]")

    match user_input:
        case "1":
            registar_mascota()
            print(mascotas_registradas())
        case "2":
            registar_consulta()
        case "3":
            mascotas_registradas()
        case "4":
            print('Ingrese el nombre de la mascota')
            nombre_mascota = input()
            print('Ingrese el nombre del dueño')
            nombre_owner = input()
            consulta_por_mascota(nombre_mascota, nombre_owner)

        case "5":
            if typer.confirm("¿Está seguro de que desea salir?"):
                typer.Exit(code = 1)

