from aiogram.fsm.state import StatesGroup, State


class UserRegistration(StatesGroup):
    name = State()
    sex = State()
    born = State()
    skills = State()
    tools = State()
    phone = State()
    wallet = State()
    transport = State()
    other_info = State()
    save = State()


class SendingMessage(StatesGroup):
    waiting_msg = State()


class CreatingOrder(StatesGroup):
    waiting_employer = State()
    waiting_choose = State()
    waiting_date_order = State()
    waiting_tasks = State()
    waiting_place = State()
    waiting_work_form = State()
    waiting_price_full = State()
    waiting_price_hour = State()
    waiting_payment_form = State()
    waiting_need_workers = State()
    waiting_tools = State()
    waiting_transfer_type = State()
    waiting_leave_place = State()
    waiting_leave_time = State()
    waiting_start_time = State()
    waiting_finish_time = State()
    waiting_back_time = State()
    waiting_break_time = State()
    waiting_is_feed = State()
    waiting_clothes = State()
    waiting_add_info = State()
    waiting_break_duration = State()


class FindingUser(StatesGroup):
    waiting_msg = State()
    waiting_choose = State()


class DeletingUser(StatesGroup):
    waiting_delete_text = State()


class AddingEmployer(StatesGroup):
    waiting_name = State()
    waiting_company = State()
    waiting_address = State()
    waiting_phone = State()
    waiting_telegram_id = State()
    waiting_comment = State()