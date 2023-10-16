import os
import requests
from tjpw_schedule.domain.schedule import TournamentSchedule
from datetime import timedelta


class GasApi:
    def __init__(self) -> None:
        self.domain = os.environ["DAILY_API_DOMAIN"] + "/gas"

    def regist_tournament_schedule(self, schedule: TournamentSchedule):
        """ スケジュールを登録 """
        print(schedule)
        start = schedule.open_datetime
        # 終了時刻は開場時刻からとりあえず4時間後
        end = start + timedelta(hours=4)
        json_data = {
            "category": "東京女子",
            "title": schedule.tournament_name.value,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "detail": schedule.convert_to_detail(),
        }

        response = requests.post(url=self.domain + "/calendar/",
                                 json=json_data)
        return response.json()


if __name__ == "__main__":
    # python -m tjpw_schedule.interface.gas.gas_api
    from tjpw_schedule.domain.schedule import TournamentSchedule, TournamentName, Date, Venue, SeatType, Note
    suite = GasApi()
    schedule = TournamentSchedule(
        url='https://www.ddtpro.com/schedules/20450',
        tournament_name=TournamentName(value="TJPW CITY CIRCUIT '23～仙台再上陸～"),
        date=Date(value='2023年10月21日(土)\u3000開場12:30\u3000開始13:00'),
        venue=Venue(value='宮城・夢メッセみやぎ西館ホール（仙台市）'),
        seat_type=SeatType(value='■チケット\n－前売り－\nスーパーシート8,500円\u3000完売\n特別リングサイド6,500円\n指定席4,500円\nレディースシート2,000円\n－当日－\n特別リングサイド7,000円\n指定席5,000円\nレディースシート2,500円\nU-18チケット1,000円（要身分証）\n\n■販売場所\n公式チケット購入フォーム、チケットぴあ、ローソンチケット、e+\n※UNIVERSE会員先行受付＝7月20日(木)12:00～7月24日(月)12:00、一般販売＝8月6日(日)～。'),
        note=Note(value='■全カード\n○メインイベント\n瑞希＆遠藤有栖\u3000vs\u3000伊藤麻希＆上福ゆき\n○マックス・ジ・インペイラー＆愛野ユキ＆原宿ぽむ\u3000vs\u3000辰巳リカ＆渡辺未詩＆上原わかな\n○乃蒼ヒカリ＆角田奈穂\u3000vs\u3000宮本もか＆鳥喰かや\n○レジーナ\u3000vs\u3000HIMAWARI\n○中島翔子＆ハイパーミサヲ\u3000vs\u3000凍雅＆風城ハル\n○3WAYマッチ\nらく\u3000vs\u3000桐生真弥\u3000vs\u3000鈴木志乃\n○鈴芽\u3000vs\u3000大久保琉那'))
    suite.regist_tournament_schedule(schedule)
