import click
from tasks import (
    app,
    revoke_task,
    simulate_client_data,
    simulate_delivery_data,
    simulate_driver_data,
    simulate_location_data,
    simulate_product_data,
    simulate_vehicle_data,
)
from termcolor import colored
from utils import (
    format_info_number_interactions,
    print_result_list,
    print_result_run,
    print_running_actions,
    task_elapsed_time,
)

MODELS_MAPPING = {
    'driver': simulate_driver_data,
    'vehicle': simulate_vehicle_data,
    'client': simulate_client_data,
    'location': simulate_location_data,
    'product': simulate_product_data,
    'delivery': simulate_delivery_data,
}


@click.group()
def cli():
    pass


@cli.command(name='simulate-run')
@click.argument(
    'models',
    type=click.Choice(
        ['driver', 'vehicle', 'client', 'location', 'product', 'delivery'],
        case_sensitive=False,
    ),
    nargs=-1,
)
@click.option(
    '-a',
    '--db-address',
    envvar='MONGODB_ADDRESS',
    default='mongodb://mongodb:27017/',
    help='Database connection address.',
)
@click.option(
    '-n',
    '--db-name',
    envvar='DB_NAME',
    default='montogre',
    help=('Name of the database.'),
)
@click.option(
    '-t',
    '--time-action',
    default=None,
    type=int,
    help=('Maximum time for each interaction (in seconds).'),
)
@click.option(
    '-ca',
    '--custom-actions',
    default=None,
    multiple=True,
    type=click.Choice(['create', 'update', 'delete'], case_sensitive=False),
    help=('Specify custom actions (create, update, delete).'),
)
@click.option(
    '-e',
    '--editing-grade',
    default=None,
    type=int,
    help=('Percentage of keys to update in editing actions.'),
)
@click.option(
    '-q',
    '--quantity-interactions',
    default=None,
    type=int,
    help=('Total number of interactions to simulate.'),
)
def run(
    models,
    db_address,
    db_name,
    time_action,
    custom_actions,
    editing_grade,
    quantity_interactions,
):
    """
    Start the simulation through a task (Warning: If started directly without
    parameters, it performs random actions and an undetermined number of
    interactions))
    """
    for model in models:
        if model in MODELS_MAPPING:
            task_function = MODELS_MAPPING[model]
            result = task_function.apply_async(
                args=(
                    db_address,
                    db_name,
                    time_action,
                    custom_actions,
                    editing_grade,
                    quantity_interactions,
                )
            )
            click.echo(
                f'\n{print_result_run(task_function.__name__, result.id)}\n'
            )


@cli.command(name='simulate-list')
def list():
    """Lists and displays information about all running simulations(tasks)."""
    active_tasks = app.control.inspect().active()
    task_list = []

    if any(active_tasks.values()):

        for worker, tasks in active_tasks.items():
            for task in tasks:
                task_id = task['id']
                task_name = task['name']
                task_args = task['args']
                time_start = task['time_start']
                interactions = task_args[-1]
                time_ago_formatted = task_elapsed_time(time_start)
                formatted_interactions = format_info_number_interactions(
                    interactions
                )

                custom_actions = task_args[3]
                action_str = print_running_actions(custom_actions)

                task_list.append(
                    [
                        task_id,
                        task_name,
                        time_ago_formatted,
                        formatted_interactions,
                        action_str,
                    ]
                )

        click.echo(f'\n{print_result_list(task_list)}\n')

    else:
        click.echo(
            colored(
                '\n[ ! ] THERE ARE NO TASKS CURRENTLY RUNNING.\n', 'yellow'
            )
        )


@cli.command(name='simulate-revoke')
@click.argument('id_tasks', nargs=-1)
@click.option(
    '-a', '--all', is_flag=True, help='Revoke all running simulations.'
)
def revoke(id_tasks, all):
    """Revokes one or more simulations by id(tasks)."""
    if not id_tasks and not all:
        message_without_tasks_revoke = colored(
            '[ ! ] THE "revoke" COMMAND NEED A <TASK_ID> OR --all/--a FOR ALL'
            'TASKS',
            'yellow',
        )
        click.echo(f'\n{message_without_tasks_revoke}\n')
        return

    if all:
        active_tasks = app.control.inspect().active()
        if active_tasks and any(active_tasks.values()):
            id_tasks = []
            for tasks in active_tasks.values():
                if tasks:
                    for task in tasks:
                        id_tasks.append(task['id'])
        else:
            message_no_active_tasks = colored(
                '[ ! ] NO ACTIVE TASKS TO REVOKE.', 'yellow'
            )
            click.echo(f'\n{message_no_active_tasks}\n')
            return

    for id_task in id_tasks:
        result = revoke_task(id_task)
        if not result:
            message_erro_revoke_tasks = colored(
                f'[ ✗ ] TASK ID "{id_task}" NOT FOUND OR ALREADY REVOKED.',
                'red',
            )
            click.echo(f'\n{message_erro_revoke_tasks}\n')
        else:
            message_revoked_tasks = colored(
                f'[ ✓ ] TASK ID: {result} - REVOKE', 'green'
            )
            click.echo(f'\n{message_revoked_tasks}\n')


if __name__ == '__main__':
    cli()
