import datetime


def parse_date(date: str) -> str:
    # TODO
    # FIXME
    date = datetime.datetime.fromisoformat(date) + datetime.timedelta(days=1)
    return date.strftime("%Y-%m-%d")
