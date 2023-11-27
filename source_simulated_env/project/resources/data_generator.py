import csv
import json
import os
import random

from faker import Faker
from termcolor import colored

LANGUAGE = 'pt_BR'


def validate_quantity(quantity) -> int:
    """
    Checks whether the provided value is one of type ``int`` and greater
    than zero.
    """
    if not isinstance(quantity, int) or quantity < 1:
        message_error = colored(
            '✗ THE "quantity" PARAMETER MUST BE A POSITIVE INTEGER.'
            f'[** "{quantity}"({type(quantity)}):INVALID **]',
            'red',
        )
        raise ValueError(message_error)
    return quantity


def generator_driver_data(
    language: str = LANGUAGE,
    collection_name: str = 'DriverCollection',
    quantity: int = 1,
) -> dict[str, list[dict]]:
    """
    Generate driver data for a MongoDB collection.

    Args:
        - ``language (str, optional):`` The language to use for generating
        fake data. Default is 'LANGUAGE='pt_BR' (Brazilian Portuguese).
        - ``collection_name (str, optional):`` The name of the MongoDB
        collection where the driver data will be stored. Default is
        'DriverCollection'.
        - ``quantity (int, optional):`` The number of driver records to
        generate. Default is 1.

    Returns:
        ``dict:`` A dictionary containing the generated driver data. The keys
        of the dictionary correspond to the collection name, and the values
        are lists of driver records in the specified language.
    """
    quantity = validate_quantity(quantity)
    fake = Faker(language)
    drivers = []

    for _ in range(quantity):
        driver = {
            'name': fake.name(),
            'cnh_number': fake.ssn(),
            'address': fake.address(),
            'phone_number': fake.phone_number(),
            'e-mail': fake.ascii_free_email(),
        }
        drivers.append(driver)
    return {collection_name: drivers}


def generator_vehicle_data(
    language: str = LANGUAGE,
    collection_name: str = 'VehicleCollection',
    quantity: int = 1,
) -> dict[str, list[dict]]:
    """
    Generate driver data for a MongoDB collection.

    Args:
        - ``language (str, optional):`` The language to use for generating
        fake data. Default is 'LANGUAGE='pt_BR' (Brazilian Portuguese).
        - ``collection_name (str, optional):`` The name of the MongoDB
        collection where the driver data will be stored. Default is
        'VehicleCollection'.
        - ``quantity (int, optional):`` The number of driver records to
        generate. Default is 1.

    Returns:
        ``dict:`` A dictionary containing the generated driver data. The keys
        of the dictionary correspond to the collection name, and the values
        are lists of driver records in the specified language.
    """
    quantity = validate_quantity(quantity)
    fake = Faker(language)
    vehicles = []

    for _ in range(quantity):
        vehicle = {
            'name': random.choice(['Truck', 'Báu', 'Van', 'Mini-Cargo']),
            'vehicle_plate': fake.license_plate(),
            'dimensions': {
                'length': round(random.uniform(0.0, 5.0), 1),
                'width': round(random.uniform(0.0, 5.0), 1),
                'height': round(random.uniform(0.0, 5.0), 1),
            },
        }
        vehicles.append(vehicle)
    return {collection_name: vehicles}


def generator_client_data(
    language: str = LANGUAGE,
    collection_name: str = 'ClientCollection',
    quantity: int = 1,
) -> dict[str, list[dict]]:
    """
    Generate driver data for a MongoDB collection.

    Args:
        - ``language (str, optional):`` The language to use for generating
        fake data. Default is 'LANGUAGE='pt_BR' (Brazilian Portuguese).
        - ``collection_name (str, optional):`` The name of the MongoDB
        collection where the driver data will be stored. Default is
        'ClientCollection'.
        - ``quantity (int, optional):`` The number of driver records to
        generate. Default is 1.

    Returns:
        ``dict:`` A dictionary containing the generated driver data. The keys
        of the dictionary correspond to the collection name, and the values
        are lists of driver records in the specified language.
    """
    quantity = validate_quantity(quantity)
    fake = Faker(language)
    clients = []

    for _ in range(quantity):
        client = {
            'name': f'{fake.company()} {fake.company_suffix()}',
            'cnpj': fake.cnpj(),
            'address': fake.address(),
            'phone_number': fake.phone_number(),
            'e-mail': fake.ascii_free_email(),
        }
        clients.append(client)
    return {collection_name: clients}


