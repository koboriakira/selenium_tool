from datetime import datetime


class Vacancy:
    """空き予定"""

    datetime_: datetime
    value: str

    @staticmethod
    def of(date_str: str, time_str: str, value: str) -> "Vacancy":
        vacancy = Vacancy()
        vacancy.datetime_ = datetime.strptime(
            f"{date_str} {time_str}:00+0900",
            "%Y-%m-%d %H:%M:%S%z",
        )
        vacancy.value = value
        return vacancy
