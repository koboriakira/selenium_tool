import re
from dataclasses import dataclass
from datetime import date, time


@dataclass
class ShowScheduleDate:
    date_: date
    time_: time

    @staticmethod
    def from_str(value: str) -> "ShowScheduleDate":  # noqa: C901
        """
        valueの例: 2023年10月9日(月)\u3000開場13:00\u3000開始14:00
        """
        match = re.search(r"\d+年\d+月\d+日", value)
        if not match:
            msg = "日付の文字列から日付を取得できませんでした"
            raise ValueError(msg)
        # 2023年10月9日のような文字列を2023-10-9のような文字列に変換
        date_str = match.group().replace("年", "-").replace("月", "-").replace("日", "")
        # isoformatな文字列に変換。0埋めできてない箇所を埋める。例: 2023-10-9 -> 2023-10-09
        date_str = "-".join([f"{int(d):02d}" for d in date_str.split("-")])
        date_ = date.fromisoformat(date_str)

        # 開始時間を探してみる
        match = re.search(r"開始\d+:\d+", value)
        if match:
            try:
                time_str = match.group().replace("開始", "")
                time_ = time.fromisoformat(time_str + ":00")
                return ShowScheduleDate(date_=date_, time_=time_)
            except ValueError:
                msg = "開始時間の文字列から開始時間を取得できませんでした"
                raise ValueError(msg) from None

        # 開場時間を探してみる
        match = re.search(r"開場\d+:\d+", value)
        if match:
            try:
                time_str = match.group().replace("開場", "")
                time_ = time.fromisoformat(time_str + ":00")
                return ShowScheduleDate(date_=date_, time_=time_)
            except ValueError:
                msg = "開場時間の文字列から開場時間を取得できませんでした"
                raise ValueError(msg) from None

        msg = f"開場時間の文字列が見つかりませんでした: {self.value}"
        raise ValueError(msg)
