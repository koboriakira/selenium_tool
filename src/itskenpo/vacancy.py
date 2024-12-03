from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class VacancyType(Enum):
    EMPTY = "○"
    LIMITED = "△"
    FULL = "☓"

    @staticmethod
    def from_str(value: str) -> "VacancyType":
        if value == VacancyType.EMPTY:
            return VacancyType.EMPTY
        if value == VacancyType.LIMITED:
            return VacancyType.LIMITED
        if value in (VacancyType.FULL, "☓"):
            return VacancyType.FULL
        msg = f"Unexpected value: {value}"
        raise ValueError(msg)


@dataclass
class Vacancy:
    """空き予定"""

    datetime_: datetime
    type_: VacancyType

    @staticmethod
    def of(date_str: str, time_str: str, value: str) -> "Vacancy":
        datetime_ = datetime.strptime(
            f"{date_str} {time_str}:00+0900",
            "%Y-%m-%d %H:%M:%S%z",
        )
        type_ = VacancyType.from_str(value)
        return Vacancy(datetime_=datetime_, type_=type_)

    def is_not_full(self) -> bool:
        """満席でないかどうか"""
        return self.type_ != VacancyType.FULL

    def __str__(self) -> str:
        return f"{self.datetime_.strftime('%Y-%m-%d %H:%M')} {self.type_.value}"


@dataclass
class Vacancies:
    values: list[Vacancy]

    @staticmethod
    def empty() -> "Vacancies":
        return Vacancies([])

    def filter_empty_or_limited(self) -> "Vacancies":
        values = [v for v in self.values if v.type_ != VacancyType.FULL]
        return Vacancies(values)

    def append(self, vacancy: Vacancy) -> None:
        self.values.append(vacancy)

    def is_not_empty(self) -> bool:
        return len(self.values) > 0
