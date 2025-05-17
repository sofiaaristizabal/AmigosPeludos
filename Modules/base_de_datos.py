
mascotas = []
owners = []
consultas = []


def add_mascota(mascota):
    mascotas.append(mascota)


def add_owners(owner):
    owners.append(owner)


def add_consulta(consulta):
    consultas.append(consulta)


def buscar_mascota(nombre_mascota, nombre_owner):
    for mascota in mascotas:
        if nombre_mascota == mascota.nombre and nombre_owner == mascota.owner.nombre:
            return mascota

    return None

def buscar_owner(nombre_owner, telefono):
    for owner in owners:
        if owner.nombre == nombre_owner and owner.telefono == telefono:
            return owner

    return None


def consulta_por_mascota(nombre_mascota, nombre_owner):
    mascota = buscar_mascota(nombre_mascota, nombre_owner)
    consultasM = []
    for consulta in consultas:
        if consulta.mascota == mascota:
            consultasM.append(consulta)

    print('\n'.join(str(consulta) for consulta in consultasM))


def mascotas_registradas():
    print('\n'.join(str(mascota) for mascota in mascotas))
