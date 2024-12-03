from enum import Enum


class ReservationType(Enum):
    """予約種別"""

    DINNER_17_TABLE = {  # noqa: RUF012
        "label": "ディナー17時・テーブル席",
        "tab_id": "link-2037",
        "table_id": "tcb-2037",
    }
    DINNER_19_TABLE = {  # noqa: RUF012
        "label": "ディナー19時・テーブル席",
        "tab_id": "link-2038",
        "table_id": "tcb-2038",
    }
    DINNER_17_COUNTER = {  # noqa: RUF012
        "label": "ディナー17時・カウンター席",
        "tab_id": "link-2039",
        "table_id": "tcb-2039",
    }
    DINNER_19_COUNTER = {  # noqa: RUF012
        "label": "ディナー19時・カウンター席",
        "tab_id": "link-2040",
        "table_id": "tcb-2040",
    }
    LUNCH_TABLE = {  # noqa: RUF012
        "label": "ランチ・テーブル席",
        "tab_id": "link-2041",
        "table_id": "tcb-2041",
    }
    LUNCH_COUNTER = {  # noqa: RUF012
        "label": "ランチ・カウンター席",
        "tab_id": "link-2042",
        "table_id": "tcb-2042",
    }

    def tab_id(self) -> str:
        return self.value["tab_id"]

    def table_id(self) -> str:
        return self.value["table_id"]

    def label(self) -> str:
        return self.value["label"]
