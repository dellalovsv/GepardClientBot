from . import query, logs, types
from config import Abills
from keyboards import phones
from messages import start as msg_start

from aiogram.filters import Filter
from aiogram.types import Message


class CheckUser(Filter):
    """
    Проверка существования абонента и его авторизация в системе.
    """

    async def __call__(self, m: Message):
        try:
            sql = 'select count(*) as count from users where tid=%s'
            res = query(sql, m.from_user.id)
            if res is not None and res is not False and len(res) > 0:
                if res[0]['count'] > 0:
                    return True
                else:
                    await m.answer(msg_start.no_auth, reply_markup=phones.kb_phones)
            else:
                await m.answer(msg_start.no_auth, reply_markup=phones.kb_phones)
        except Exception as e:
            logs.logger.error(f'funcs.users.CheckUser.__call__: {e}')
            return False


def get_uid_from_phone(phone: str = None) -> int | None:
    if '+7' not in phone and phone[0] != '7' and phone is None:
        return None

    try:
        if phone[0] == '7':
            phone = f'+{phone}'
        sql = 'select uid from users_pi where phone=%s'
        res = query(sql, phone)
        if res is not False and res is not None and len(res) > 0:
            return int(res[0]['uid'])
        else:
            return None
    except Exception as e:
        logs.logger.error(f'funcs.users.get_uid_from_phone: {e}')
        return None


def get_uid_from_tid(tid: int = None) -> int | None:
    try:
        sql = 'select uid from users where tid=%s'
        res = query(sql, tid)
        if res is not None and res is not False and len(res) > 0:
            return res[0]['uid']
        return None
    except Exception as e:
        logs.logger.error(f'funcs.users.get_uid_from_tid: {e}')
        return None


def new_user(uid: int = None, tid: int = None) -> bool:
    if uid is None or tid is None:
        return False

    try:
        sql = 'update users set tid=%s where uid=%s'
        if query(sql, tid, uid, commit=True):
            sql = 'select count(*) as count from users where uid=%s and tid=%s'
            res = query(sql, uid, tid)
            if res is not None and res is not False and len(res) > 0:
                if res[0]['count'] > 0:
                    return True
                else:
                    return False
        else:
            return False
    except Exception as e:
        logs.logger.error(f'funcs.users.new_user: {e}')
        return False


def get_user_password(uid: int = None) -> dict | int | None:
    if uid is None:
        return None

    try:
        sql = 'select id as login, decode(`password`, %s) as password from users where uid=%s limit 1'
        res = query(sql, Abills.secret_key, uid)
        if res is not None and res is not False and len(res) > 0:
            res = res[0]
            res['password'] = str(res['password'], 'utf-8')
            return res
        return None
    except Exception as e:
        logs.logger.error(f'funcs.users.get_user_password: {e}')
        return -1000


def get_passport(uid: int = None) -> dict | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    try:
        sql = ('select pasport_num, pasport_date, pasport_grant, __code_podrazdel as code_podrazdel from users_pi '
               'where uid=%s')
        res = query(sql, uid)
        if res is not None and res is not False and len(res) > 0:
            res[0]['pasport_date'] = str(res[0]['pasport_date'])
            return res[0]
        return None
    except Exception as e:
        logs.logger.error(f'funcs.users.get_passport: {e}')
        return -1000


