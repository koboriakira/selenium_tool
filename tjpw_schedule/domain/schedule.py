from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ItemType(Enum):
    """ 情報の種類 """
    # 大会名
    TOURNAMENT_NAME = "大会名"
    # 日時
    DATE = "日時"
    # 会場
    VENUE = "会場"
    # 席種
    SEAT_TYPE = "席種"
    # 備考
    NOTE = "備考"


@dataclass(frozen=True)
class TournamentName:
    value: str


@dataclass(frozen=True)
class Date:
    value: str


@dataclass(frozen=True)
class Venue:
    value: str


@dataclass(frozen=True)
class SeatType:
    value: str


@dataclass(frozen=True)
class Note:
    value: str


@dataclass(frozen=True)
class Item:
    tournament_name: TournamentName
    date: Date
    venue: Venue
    seat_type: SeatType
    note: Optional[Note] = None

    def __str__(self):
        return f"大会名: {self.tournament_name}\n日時: {self.date}\n会場: {self.venue}\n座種: {self.seat_type}\n備考: {self.note}"
