from time import sleep

from src.tjpw.domain.schedule_external_api import (
    ScheduleExternalApi,
)
from src.tjpw.domain.scraper import Scraper
from src.tjpw.usecase.request.scrape_range import ScrapeRange
from src.tjpw.usecase.service.scrape_show import ScrapeShow


class ScrapeTjpw:
    def __init__(
        self,
        scraper: Scraper,
        schedule_external_api_list: list[ScheduleExternalApi],
    ) -> None:
        self.scraper = scraper
        self._schedule_external_api_list = schedule_external_api_list
        self._scrape_show = ScrapeShow(scraper, schedule_external_api_list)

    def execute(self, range: ScrapeRange) -> None:
        for target_yyyymm in range.to_target_yyyymm_list():
            print(f"target_yyyymm: {target_yyyymm}")

            # その月にふくまれる、試合詳細のURL一覧を取得
            detail_urls = self.scraper.get_detail_urls(
                target_year=int(target_yyyymm[:4]),
                target_month=int(target_yyyymm[4:]),
            )
            # 検索範囲内に絞る
            detail_urls = [d for d in detail_urls if range.is_in(d.date)]

            for detail_url in detail_urls:
                # スクレイピング
                sleep(3)
                show_schedule = self.scraper.scrape_detail(detail_url.value)

                # 注入したAPIの分、登録処理を行う
                for schedule_external_api in self._schedule_external_api_list:
                    schedule_external_api.save(show_schedule)


if __name__ == "__main__":
    # python -m src.tjpw.usecase.scrape_tjpw
    from src.tjpw.infrastructure.selenium_scraper import SeleniumScraper
    from src.tjpw.usecase.request.scrape_range import ScrapeRange

    controller = ScrapeTjpw(
        scraper=SeleniumScraper(),
        schedule_external_api_list=[],
    )
    controller.execute(ScrapeRange.create_default_instance(is_dev=True))
