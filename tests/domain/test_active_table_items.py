from unittest import TestCase
from tjpw_schedule.domain.scraper import ActiveTableItems, ActiveTableItem, ItemType


class TestActiveTableItems(TestCase):
    def test_convert(self):
        # Given
        url = "https://www.ddtpro.com/schedules/21886"
        active_table_item_list = [
            ActiveTableItem(ItemType.TOURNAMENT_NAME, "TJPW LIVE TOUR 2024 SPRING"),
            ActiveTableItem(
                ItemType.DATE, "2024年3月16日(土)\u3000開場11:30\u3000開始12:00"
            ),
            ActiveTableItem(ItemType.VENUE, "神奈川・横浜ラジアントホール"),
            ActiveTableItem(
                ItemType.SEAT_TYPE,
                "■チケット\n－前売り－\nスーパーシート 7,500円\n特別リングサイド 5,500円\n指定席 4,500円\nレディースシート 2,000円\n－当日－\nスーパーシート 8,000円\n特別リングサイド 6,000円\n指定席 5,000円\nレディースシート 2,500円\nU-18チケット 1,000円（要身分証）\n\n■販売場所\n公式チケット購入フォーム、チケットぴあ、ローソンチケット、e+\n※UNIVERSE会員先行受付＝2024年1月11日(木)12:00～1月15日(月)12:00、会場先行販売＝1月27日両国KFCホール大会、一般販売＝1月28日(日)～。",
            ),
        ]
        active_table_items = ActiveTableItems(url=url, items=active_table_item_list)

        # When
        entity = active_table_items.to_entity_with_url()
        actual = entity.convert_to_tournament_schedule()

        print(actual)

        # Then
        self.assertEqual(actual.url, url)
        self.assertEqual(actual.tournament_name.value, "TJPW LIVE TOUR 2024 SPRING")
        self.assertEqual(actual.date.convert_date().isoformat(), "2024-03-16")
        self.assertEqual(actual.date.open_time.strftime("%H:%M"), "11:30")
        self.assertEqual(actual.venue.value, "神奈川・横浜ラジアントホール")
