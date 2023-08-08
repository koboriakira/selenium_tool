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

    def overview(self) -> str:
        """ 席種、備考を除いた試合の概要を取得 """
        return f"{self.tournament_name.value}\n{self.date.value}\n{self.venue.value}"
