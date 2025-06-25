from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int] = mapped_column(nullable=False, default=0)
    board_id: Mapped[int] = mapped_column(ForeignKey("board.board_id"))
    board: Mapped["Board"] = relationship(back_populates="cards")

    def to_dict(self):
        return {
            "card_id" : self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
        }
    @classmethod
    def from_dict(cls, card_data):
        return cls(
            message = card_data["message"],
            likes_count = card_data.get("likes_count",0),
            board_id=card_data.get("board_id")
        )