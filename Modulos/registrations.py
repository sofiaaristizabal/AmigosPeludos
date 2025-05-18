from Modulos.owner import Owner
from Modulos.pet import Pet
from Modulos.appointment import Query
from Modulos.checker import verify_date, verify_number
from Modulos.base_de_datos import add_pet, add_owner, find_pet, add_query, find_owner
from Modulos.checker import check_valid_option
import typer


def registar_mascota():

    nombre_mascota = typer.prompt('Ingrese el nombre de la mascota')

    fecha_de_nacimiento = typer.prompt('Ingrese la fecha de nacimiento de la mascota en formatio dd/mm/yyyy')
    if not verify_date(fecha_de_nacimiento):
        raise ValueError("fecha invalida")
    
    especie = typer.prompt('Ingrese la especie de la mascota')
    raza = typer.prompt('Ingrese la raza de la mascota')

    user_input = typer.prompt('Si el dueño ya esta registrado previamente presione 1, si el dueño aun no esta registrado presione 2')
    

    while not (selected_option := check_valid_option(user_input, 1, 5)):
        print('La opcion seleccionada no es valida')
        user_input = typer.prompt('Si el dueño ya esta registrado previamente presione 1, si el dueño aun no esta registrado presione 2')

    match selected_option:
        case "1":
            nombre = typer.prompt('Ingrese el nombre del dueño de la mascota')
            telefono = typer.prompt('Ingrese el numero de telefono del dueño de la mascota')
            owner = find_owner(nombre, telefono)

            if owner is None:
                print("Dueño no encontrado. No se pudo registrar la mascota.")
                return
            
            mascota = Pet(nombre_mascota, especie, fecha_de_nacimiento, raza, owner)
            add_pet(mascota)

        case "2":
            nombre = typer.prompt('Ingrese el nombre del dueño de la mascota')
            numero = typer.prompt('Ingrese el numero telefonico del dueño de la mascota ')
            if not verify_number(numero):
                raise ValueError('numero invalido')
            
            direccion = typer.prompt('Ingrese la direccion del dueño de la mascota')

            owner = Owner(nombre, numero, direccion)
            add_owner(owner)

            mascota = Pet(nombre_mascota, especie, fecha_de_nacimiento, raza, owner)
            add_pet(mascota)


def registar_consulta():
    fecha = typer.prompt('Ingrese la fecha de la consulta')
    if not verify_date(fecha):
        raise ValueError('Fecha invalida')
    
    motivo = typer.prompt('Ingrese el motivo de la consulta')
    diagnostico = typer.prompt('Ingrese el diagnostico de la mascota')
    nombre_mascota = typer.prompt('Ingrese el nombre de la mascota')
    nombre_owner = typer.prompt('Ingrese el nombre de su dueño')

    mascota = find_pet(nombre_mascota, nombre_owner)
    if mascota is None:
        print("Mascota no encontrada")
        return

    consulta = Query(fecha, motivo, diagnostico, mascota)
    add_query(consulta)