import os

import data_generator as generator
from celery import Celery
from simulator import simulate_data

RABBIT_MQ_ADDRESS = os.getenv(
    'RABBIT_MQ_ADDRESS', 'pyamqp://admin:admin@rabbitmq:5672//'
)

app = Celery(broker=RABBIT_MQ_ADDRESS)


@app.task
def simulate_driver_data(
    db_address,
    db_name,
    time_action,
    custom_actions,
    editing_grade,
    quantity_interactions,
):
    simulate_data(
        db_address=db_address,
        db_name=db_name,
        data_generator_func=generator.generator_driver_data,
        time_action=time_action,
        custom_actions=custom_actions,
        editing_grade=editing_grade,
        quantity_interactions=quantity_interactions,
    )


@app.task
def simulate_vehicle_data(
    db_address,
    db_name,
    time_action,
    custom_actions,
    editing_grade,
    quantity_interactions,
):
    simulate_data(
        db_address=db_address,
        db_name=db_name,
        data_generator_func=generator.generator_vehicle_data,
        time_action=time_action,
        custom_actions=custom_actions,
        editing_grade=editing_grade,
        quantity_interactions=quantity_interactions,
    )


@app.task
def simulate_client_data(
    db_address,
    db_name,
    time_action,
    custom_actions,
    editing_grade,
    quantity_interactions,
):
    simulate_data(
        db_address=db_address,
        db_name=db_name,
        data_generator_func=generator.generator_client_data,
        time_action=time_action,
        custom_actions=custom_actions,
        editing_grade=editing_grade,
        quantity_interactions=quantity_interactions,
    )


@app.task
def simulate_location_data(
    db_address,
    db_name,
    time_action,
    custom_actions,
    editing_grade,
    quantity_interactions,
):
    simulate_data(
        db_address=db_address,
        db_name=db_name,
        data_generator_func=generator.generator_location_data,
        time_action=time_action,
        custom_actions=custom_actions,
        editing_grade=editing_grade,
        quantity_interactions=quantity_interactions,
    )


@app.task
def simulate_product_data(
    db_address,
    db_name,
    time_action,
    custom_actions,
    editing_grade,
    quantity_interactions,
):
    simulate_data(
        db_address=db_address,
        db_name=db_name,
        data_generator_func=generator.generator_product_data,
        time_action=time_action,
        custom_actions=custom_actions,
        editing_grade=editing_grade,
        quantity_interactions=quantity_interactions,
    )


@app.task
def simulate_delivery_data(
    db_address,
    db_name,
    time_action,
    custom_actions,
    editing_grade,
    quantity_interactions,
):
    simulate_data(
        db_address=db_address,
        db_name=db_name,
        data_generator_func=generator.generator_delivery_data,
        time_action=time_action,
        custom_actions=custom_actions,
        editing_grade=editing_grade,
        quantity_interactions=quantity_interactions,
    )


def get_ids_tasks_in_progress() -> list:
    """
    Obtain a list of IDs of tasks in progress.

    Returns:
        ``list:`` A list of IDs of tasks in progress.
    """
    active_tasks = app.control.inspect().active()
    task_ids = []

    for tasks in active_tasks.values():
        for task in tasks:
            task_ids.append(task['id'])

    return task_ids


def revoke_task(task_id_to_revoke: str) -> bool | str:
    """
    Revoke an ongoing task with the specified ID.

    Args:
        - ``task_id_to_revoke:`` The ID of the task to be revoked.

    Returns:
        ``str:`` The ID of the task that was successfully revoked, or
        ``False`` if the task could not be revoked or was not found.
    """
    tasks_ids_before_revoke = get_ids_tasks_in_progress()
    if task_id_to_revoke in tasks_ids_before_revoke:
        app.control.revoke(task_id_to_revoke, terminate=True)
        tasks_ids_after_delete = get_ids_tasks_in_progress()
        if task_id_to_revoke not in tasks_ids_after_delete:
            return task_id_to_revoke
    else:
        return False
