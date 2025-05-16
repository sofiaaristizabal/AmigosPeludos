from Modules.Cuestionario import registar_mascota, registar_consulta
from Modules.base_de_datos import mascotas_registradas, consulta_por_mascota


while True:

    Menu = ("Ingrese el numero de la opcion el numero opcion que desea realizar \n"
            "1.Registrar mascota. \n"
            "2. Registrar consulta. \n"
            "3. Listar mascotas. \n"
            "4. Ver historial de consultas de una mascota específica. \n"
            "5. Salir de la aplicación.")

    print(Menu)
    user_input = input('Numero: ')

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
            break

