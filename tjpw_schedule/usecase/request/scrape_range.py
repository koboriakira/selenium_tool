from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta


@dataclass(frozen=True)
class ScrapeRange:
    """スクレイピングする範囲"""

    start_date: datetime
    end_date: datetime

    def __post_init__(self):
        if self.start_date.timestamp() > self.end_date.timestamp():
            raise ValueError("start_date must be earlier than end_date")

    @staticmethod
    def create_default_instance(is_dev: bool = False):
        JST = timezone(timedelta(hours=+9), "JST")
        start_date = datetime.now(JST)
        end_date = start_date + timedelta(days=(90 if not is_dev else 7))
        return ScrapeRange(start_date=start_date, end_date=end_date)

    @staticmethod
    def from_yyyymmdd(start_date: str, end_date: str):
        JST = timezone(timedelta(hours=+9), "JST")
        start_date = datetime.strptime(start_date, "%Y%m%d").replace(tzinfo=JST)
        end_date = datetime.strptime(end_date, "%Y%m%d").replace(tzinfo=JST)
        return ScrapeRange(start_date=start_date, end_date=end_date)

    def to_target_yyyymm_list(self) -> list[str]:
        """start_dateからend_dateまでの日付のリストを作成"""
        date_list = []
        start_date = self.start_date
        while start_date <= self.end_date:
            date_list.append(start_date)
            start_date += relativedelta(months=1)
        return [date.strftime("%Y%m") for date in date_list]
