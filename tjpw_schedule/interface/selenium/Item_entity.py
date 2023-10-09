from dataclasses import dataclass
from typing import Optional
from tjpw_schedule.domain.schedule import TournamentSchedule, TournamentName, Date, Venue, SeatType, Note


@dataclass(frozen=True)
class ItemEntity:
    url: str
    tournament_name: str
    date: str
    venue: str
    seat_type: Optional[str] = None
    note: Optional[str] = None

    @staticmethod
    def from_dict(params: dict[str, str]):
        return ItemEntity(
            url=params.get("url"),
            tournament_name=params.get("tournament_name"),
            date=params.get("date"),
            venue=params.get("venue"),
            seat_type=params.get("seat_type"),
            note=params.get("note")
        )

    def convert_to_tournament_schedule(self) -> TournamentSchedule:
        """ TournamentScheduleに変換 """
        return TournamentSchedule(
            url=self.url,
            tournament_name=TournamentName(self.tournament_name),
            date=Date(self.date),
            venue=Venue(self.venue),
            seat_type=SeatType(self.seat_type) if self.seat_type else None,
            note=Note(self.note) if self.note else None
        )
