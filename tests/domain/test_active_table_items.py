from unittest import TestCase

from tjpw.domain.scraper import ActiveTableItems


class TestActiveTableItems(TestCase):
    def test_convert(self):
        # Given
        scraped_results = [
            {"key": "url", "value": "https://www.ddtpro.com/schedules/23289"},
            {"key": "大会名", "value": "桐生真弥地元凱旋興行〜とうきょうじょしのやぼう〜"},
            {"key": "日時", "value": "2024年11月3日(日)　開場12:30　開始13:00"},
            {"key": "会場", "value": "群馬・Gメッセ群馬メインホールC（高崎市）"},
            {
                "key": "席種",
                "value": "■チケット\n－前売り－\nスーパーシート7,500円　完売\n特別リングサイド5,500円　完売\n指定席4,500円　完売\nレディースシート2,000円　完売\n\n■販売場所\n公式チケット購入フォーム、チケットぴあ、ローソンチケット、e+\n※UNIVERSE会員先行受付＝2024年8月15日(木)12:00～8月19日(月)12:00、一般販売＝8月31日(土)～。",
            },
            {
                "key": "備考",
                "value": "■全対戦カード\n○山下実優＆宮本もか　vs　上福ゆき＆桐生真弥\n○渡辺未詩＆らく＆鈴木志乃　vs　瑞希＆愛野ユキ＆風城ハル\n○「ねくじぇねトーナメント'24」1回戦\n上原わかな　vs　七瀬千花\n○長谷川美子　vs　高見汐珠\n○伊藤麻希＆キラ・サマー　vs　中島翔子＆HIMAWARI\n○鈴芽＆猫はるな　vs　鳥喰かや＆凍雅\n○3WAYマッチ\n辰巳リカ　vs　原宿ぽむ　vs　遠藤有栖",
            },
        ]
        # When
        actual = ActiveTableItems.from_scraped_result(scraped_results)

        # Then
        self.assertEqual(actual.url, url)
        self.assertEqual(actual.tournament_name.value, "TJPW LIVE TOUR 2024 SPRING")
        self.assertEqual(actual.date.convert_date().isoformat(), "2024-03-16")
        self.assertEqual(actual.date.open_time.strftime("%H:%M"), "11:30")
        self.assertEqual(actual.venue.value, "神奈川・横浜ラジアントホール")
