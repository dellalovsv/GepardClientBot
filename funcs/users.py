from . import query, logs
from keyboards import phones

from aiogram.filters import Filter
from aiogram.types import Message


class CheckUser(Filter):
    async def __call__(self, m: Message):
        try:
            sql = 'select count(*) as count from users where tid=%s'
            res = query(sql, m.from_user.id)
            if res is not None and res is not False and len(res) > 0:
                if res[0]['count'] > 0:
                    return True
                else:
                    await m.answer('No auth', reply_markup=phones.kb_phones)
            else:
                await m.answer('No auth', reply_markup=phones.kb_phones)
        except Exception as e:
            logs.logger.error(f'funcs.users.CheckUser.__call__: {e}')
            return False