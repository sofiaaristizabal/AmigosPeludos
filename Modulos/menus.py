from Modulos.clean_terminal import limpiar_terminal
import Modulos.base_de_datos
import pyfiglet
from rich.table import Table
import typer
from rich.console import Console
from Modulos.Owner import Owner
from Modulos.Pet import Pet
from Modulos.appointment import Query
from Modulos.checker import verify_date, verify_number
from Modulos.base_de_datos import add_pet, add_owner, find_pet, add_query, find_owner, query_by_pet
from Modulos.checker import check_valid_option
from rich import print
import time


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


def registrar_dueno() -> Owner:
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
        raise ValueError('Número invalido')
    
    direccion = typer.prompt('\nIngrese la direccion del dueño de la mascota')

    print("Asi quedó la informacion del dueno:")
    tabla_dueno.add_row(nombre, numero, direccion)
    print(tabla_dueno)

    owner = Owner(nombre, numero, direccion)
    add_owner(owner)
    return owner


def registar_mascota():
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
            owner = find_owner(nombre, telefono)

            if owner is None:
                print("Dueño no encontrado. No se pudo registrar la mascota.")
                return

        case 2:
            print("\n" * 2)
            owner = registrar_dueno()
            print("\n" * 2)

    tabla_mascota.add_row(nombre_mascota, fecha_de_nacimiento, especie, raza, owner.nombre)
    print()
    print("=" * 100)
    print("Asi quedó la mascota a ingresar")
    print(tabla_mascota)
    
    if not typer.confirm("\nEsta seguro de ingresar la mascota?"):
        print("[/bold red]No se realizo el registro de la mascota[/bold red]")
        return
    
    mascota = Pet(nombre_mascota, especie, fecha_de_nacimiento, raza, owner)
    add_pet(mascota)
    print("[bold green]Se realizo exitosamente el registro de la mascota[/bold green]")
    time.sleep(2)


def registar_consulta():
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
    
    mascota = find_pet(nombre_mascota, nombre_owner)
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

    consulta = Query(fecha, motivo, diagnostico, mascota)
    add_query(consulta)
    print("[bold green]Se realizo exitosamente el registro de la consulta[/bold green]")
    time.sleep(2)


def pets_appointments():
    limpiar_terminal()

    print("=" * 100)
    print(pyfiglet.figlet_format("Registro de consulta"))
    print("=" * 100)

    nombre_mascota = typer.prompt("\nIngrese el nombre de la mascota")
    nombre_owner = typer.prompt("\nIngrese el nombre del dueño")

    tabla_consulta = Table("Mascota", "Nombre Dueno", "Fecha", "Motivo", "Diagnostico")
    for consulta in query_by_pet(nombre_mascota, nombre_owner):
        tabla_consulta.add_row(consulta.mascota.nombre, consulta.mascota.owner.nombre, consulta.fecha, consulta.motivo, consulta.diagnostico)

    print("\n")
    print(tabla_consulta)
    typer.prompt("Escriba cualquier cosa para volver al menu principal")
