from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import Optional

class Board(db.Model):
    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    @classmethod
    def from_dict(cls, board_data):
        return cls(
            title=board_data["title"],
            owner=board_data["owner"]
        )

    def to_dict(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }

    def board_with_cards(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            "cards": [card.to_dict() for card in self.cards]
        }