def get_address(uid: int = None) -> str | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    try:
        sql = ('select address_street as street, address_build as build, address_flat as flat from users_pi where '
               'uid=%s')  # Запрос к БД для получения первичных данных об адресе
        res = query(sql, uid)  # Выполнение запроса
        if res is not None and res is not False and len(res) > 0:  # Проверка. Успешен ли запрос
            if len(res[0]['street']) > 0:  # Проверка. Не пустое ли поле
                if types.check_int(res[0]['street']):  # Проверка. Улица содержит индекс или строку
                    # Улица содержит индекс
                    street = res[0]['street']
                    build = res[0]['build']
                    flat = res[0]['flat']
                    sql = 'select number from builds where id=%s and street_id=%s'  # Запрос для получения № дома
                    res = query(sql, build, street)  # Выполнение запроса
                    if res is not None and res is not False and len(res) > 0:  # Проверка. Успешен ли запрос
                        build = res[0]['number']  # Получение № дома
                        sql = 'select name, district_id from streets where id=%s'  # Запрос для получения названия улицы и id дистрикта
                        res = query(sql, street)  # Выполнения запроса
                        if res is not None and res is not False and len(res) > 0:
                            street = res[0]['name']  # Присваивание названия улицы
                            district = res[0]['district_id']  # Приваивание id дистрикта
                            sql = 'select name from districts where id=%s'  # Запрос для получения названия дистрикта
                            res = query(sql, district)  # Выполнение запроса
                            if res is not None and res is not False and len(res) > 0:  # Проверка. Успешн ли запрос
                                district = res[0]['name']  # Присвоение названия дистрикта
                                if flat == '':  # Проверка. Есть ли № квартиры
                                    # Нет № квартиры
                                    return f'{district}; {street}, д. {build}'
                                else:
                                    # Есть № квартиры
                                    return f'{district}; {street}, д. {build}, кв. {flat}'
                elif str(res[0]['street']).isalpha():  # Если улица содержит строку
                    if len(res[0]['build']) > 0:  # Если № дома не пуст
                        if len(res[0]['flat']) > 0:  # Если № квартиры не пусто
                            return f'{res[0]["street"]}, д. {res[0]["build"]}, кв. {res[0]["flat"]}'
                        else:  # Если № квартиры пуст
                            return f'{res[0]["street"]}, д. {res[0]["build"]}'
            else:  # Улица ничего не содержит
                sql = ('select __addresscity as city, __addressstreet as street, __addresshome as build from users_pi '
                       'where uid=%s')  # Запрос. Город, улица, № дома
                res = query(sql, uid)  # Выполнение запроса
                if res is not None and res is not False and len(res) > 0:  # Проверка. Успешен ли запрос
                    if len(res[0]['build']) > 0:
                        if len(res[0]['city']) > 0 and len(res[0]['street']) > 0:
                            return f'{res[0]["city"]}; {res[0]["street"]}, {res[0]["build"]}'
                        if len(res[0]['city']) <= 0 and len(res[0]['street']) > 0:
                            return f'{res[0]["street"]}, {res[0]["build"]}'

        # Ошибка при запросе
        return None
    except Exception as e:
        logs.logger.error(f'funcs.users.get_address: {e}')
        return -1000


def get_info(uid: int = None) -> dict | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    try:
        res = {}
        sql = 'select fio, phone, contract_id, contract_date from users_pi where uid=%s limit 1'
        users_pi = query(sql, uid)
        if users_pi is not None and users_pi is not False and len(users_pi) > 0:
            sql = 'select registration, disable, deleted from users where uid=%s limit 1'
            users = query(sql, uid)
            if users is not None and users is not False and len(users) > 0:
                res['personal_info'] = {}
                res['personal_info']['fio'] = users_pi[0]['fio']
                res['personal_info']['phone'] = users_pi[0]['phone']
                res['personal_info']['passport'] = {}
                res['personal_info']['passport'] = get_passport(uid)
                res['personal_info']['address'] = get_address(uid)
                res['contract'] = {}
                res['contract']['number'] = users_pi[0]['contract_id']
                res['contract']['date'] = str(users_pi[0]['contract_date'])
                res['registration'] = str(users[0]['registration'])
                res['status'] = {}
                res['status']['disable'] = users[0]['disable']
                res['status']['deleted'] = users[0]['deleted']

            return res

        return None
    except Exception as e:
        logs.logger.error(f'funcs.users.get_info: {e}')
        return -1000
