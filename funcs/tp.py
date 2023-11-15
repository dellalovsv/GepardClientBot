from . import query, logs


def get_tp(uid: int = None) -> dict | None:
    try:
        sql = 'select tp_id from dv_main where uid=%s'
        res = query(sql, uid)
        if res is not None and res is not False and len(res) > 0:
            sql = 'select name, day_fee from tarif_plans where id=%s'
            res = query(sql, res[0]['tp_id'])
            if res is not None and res is not False and len(res) > 0:
                return res[0]
        return None
    except Exception as e:
        logs.logger.error(f'funcs.tp.get_tp: {e}')
        return None
