import logging
from logging import getLogger

from common import slack
from common.printer import CliPrinter, Printer
from itskenpo.reservation_type import ReservationType
from itskenpo.vacancy import Vacancies, Vacancy
from itskenpo.visitor import Visitor

MAX_COUNTABLE_WEEKS = 13


class CheckReservationUseCase:
    def __init__(self, visitor: Visitor, printer: Printer | None = None) -> None:
        self._visitor = visitor
        self._printer = printer or CliPrinter()

    def execute(self, weeks: int = MAX_COUNTABLE_WEEKS) -> None:
        try:
            # ページを開く
            self._visitor.access_restaurant("鮨一新")

            vacancies = Vacancies.empty()
            for i in range(weeks + 1):
                self._printer.print(f"{i + 1}週目")

                # 予約種別(時間・席別)のタブをクリックして空きを調査
                for reservation in ReservationType:
                    self._printer.print(f"{reservation.label()}を調査")
                    self._visitor.click_tab(reservation.tab_id())
                    tbody_props = self._visitor.get_table_properties(reservation.table_id())
                    for prop in tbody_props:
                        vacancy = Vacancy.of(prop["date"], prop["time"], prop["text"])
                        if vacancy.is_not_full():
                            self._printer.print(str(vacancy))
                        vacancies.append(vacancy)
                self._visitor.click_next_week()

            if vacancies.filter_empty_or_limited().is_not_empty():
                slack.post_to_dm("鮨一新の空きがあるので確認する")

        finally:
            self._visitor.quit()


if __name__ == "__main__":
    # python -m src.itskenpo.check_reservation_usecase
    logger = getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    visitor = Visitor(logger=logger, wait_time=1)
    usecase = CheckReservationUseCase(visitor)
    usecase.execute(weeks=0)
