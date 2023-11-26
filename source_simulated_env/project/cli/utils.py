from datetime import datetime

from tabulate import tabulate
from termcolor import colored


def task_elapsed_time(task_start_time: float) -> str:
    """
    Calculate the elapsed time for a task from a given start time.

    Args:
        - ``task_start_time`` (float): The start time (timestamp) from which
        to calculate the elapsed time.

    Returns:
        - ``str``: A formatted representation of the elapsed time in the
        HH:MM:SS format.
    """
    current_time = datetime.now()
    time_difference = current_time - datetime.fromtimestamp(task_start_time)
    hours, remainder = divmod(time_difference.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'


def format_info_number_interactions(interactions: int | None) -> str:
    """
    Format the number of interactions for a task.

    Args:
        - ``interactions`` (int): The number of interactions for the task.

    Returns:
        - ``str``: A formatted message indicating the number of interactions.
    """
    if interactions is None:
        return colored('WARNING TASK [∞]', 'yellow')
    return colored(f'QUANTITY TASK [{interactions}]', 'green')


def print_result_run(task_name: str, task_id: str) -> str:
    """
    Format and return a success message for a task.

    Args:
        - ``task_name`` (str): The name of the task.
        - ``task_id`` (str): The ID of the task.

    Returns:
        - ``str``: A formatted message indicating the success of the task.
    """
    return colored(f'[ ✓ ] TASK: "{task_name}" ID: "{task_id}" ', 'green')


def print_running_actions(custom_actions: list) -> str:
    """
    Format and print the running actions of a task.

    Args:
        - ``custom_actions`` (list): A list of custom actions
    (e.g., ['create', 'update', 'delete']).

    Returns:
        - ``str``: A formatted string representing the running actions.
    """
    color_mapping = {
        'create': ('C', 'green'),
        'update': ('U', 'yellow'),
        'delete': ('D', 'red'),
    }

    formatted_actions = []

    if custom_actions:
        for action in custom_actions:
            action_key = action.lower()
            action_char, action_color = color_mapping.get(
                action_key, (action[0].upper(), None)
            )
            formatted_actions.append(
                colored(action_char, action_color) if action_color else action_char
            )

        return '-'.join(formatted_actions)
    
    else:
        for key,value in color_mapping.items():
            formatted_actions.append(colored(value[0], value[1]))

        return '-'.join(formatted_actions)



def print_result_list(tasks_info: list) -> str:
    """
    Get the table of active tasks or a message when there are no tasks.

    Args:
        - ``tasks_info`` (list): A list of active tasks formatted for display.

    Returns:
        - ``str``: A string containing the task table or a message.
    """
    if tasks_info:
        headers = [
            'TASK ID',
            'TASK NAME',
            'TIME AGO',
            'INTERACTIONS',
            'ACTIONS ON',
        ]
        table = tabulate(tasks_info, headers, tablefmt='heavy_outline')
        return table

    return colored(f'[ ! ] THERE ARE NO TASKS CURRENTLY RUNNING.', 'yellow')
