from Modulos.owner import Owner
from Modulos.pet import Pet
from Modulos.appointment import Query
from Modulos.checker import verify_date, verify_number
from Modulos.base_de_datos import add_pet, add_owner, find_pet, add_query, find_owner


def registar_mascota():

    print('Ingrese el nombre de la mascota: ')
    nombre_mascota = input()
    print('Ingrese la fecha de nacimiento de la mascota en formatio dd/mm/yyyy: ')
    fecha_de_nacimiento = input()
    if not verify_date(fecha_de_nacimiento):
        raise ValueError("fecha invalida")
    print('Ingrese la especie de la mascota: ')
    especie = input()
    print('Ingrese la raza de la mascota: ')
    raza = input()

    print('Si el dueño ya esta registrado con otra mascota presione 1, si el dueño aun no esta registrado presione 2: ')
    user_input = input()

    match user_input:
        case "1":
            print('Ingrese el nombre del dueño de la mascota: ')
            nombre = input()
            print('Ingrese el numero de telefono del dueño de la mascota: ')
            telefono = input()
            owner = find_owner(nombre, telefono)

            if owner is None:
                print("Dueño no encontrado. No se puede registrar la mascota.")
                return
            
            mascota = Pet(nombre_mascota, especie, fecha_de_nacimiento, raza, owner)
            add_pet(mascota)
        case "2":
            print('Ingrese el nombre del dueño de la mascota')
            nombre = input()
            print('Ingrese su numero telefonico')
            numero = input()
            if not verify_number(numero):
                raise ValueError('numero invalido')
            print('Ingrese su direccion')
            direccion = input()

            owner = Owner(nombre, numero, direccion)
            add_owner(owner)

            mascota = Pet(nombre_mascota, especie, fecha_de_nacimiento, raza, owner)
            add_pet(mascota)

def registar_consulta():
    print('Ingrese la fecha de la consulta')
    fecha = input()
    if not verify_date(fecha):
        raise ValueError('Fecha invalida')
    print('Ingrese el motivo de la consulta')
    motivo = input()
    print('Ingrese el diagnostico de la mascota')
    diagnostico = input()
    print('Ingrese el nombre de la mascota')
    nombre_mascota = input()
    print('Ingrese el nombre de su dueño')
    nombre_owner = input()
    mascota = find_pet(nombre_mascota, nombre_owner)
    if mascota is None:
        print("Mascota no encontrada")

    consulta = Query(fecha, motivo, diagnostico, mascota)
    add_query(consulta)