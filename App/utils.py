from jinja2 import FileSystemLoader, Environment
from datetime import date
import datetime


def time_is_valid(time: str):
    time_list = time.split(':')
    if len(time_list) != 2 or not all(x.isdigit() for x in time_list):
        return False
    return True


async def create_order_mess_full(**kwargs) -> str:
    try:
        kwargs['start_time'] = kwargs['start_time'][:5]
        kwargs['finish_time'] = kwargs['finish_time'][:5]
        kwargs['leave_time'] = kwargs['leave_time'][:5]
        kwargs['finish_time'] = kwargs['finish_time'][:5]
        kwargs['back_time'] = kwargs['back_time'][:5]
        kwargs['tasks'] = kwargs['tasks'].split(', ')
        kwargs['order_date'] = date.fromisoformat(kwargs['order_date'])
        kwargs['order_date'] = kwargs['order_date'].strftime('%d.%m.%Y')

        environment = Environment(loader=FileSystemLoader('templates/'))
        template = environment.get_template('order_mess.txt')
        mess = template.render(kwargs)
        return mess
    except Exception as e:
        raise f'Error loading or rendering template: {e}'


async def create_order_mess_admin(**kwargs) -> str:
    try:
        kwargs['start_time'] = kwargs['start_time'][:5]
        kwargs['finish_time'] = kwargs['finish_time'][:5]
        kwargs['leave_time'] = kwargs['leave_time'][:5]
        kwargs['finish_time'] = kwargs['finish_time'][:5]
        kwargs['tasks'] = kwargs['tasks'].split(', ')
        kwargs['order_date'] = date.fromisoformat(kwargs['order_date'])
        kwargs['order_date'] = kwargs['order_date'].strftime('%d.%m.%Y')

        environment = Environment(loader=FileSystemLoader('templates/'))
        template = environment.get_template('order_active.txt')
        mess = template.render(kwargs)
        return mess
    except Exception as e:
        raise f'Error loading or rendering template: {e}'