import random
import time
from collections.abc import Callable

from actions_db import MongoDBActions

from project.config import setup_custom_logger


def simulate_data(
    db_address: str,
    db_name: str,
    data_generator_func: Callable,
    time_action: float | None = None,
    custom_actions: list | None = None,
    editing_grade: int | None = None,
    quantity_interactions: int | None = None,
):
    logger = setup_custom_logger()

    loop_count = 0
    while quantity_interactions is None or loop_count < quantity_interactions:
        if not custom_actions:
            custom_actions = ['create', 'update', 'delete']

        action = random.choice(custom_actions)

        data_generator = data_generator_func()

        name_collection = list(data_generator.keys())[0]
        data_document = data_generator[name_collection][0]

        if action in ['create', 'update']:
            simulator = MongoDBActions(
                db_address, db_name, name_collection, data_document
            )
            if action == 'create':
                id = simulator.create_document()
                logger.info(
                    f'ADD DOCUMENT      [{name_collection} - ObjectID: {id}]'
                )
            else:
                if editing_grade:
                    id = simulator.update_document(
                        percent_to_update=editing_grade
                    )
                    logger.info(
                        f'UPDATE* DOCUMENT   [{name_collection} - ObjectID: {id}]'
                    )
                else:
                    id = simulator.update_document()
                    logger.info(
                        f'UPDATE DOCUMENT   [{name_collection} - ObjectID: {id}]'
                    )
        else:
            simulator = MongoDBActions(
                db_address, db_name, name_collection, data_document
            )
            id = simulator.delete_document()
            logger.info(
                f'DELETE DOCUMENT   [{name_collection} - ObjectID: {id}]'
            )

        loop_count += 1

        if time_action is not None:
            time.sleep(random.uniform(0, time_action))
