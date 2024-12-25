from jinja2 import FileSystemLoader, Environment, TemplateNotFound
from datetime import date


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

        environment = Environment(loader=FileSystemLoader('App/templates/'))
        template = environment.get_template('order_mess.txt')
        mess = template.render(kwargs)
        return mess
    except Exception as e:
        raise Exception(f'Error loading or rendering template: {e}')


async def create_order_mess_admin(**kwargs) -> str:
    try:
        environment = Environment(loader=FileSystemLoader('App/templates/'))
        template = environment.get_template('order_active.txt')

        data = {
            'start_time': kwargs.get('start_time')[:5],
            'order_date': date.fromisoformat(kwargs.get('order_date')).strftime('%d.%m.%Y') if kwargs.get(
                'order_date') else None,
            'finish_time': kwargs.get('finish_time')[:5],
            'leave_time': kwargs.get('leave_time')[:5],
            'tasks': kwargs.get('tasks').split(', ')
        }
        msg = template.render(data)
        return msg
    except TemplateNotFound as e:
        raise e
    except Exception as e:
        raise Exception(f'Ошибка рендеринга сообщения: {e}')


async def create_profile_mess(kwargs: dict) -> str:
    try:
        environment = Environment(loader=FileSystemLoader('App/templates/'))
        template = environment.get_template('user_profile.txt')

        data = {
            'name': kwargs.get('name') if kwargs.get('name') else 'Не заполнено',
            'sex': kwargs.get('sex') if kwargs.get('sex') else 'Не заполнено',
            'born_date': date.fromisoformat(kwargs.get('born_date')).strftime('%d-%m-%Y') if kwargs.get(
                'born_date') else None,
            'skills': kwargs.get('skills') if kwargs.get('skills') else 'Не заполнено',
            'phone': kwargs.get('phone') if kwargs.get('phone') else 'Не заполнено',
            'tools': kwargs.get('tools') if kwargs.get('tools') else 'Не заполнено',
            'transport': kwargs.get('transport') if kwargs.get('transport') else 'Не заполнено',
            'other_info': kwargs.get('other_info') if kwargs.get('other_info') else 'Не заполнено',
            'status': kwargs.get('status') if kwargs.get('status') else 'Не заполнено',
            'rating': kwargs.get('rating') if kwargs.get('rating') else 'Не заполнено',
            'profit': kwargs.get('profit') if kwargs.get('profit') else 'Не заполнено',
            'orders': kwargs.get('orders') if kwargs.get('orders') else 'Не заполнено',
            'wallet': kwargs.get('wallet') if kwargs.get('wallet') else None,
            'reg_date': date.fromisoformat(kwargs.get('reg_date')).strftime('%d-%m-%Y') if kwargs.get(
                'reg_date') else None,
        }
        msg = template.render(data)
        return msg

    except TemplateNotFound as e:
        raise e
    except Exception as e:
        raise Exception(f'Ошибка рендеринга сообщения: {e}')