from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import date, time, datetime, timedelta
import re


@dataclass(frozen=True)
class TournamentName:
    value: str


@dataclass(frozen=True)
class Date:
    value: str

    @property
    def isoformatted_date(self) -> str:
        """yyyy-mm-dd形式の日付"""
        return self.convert_date().isoformat()

    def convert_date(self) -> date:
        # 正規表現をつかって、"2023年10月9日(月)\u3000開場13:00\u3000開始14:00"のような文字列から日付にあたる箇所を抜き出す
        match = re.search(r"\d+年\d+月\d+日", self.value)
        if match:
            # 2023年10月9日のような文字列を2023-10-9のような文字列に変換
            date_str = (
                match.group().replace("年", "-").replace("月", "-").replace("日", "")
            )
            # isoformatな文字列に変換。0埋めできてない箇所を埋める。例: 2023-10-9 -> 2023-10-09
            date_str = "-".join([f"{int(d):02d}" for d in date_str.split("-")])
            return date.fromisoformat(date_str)
        else:
            raise ValueError("日付の文字列から日付を取得できませんでした")

    @property
    def open_time(self) -> time:
        """開始時間を取得"""
        # 開始時間を探してみる
        match = re.search(r"開始\d+:\d+", self.value)
        if match:
            try:
                time_str = match.group().replace("開始", "")
                return time.fromisoformat(time_str + ":00")
            except:
                raise ValueError("開始時間の文字列から開始時間を取得できませんでした")

        # 開場時間を探してみる
        match = re.search(r"開場\d+:\d+", self.value)
        if match:
            try:
                time_str = match.group().replace("開場", "")
                return time.fromisoformat(time_str + ":00")
            except:
                raise ValueError("開場時間の文字列から開場時間を取得できませんでした")

        raise ValueError(f"開場時間の文字列が見つかりませんでした: {self.value}")


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
class TournamentSchedule:
    url: str
    tournament_name: TournamentName
    date: Date
    venue: Venue
    seat_type: SeatType
    note: Optional[Note] = None

    def overview(self) -> str:
        """席種、備考を除いた試合の概要を取得"""
        return f"{self.tournament_name.value}\n{self.date.value}\n{self.venue.value}"

    def convert_to_detail(self) -> str:
        """カレンダー登録用の詳細文を作成"""
        # URLと会場、座席と備考欄を合成する
        note_str = self.note.value if self.note else ""
        return (
            f"{self.url}\n\n{self.venue.value}\n\n{self.seat_type.value}\n\n{note_str}"
        )

    @property
    def open_datetime(self) -> datetime:
        """開場時間を含めた日時を取得"""
        return datetime.combine(self.date.convert_date(), self.date.open_time)

    @property
    def end_datetime(self) -> datetime:
        """終了時刻を取得。とりあえず開場時間から4時間後とする。"""
        return self.open_datetime + timedelta(hours=4)
