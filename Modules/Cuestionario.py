from Modules.base_de_datos import add_mascota, add_owners, buscar_mascota, add_consulta, buscar_owner
from Modules.Owner import Owner
from Modules.Mascota import Mascota
from Modules.Consulta import Consulta
from Modules.Verificaciones import verificar_fecha, verificar_numero

def registar_mascota():

    print('Ingrese el nombre de la mascota: ')
    nombre_mascota = input()
    print('Ingrese la fecha de nacimiento de la mascota en formatio dd/mm/yyyy: ')
    fecha_de_nacimiento = input()
    if not verificar_fecha(fecha_de_nacimiento):
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
            owner = buscar_owner(nombre, telefono)
            mascota = Mascota(nombre_mascota, especie, fecha_de_nacimiento, raza, owner)
            add_mascota(mascota)
        case "2":
            print('Ingrese el nombre del dueño de la mascota')
            nombre = input()
            print('Ingrese su numero telefonico')
            numero = input()
            if not verificar_numero(numero):
                raise ValueError('numero invalido')
            print('Ingrese su direccion')
            direccion = input()

            owner = Owner(nombre, numero, direccion)
            add_owners(owner)

            mascota = Mascota(nombre_mascota, especie, fecha_de_nacimiento, raza, owner)
            add_mascota(mascota)

def registar_consulta():
    print('Ingrese la fecha de la consulta')
    fecha = input()
    if not verificar_fecha(fecha):
        raise ValueError('Fecha invalida')
    print('Ingrese el motivo de la consulta')
    motivo = input()
    print('Ingrese el diagnostico de la mascota')
    diagnostico = input()
    print('Ingrese el nombre de la mascota')
    nombre_mascota = input()
    print('Ingrese el nombre de su dueño')
    nombre_owner = input()
    mascota = buscar_mascota(nombre_mascota, nombre_owner)
    if mascota is None:
        print("Mascota no encontrada")

    consulta = Consulta(fecha, motivo, diagnostico, mascota)
    add_consulta(consulta)