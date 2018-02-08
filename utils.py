import datetime

def isToday(timestamp):
    today = datetime.date.today()
    plan_day = datetime.datetime.fromtimestamp(timestamp).date()
    if (plan_day - today).days == 0:
        return True
    else:
        return False
