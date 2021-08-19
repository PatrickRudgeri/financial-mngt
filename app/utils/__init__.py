from django.utils import timezone as tz


def now():
    now_naive = tz.datetime.now()
    return tz.make_aware(now_naive, tz.get_current_timezone())
