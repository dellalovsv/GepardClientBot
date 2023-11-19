import config
from funcs import query, logs, telegram, deposit, payments, dt
from messages import info


def main():
    try:
        sql = 'select uid, tid from users where tid!=0'
        users = query(sql)
        if users is not None and users is not False and len(users) > 0:
            for user in users:
                days = deposit.get_left_days(user['uid'])
                if days == config.Abills.attention_days:
                    dep = deposit.get_deposit(user['uid'])
                    next_date_pay = payments.get_next_date_pay(user['uid'])[1]
                    telegram.sendMessage(int(user['tid']), info.internet_left_X_days % (
                        dt.get_now()[2], "%.2f" % float(dep), next_date_pay, days
                    ))
    except Exception as e:
        logs.logger.error(f'scripts.check_left_days.main: {e}')
        return False


if __name__ == '__main__':
    main()
