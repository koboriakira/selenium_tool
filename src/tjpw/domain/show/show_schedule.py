from dataclasses import dataclass

from tjpw.domain.show.show_schedule_date import ShowScheduleDate


def find_value(params: list[dict[str, str]], key: str) -> str:
    for param in params:
        if param["key"] == key:
            return param["value"]
    return ""


@dataclass(frozen=True)
class ShowSchedule:
    """
    下記をオブジェクトとして扱うデータクラス
    [
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
    """

    url: str
    tournament_name: str
    date: ShowScheduleDate
    venue: str
    seat_type: str
    note: str

    @staticmethod
    def from_dict(params: list[dict[str, str]]) -> "ShowSchedule":
        return ShowSchedule(
            url=find_value(params, "url"),
            tournament_name=find_value(params, "大会名"),
            date=ShowScheduleDate.from_str(find_value(params, "日時")),
            venue=find_value(params, "会場"),
            seat_type=find_value(params, "席種"),
            note=find_value(params, "備考"),
        )

    def overview(self) -> str:
        """席種、備考を除いた試合の概要を取得"""
        return f"{self.tournament_name}\n{self.date}\n{self.venue}"

    def convert_to_detail(self) -> str:
        """カレンダー登録用の詳細文を作成"""
        # URLと会場、座席と備考欄を合成する
        note_str = self.note.value if self.note else ""
        return f"{self.url}\n\n{self.venue.value}\n\n{self.seat_type.value}\n\n{note_str}"

    @property
    def open_datetime(self) -> datetime:
        """開場時間を含めた日時を取得"""
        return datetime.combine(self.date.convert_date(), self.date.open_time)

    @property
    def end_datetime(self) -> datetime:
        """終了時刻を取得。とりあえず開場時間から4時間後とする。"""
        return self.open_datetime + timedelta(hours=4)
