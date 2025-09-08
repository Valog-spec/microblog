from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from app.models.database import Base
from app.models.like import Like
from app.models.tweet import Tweet

followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    api_key: Mapped[str] = mapped_column(unique=True, nullable=False)

    tweets: Mapped[list["Tweet"]] = relationship(back_populates="author")
    likes: Mapped[list["Like"]] = relationship(back_populates="user")

    following: Mapped[list["User"]] = relationship(
        secondary=followers,
        primaryjoin=lambda: followers.c.follower_id == User.id,
        secondaryjoin=lambda: followers.c.followed_id == User.id,
        backref=backref("followers", lazy="select"),
        lazy="select",
    )
