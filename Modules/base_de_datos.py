
mascotas = []
owners = []
consultas = []


def add_pet(mascota):
    mascotas.append(mascota)


def add_owner(owners):
    owners.append(owners)


def add_query(queries):
    queries.append(queries)


def find_pet(nombre_mascota, nombre_owner):
    for mascota in mascotas:
        if nombre_mascota == mascota.nombre and nombre_owner == mascota.owner.nombre:
            return mascota

    return None

def find_owner(nombre_owner, telefono):
    for owner in owners:
        if owner.nombre == nombre_owner and owner.telefono == telefono:
            return owner

    return None


def query_by_pet(nombre_mascota, nombre_owner):
    mascota = find_pet(nombre_mascota, nombre_owner)
    consultasM = []
    for consulta in consultas:
        if consulta.mascota == mascota:
            consultasM.append(consulta)

    print('\n'.join(str(consulta) for consulta in consultasM))


def registered_pets():
    print('\n'.join(str(mascota) for mascota in mascotas))
