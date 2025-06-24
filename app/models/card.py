from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[Optional[int]]
    board_id: Mapped[Optional[int]] = mapped_column(ForeignKey("board.board_id"))
    board: Mapped[Optional["Board"]] = relationship(back_populates="cards")

    def to_dict(self):
        return {
            "card_id" : self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }
    @classmethod
    def from_dict(cls, card_data):
        return cls(
            message = card_data["message"],
            likes_count = card_data["likes_count"]
        )