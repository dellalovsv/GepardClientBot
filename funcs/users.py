from . import query, logs
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