def generator_location_data(
    language: str = LANGUAGE,
    collection_name: str = 'LocationCollection',
    quantity: int = 1,
) -> dict[str, list[dict]]:
    """
    Generate location data for a MongoDB collection.

    Args:
        - ``language (str, optional):`` The language to use for generating
        fake data. Default is 'LANGUAGE='pt_BR' (Brazilian Portuguese).
        - ``collection_name (str, optional):`` The name of the MongoDB
        collection where the location data will be stored. Default is
        'LocationCollection'.
        - ``quantity (int, optional):`` The number of location records to
        generate. Default is 1.

    Returns:
        ``dict:`` A dictionary containing the generated location data. The keys
        of the dictionary correspond to the collection name, and the values are
        lists of location records in the specified language.

    This function generates location data based on a local CSV file that
    contains municipality information. It randomly selects rows from the CSV
    file to create location records with city IDs, names, and coordinates
    (latitude and longitude).

    The `language` parameter allows you to specify the language for generating
    fake data.
    """
    quantity = validate_quantity(quantity)
    fake = Faker(language)
    locations = []

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '..', 'seed', 'municipios.csv')

    for _ in range(quantity):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            read = csv.reader(csvfile, delimiter=',')
            next(read)
            data = list(read)
            row = fake.random_element(data)
            city_id = row[0]
            city_name = row[1]
            latitude = row[2]
            longitude = row[3]
            location = {
                'city_id': city_id,
                'city_name': city_name,
                'coordinates': {'latitude': latitude, 'longitude': longitude},
            }
            locations.append(location)
    return {collection_name: locations}


def generator_product_data(
    language: str = LANGUAGE,
    collection_name: str = 'ProductCollection',
    quantity: int = 1,
) -> dict[str, list[dict]]:
    """
    Generate product data for a MongoDB collection.

    Args:
        - ``language (str, optional):`` The language to use for generating
        fake data. Default is 'LANGUAGE='pt_BR' (Brazilian Portuguese).
        - ``collection_name (str, optional):`` The name of the MongoDB
        collection where the product data will be stored. Default is
        'ProductCollection'.
        - ``quantity (int, optional):`` The number of product records to
        generate. Default is 1.

    Returns:
        ``dict:`` A dictionary containing the generated product data. The keys
        of the dictionary correspond to the collection name, and the values
        are lists of product records in the specified language.

    This function generates product data based on a local JSON file that
    contains product information. It randomly selects products from the JSON
    file to create product records with details such as name, price, and
    description.

    The `language` parameter allows you to specify the language for generating
    fake data
    """
    quantity = validate_quantity(quantity)
    fake = Faker(language)
    products = []

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '..', 'seed', 'products.json')

    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for _ in range(quantity):
            product = fake.random_element(data)
            products.append(product)
    return {collection_name: products}


def generator_delivery_data(
    language: str = LANGUAGE,
    collection_name: str = 'DeliveryCollection',
    quantity: int = 1,
) -> dict[str, list[dict]]:
    """
    Generate delivery data for a MongoDB collection.

    Args:
        - ``language (str, optional):`` The language to use for generating
        fake data. Default is 'LANGUAGE='pt_BR' (Brazilian Portuguese).
        - ``collection_name (str, optional):`` The name of the MongoDB
        collection where the delivery data will be stored. Default is
        'DeliveryCollection'.
        - ``quantity (int, optional):`` The number of delivery records to
        generate. Default is 1.

    Returns:
        ``dict:`` A dictionary containing the generated delivery data. The keys
        of the dictionary correspond to the collection name, and the values
        are lists of delivery records in the specified language.

    This function generates delivery data by combining various other functions
    to create a complete delivery record. It includes a driver, a vehicle, a
    client, origin and destination locations, and a product for each delivery.

    The `language` parameter allows you to specify the language for generating
    fake data.
    """
    quantity = validate_quantity(quantity)
    fake = Faker(language)
    deliveries: list[dict] = []
    products: list[dict] = []

    for _ in range(quantity):
        driver = generator_driver_data()['DriverCollection'][0]
        vehicle = generator_vehicle_data()['VehicleCollection'][0]
        client = generator_client_data()['ClientCollection'][0]
        location_origin = generator_location_data()['LocationCollection'][0]
        location_destination = None

        while (
            location_destination is None
            or location_destination == location_origin
        ):
            location_destination = generator_location_data()[
                'LocationCollection'
            ][0]

        for _ in range(random.randint(1, 5)):
            product = generator_product_data()['ProductCollection'][0]
            products.append(product)

        delivery = {
            'driver': driver,
            'vehicle': vehicle,
            'client': client,
            'data_delivery': {
                'data_start': fake.date_time_this_month(
                    before_now=False, after_now=True
                ).isoformat(),
                'origin': location_origin,
                'destination': location_destination,
                'products': products,
            },
        }
        deliveries.append(delivery)
    return {collection_name: deliveries}
