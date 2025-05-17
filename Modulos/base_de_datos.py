from Modulos.Pet import Pet
from Modulos.Owner import Owner
from Modulos.Query import Query


_owners: list[Owner] = [
    Owner('Santiago Yepes', '3757353838', 'Siao Paulinho'),
    Owner('Sofia Aristizabal', '3454757474', 'Ilo durado'),
    Owner('Simon Gomez', '3758456363', 'Il Polles imeraldinha')
]

_pets: list[Pet] = [
    Pet('Lucas', 'French Poodle', '11/02/2013', 'French Poodle', 'Santiago Yepes'),
    Pet('Ilo', 'Golden Retriever', '05/07/2018', 'Golden Retriever', 'Sofia Aristizabal'),
    Pet('Pollo', 'Bulldog', '23/09/2020', 'Bulldog', 'Simon Gomez')
]

_queries: list[Query] = [
    Query('11/02/15', 'Vaccination', 'Teeth infection', 'Pollo'),
    Query('12/03/16', 'General Checkup', 'Healthy', 'Lucas'),
    Query('15/04/17', 'Deworming', 'Mild worms', 'Ilo'),
    Query('20/05/18', 'Vaccination', 'Allergic reaction', 'Pollo'),
    Query('22/06/19', 'Dental Cleaning', 'Tartar buildup', 'Lucas'),
    Query('30/07/20', 'Surgery', 'Neutering', 'Ilo'),
    Query('10/08/21', 'X-ray', 'Limping', 'Pollo'),
    Query('14/09/22', 'Blood Test', 'Routine check', 'Lucas'),
    Query('18/10/23', 'Vaccination', 'Healthy', 'Ilo'),
    Query('25/11/24', 'General Checkup', 'Minor cold', 'Pollo')
]


def add_pet(mascota):
    _pets.append(mascota)


def add_owner(owner):
    _owners.append(owner)


def add_query(queries):
    queries.append(queries)


def find_pet(nombre_mascota, nombre_owner):
    for mascota in _pets:
        if nombre_mascota == mascota.nombre and nombre_owner == mascota.owner.nombre:
            return mascota

    return None

def find_owner(nombre_owner, telefono):
    for owner in _owners:
        if owner.nombre == nombre_owner and owner.telefono == telefono:
            return owner

    return None


def query_by_pet(nombre_mascota, nombre_owner):
    mascota = find_pet(nombre_mascota, nombre_owner)
    consultasM = []
    for consulta in _queries:
        if consulta.mascota == mascota:
            consultasM.append(consulta)

    print('\n'.join(str(consulta) for consulta in consultasM))


def registered_pets():
    print('\n'.join(str(mascota) for mascota in _pets))
