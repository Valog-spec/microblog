from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Like(Base):
    """Модель лайка пользователя на твите"""

    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))

    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")
