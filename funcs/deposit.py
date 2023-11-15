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
    # TODO: Сделать проверку существования кредита
    ...
