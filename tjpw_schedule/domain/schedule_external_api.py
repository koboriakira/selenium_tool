from abc import ABCMeta, abstractmethod
import requests
import os
import json
from tjpw_schedule.domain.schedule import TournamentSchedule
from tjpw_schedule.custom_logging import get_logger

logger = get_logger(__name__)


class ScheduleExternalApi(metaclass=ABCMeta):
    @abstractmethod
    def save(self, schedule: TournamentSchedule) -> None:
        pass

    def post(
        self, url: str, headers: dict | None = None, data: dict | None = None
    ) -> list | dict:
        original_header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if headers:
            original_header.update(headers)
        logger.info(f"ScheduleExternalApi#_post: {url}")
        logger.info(f"ScheduleExternalApi#_post: {original_header}")
        logger.info(f"ScheduleExternalApi#_post: {data}")
        response = requests.post(url=url, headers=original_header, json=data)
        logger.info(response)
        logger.info(response.text)
        response_json = response.json()
        if isinstance(response_json, str):
            response_json = json.loads(response_json)
        return response_json


class ScheduleGoogleCalendarApi(ScheduleExternalApi):

    def __init__(self) -> None:
        self.domain = os.environ["LAMBDA_GOOGLE_CALENDAR_API_DOMAIN"]

    def save(self, schedule: TournamentSchedule) -> None:
        logger.debug(schedule)
        json_data = {
            "category": "東京女子",
            "title": schedule.tournament_name.value,
            "start": schedule.open_datetime.isoformat(),
            "end": schedule.end_datetime.isoformat(),
            "detail": schedule.convert_to_detail(),
        }

        logger.info(f"ScheduleGoogleCalendarApi#save: {schedule.tournament_name.value}")
        result = self.post(url=self.domain + "schedule", data=json_data)
        print(result)


class ScheduleNotionApi(ScheduleExternalApi):

    def __init__(self) -> None:
        self.domain = os.environ["LAMBDA_NOTION_API_DOMAIN"]
        self.notion_secret = os.environ["NOTION_SECRET"]

    def save(self, schedule: TournamentSchedule) -> None:
        logger.debug(schedule)
        data = {
            "url": schedule.url,
            "title": schedule.tournament_name.value,
            "date": schedule.date.isoformatted_date,
            "promotion": "東京女子プロレス",
            "tags": [],
        }
        headers = {
            "access-token": self.notion_secret,
        }
        logger.info(f"ScheduleNotionApi#save: {schedule.tournament_name.value}")
        url = self.domain + "prowrestling"
        result = self.post(url=url, headers=headers, data=data)
        print(result)


class ScheduleMockApi(ScheduleExternalApi):

    def save(self, schedule: TournamentSchedule) -> None:
        print("MockApi")
        print(schedule)
