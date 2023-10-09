import os
import requests
from tjpw_schedule.domain.schedule import TournamentSchedule


class NotionApi:
    def __init__(self) -> None:
        self.domain = os.environ["DAILY_API_DOMAIN"] + "/notion"

    def regist_tournament_schedule(self, schedule: TournamentSchedule):
        """ スケジュールを登録 """
        print(schedule)
        json_data = {
            "title": schedule.tournament_name.value,
            "date": schedule.date.isoformatted_date,
            "url": schedule.url,
        }
        response = requests.post(url=self.domain + "/prowrestling/",
                                 json=json_data)
        return response.json()
