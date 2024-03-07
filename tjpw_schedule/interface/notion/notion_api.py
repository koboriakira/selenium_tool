import os
import requests
from tjpw_schedule.domain.schedule import TournamentSchedule
from tjpw_schedule.custom_logging import get_logger
import json

logger = get_logger(__name__)


class NotionApi:
    def __init__(self) -> None:
        self.domain = os.environ["LAMBDA_NOTION_API_DOMAIN"]
        self.notion_secret = os.environ["NOTION_SECRET"]

    def regist_tournament_schedule(self, schedule: TournamentSchedule):
        """スケジュールを登録"""
        logger.debug(schedule)
        data = {
            "url": schedule.url,
            "title": schedule.tournament_name.value,
            "date": schedule.date.isoformatted_date,
            "promotion": "東京女子プロレス",
            "tags": [],
        }

        return self._post(url=self.domain + "prowrestling", data=data)

    def _post(self, url: str, data: dict) -> dict:
        headers = {
            "access-token": self.notion_secret,
        }
        logger.debug(f"url: {url} data: {json.dumps(data, ensure_ascii=False)}")
        respone = requests.post(url=url, headers=headers, json=data)
        if respone.status_code != 200:
            raise Exception(
                f"status_code: {respone.status_code}, message: {respone.text}"
            )
        response_json = respone.json()
        logger.debug(json.dumps(response_json, ensure_ascii=False))
        return response_json["data"]
