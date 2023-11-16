from . import query, logs, deposit, tp, dt

from netaddr import IPAddress


payment_methods = {
    2: 'Оплата картой',
    5: 'Корректировка'
}


def get_first_pay(uid: int = None, method_to_string: bool = True) -> dict | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    try:
        sql = 'select * from payments where uid=%s and method=2 order by date asc limit 1'
        res = query(sql, uid)
        if res is not None and res is not False and len(res) > 0:
            res = res[0]
            res['date'] = str(res['date'])
            res['reg_date'] = str(res['reg_date'])
            res['ip'] = str(IPAddress(res['ip']))
            if method_to_string:
                res['method'] = payment_methods[res['method']]
            return res
        return None
    except Exception as e:
        logs.logger.error(f'funcs.payments.get_first_pay: {e}')
        return -1000


def get_last_pay(uid: int = None, method_to_string: bool = True) -> dict | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    try:
        sql = 'select * from payments where uid=%s and method=2 order by date desc limit 1'
        res = query(sql, uid)
        if res is not None and res is not False and len(res) > 0:
            res = res[0]
            res['date'] = str(res['date'])
            res['reg_date'] = str(res['reg_date'])
            res['ip'] = str(IPAddress(res['ip']))
            if method_to_string:
                res['method'] = payment_methods[res['method']]
            return res
        return None
    except Exception as e:
        logs.logger.error(f'funcs.payments.get_last_pay: {e}')
        return -1000


def get_all_pays(uid: int = None, method_to_string: bool = True) -> list | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    try:
        sql = 'select * from payments where uid=%s and method=2'
        res = query(sql, uid, uid)
        if res is not None and res is not False and len(res) > 0:
            i = 0
            while i < len(res):
                res[i]['date'] = str(res[i]['date'])
                res[i]['reg_date'] = str(res[i]['reg_date'])
                res[i]['ip'] = str(IPAddress(res[i]['ip']))
                if method_to_string:
                    res[i]['method'] = payment_methods[res[i]['method']]
                i += 1
            return res
        return None
    except Exception as e:
        logs.logger.error(f'funcs.payments.get_last_pay: {e}')
        return -1000


def get_next_date_pay(uid: int = None) -> list | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    tarif = tp.get_tp(uid)
    if tarif['day_fee'] <= 0:
        return -1  # unlimited

    days = int(float(deposit.get_deposit(uid)) / float(tarif['day_fee']))
    date = dt.plus_days(days)
    return [days, date]
