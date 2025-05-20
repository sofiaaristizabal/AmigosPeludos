from Modulos.pet import Pet
from Modulos.owner import Owner
from Modulos.appointment import Query
from logging_config import set_up_logger

general_logger = set_up_logger(__name__, file_name="run_time_logger.log")

_owners: list[Owner] = [
    Owner('Santiago Yepes', '3757353838', 'Siao Paulinho'),
    Owner('Sofia Aristizabal', '3454757474', 'Ilo durado'),
    Owner('Simon Gomez', '3758456363', 'Il Polles imeraldinha')
]

_pets: list[Pet] = [
    Pet('Lucas', 'French Poodle', '11/02/2013', 'French Poodle', _owners[0]),
    Pet('Ilo', 'Golden Retriever', '05/07/2018', 'Golden Retriever', _owners[1]),
    Pet('Pollo', 'Bulldog', '23/09/2020', 'Bulldog', _owners[2])
]

_queries: list[Query] = [
    Query('11/02/15', 'Vaccination', 'Teeth infection', _pets[2]),
    Query('12/03/16', 'General Checkup', 'Healthy', _pets[0]),
    Query('15/04/17', 'Deworming', 'Mild worms', _pets[1]),
    Query('20/05/18', 'Vaccination', 'Allergic reaction', _pets[2]),
    Query('22/06/19', 'Dental Cleaning', 'Tartar buildup', _pets[0]),
    Query('30/07/20', 'Surgery', 'Neutering', _pets[1]),
    Query('10/08/21', 'X-ray', 'Limping', _pets[2]),
    Query('14/09/22', 'Blood Test', 'Routine check', _pets[0]),
    Query('18/10/23', 'Vaccination', 'Healthy', _pets[1]),
    Query('25/11/24', 'General Checkup', 'Minor cold', _pets[2])
]


def add_pet(mascota):
    _pets.append(mascota)


def add_owner(owner):
    _owners.append(owner)


def add_query(queries):
    _queries.append(queries)


def find_pet(nombre_mascota, nombre_owner):
    for mascota in _pets:
        if nombre_mascota == mascota.nombre and nombre_owner == mascota.owner.nombre:
            return mascota

    return None

def find_owner(nombre_owner, telefono) -> Owner | None:
    for owner in _owners:
        if owner.nombre == nombre_owner and owner.telefono == telefono:
            return owner

    return None


def query_by_pet(nombre_mascota, nombre_owner):
    mascota = find_pet(nombre_mascota, nombre_owner)
    if not mascota:
        raise ValueError(f"Mascota con nombre '{nombre_mascota}' y dueno '{nombre_owner}' no encontrada")
    
    return [consulta for consulta in _queries if consulta.mascota == mascota]


def registered_pets():
    print('\n'.join(str(mascota) for mascota in _pets))

def get_all_pets():
    return _pets.copy()


    
    
