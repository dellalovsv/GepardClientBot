from . import query, logs


def get_deposit(uid: int = None) -> float | None:
    try:
        sql = 'select deposit from bills where uid=%s'
        res = query(sql, uid)
        if res is not None and res is not False and len(res) > 0:
            return float(res[0]['deposit'])
        return None
    except Exception as e:
        logs.logger.error(f'funcs.deposit.get_deposit: {e}')
        return None


def get_credit(uid: int = None) -> dict | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    try:
        sql = 'select credit, credit_date from users where uid=%s and credit!=0 and credit_date!="0000-00-00"'
        res = query(sql, uid)
        if res is not None and res is not False and len(res) > 0:
            res[0]['credit_date'] = str(res[0]['credit_date'])
            return res[0]

        return None
    except Exception as e:
        logs.logger.error(f'funcs.deposit.get_credit: {e}')
        return -1000
