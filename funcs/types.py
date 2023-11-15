def check_int(data) -> bool:
    try:
        int(data)
        return True
    except ValueError:
        return False
