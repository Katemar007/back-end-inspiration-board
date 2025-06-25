from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[Optional[int]]
    board_id: Mapped[int] = mapped_column(ForeignKey("board.board_id"))
    board: Mapped[Optional["Board"]] = relationship(back_populates="cards")