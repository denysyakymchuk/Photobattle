import datetime
from datetime import datetime as dt


def check_time_login(**kwargs):
    if kwargs['time'] is not None:
        if sec(kwargs['time']) >= 100:
            return True
        else:
            return False


def sec(second):
    first = str(datetime.datetime.now())[0:19]
    sec = dt.strptime(str(first), "%Y-%m-%d %H:%M:%S") - dt.strptime(str(second),
                                                                            "%Y-%m-%d %H:%M:%S")
    return sec