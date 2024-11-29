from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from dateutil.relativedelta import relativedelta

JST = timezone(timedelta(hours=+9), "JST")


@dataclass(frozen=True)
class ScrapeRange:
    """スクレイピングする範囲"""

    start_date: datetime
    end_date: datetime

    def __post_init__(self) -> None:
        if self.start_date.timestamp() > self.end_date.timestamp():
            msg = "start_date must be earlier than end_date"
            raise ValueError(msg)

    @staticmethod
    def create_default_instance(is_dev: bool | None = None) -> "ScrapeRange":
        start_date = datetime.now(JST)
        end_date = start_date + timedelta(days=(90 if not is_dev else 7))
        return ScrapeRange(start_date=start_date, end_date=end_date)

    def to_target_yyyymm_list(self) -> list[str]:
        """start_dateからend_dateまでの日付のリストを作成"""
        date_list: list[datetime] = []
        end_year = self.end_date.year
        end_month = self.end_date.month

        target_date = self.start_date
        while target_date.year <= end_year and target_date.month <= end_month:
            date_list.append(target_date)
            target_date += relativedelta(months=1)
        return [date.strftime("%Y%m") for date in date_list]
