import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    password: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)

    login: Mapped["Login"] = relationship( back_populates="user")
    favorites: Mapped["Favorites"] = relationship( back_populates="user")
    charactersPlanets: Mapped["CharactersPlanets"] = relationship( back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.username,
            "first_name": self.firstname,
            "last_name": self.lastname
            # do not serialize the password, its a security breach
        }


class Login(db.Model):
    __tablename__ = "login"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)


    user: Mapped["User"] = relationship(back_populates="Login")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.username,
        }
    

class Favorites(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    charactersPlanets_id: Mapped[int] = mapped_column(ForeignKey("charactersPlanets.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    specific_details: Mapped[str] = mapped_column(String(120), nullable=False)

    user: Mapped["User"] = relationship(back_populates="Favorites")
    charactersPlanets: Mapped["CharactersPlanets"] = relationship( back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "specific_details": self.specific_details
        }
    

class CharactersPlanets(db.Model):
    __tablename__ = "charactersPlanets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    specific_details: Mapped[str] = mapped_column(String(120), nullable=False)

    user: Mapped["User"] = relationship(back_populates="CharactersPlanets")
    favorites: Mapped["Favorites"] = relationship(back_populates="CharactersPlanets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "specific_details": self.specific_details
        }
    