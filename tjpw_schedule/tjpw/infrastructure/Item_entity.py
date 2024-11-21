from dataclasses import dataclass

from tjpw_schedule.tjpw.domain.schedule import (
    Date,
    Note,
    SeatType,
    TournamentName,
    TournamentSchedule,
    Venue,
)


@dataclass(frozen=True)
class ItemEntity:
    url: str
    tournament_name: str
    date: str
    venue: str
    seat_type: str | None = None
    note: str | None = None

    @staticmethod
    def from_dict(params: dict[str, str]):
        return ItemEntity(
            url=params.get("url"),
            tournament_name=params.get("tournament_name"),
            date=params.get("date"),
            venue=params.get("venue"),
            seat_type=params.get("seat_type"),
            note=params.get("note"),
        )

    def convert_to_tournament_schedule(self) -> TournamentSchedule:
        """TournamentScheduleに変換"""
        return TournamentSchedule(
            url=self.url,
            tournament_name=TournamentName(self.tournament_name),
            date=Date(self.date),
            venue=Venue(self.venue),
            seat_type=SeatType(self.seat_type) if self.seat_type else None,
            note=Note(self.note) if self.note else None,
        )
