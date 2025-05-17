from Pet import Pet
from Owner import Owner

mascotas = []
owners = []
consultas = []

_owners: list[Owner] = [
    Owner('Santiago Yepes', '3757353838', 'Siao Paulinho'),
    Owner('Sofia Aristizabal', '3454757474', 'Ilo durado'),
    Owner('Simon Gomez', '3758456363', 'Il Polles imeraldinha')
]

_pets: list[Pet] = [
    Pet('Lucas', 'French Poodle', '11/02/2013', 'French Poodle', 'elvio') # Colocar owner name
]


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
