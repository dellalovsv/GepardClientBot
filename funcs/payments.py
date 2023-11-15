from . import query, logs


def get_first_pay(uid: int = None) -> dict | int | None:
    if uid is None or not isinstance(uid, int):
        return None

    try:
        # TODO: Поиск первой оплаты
        ...
    except Exception as e:
        logs.logger.error(f'funcs.payments.get_first_pay: {e}')
        return -1000
