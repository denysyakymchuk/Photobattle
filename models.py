from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config import Base

#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#
#     items = relationship("Item", back_populates="owner")
#
#
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("User", back_populates="items")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    gender = Column(String(5), nullable=False)
    unique = Column(String(300), nullable=True)
    active = Column(Boolean, default=False)
    likes = Column(Integer, default=0)
    posts = Column(Integer, default=0)
    block = Column(Boolean, default=False)
    delete_post_self = Column(Integer, default=0)
    delete_post_enemy = Column(Integer, default=0)
    cards = relationship('Cards', back_populates='cards', foreign_keys='Cards.user_id',
                            primaryjoin='User.id==Cards.user_id')

    def __repr__(self):
        return '<User %r>' % self.username


class Likes(Base):
    __tablename__ = "likes"
    id_likes = Column(Integer, primary_key=True)
    id_user = Column(Integer)
    id_card = Column(Integer)
    id_battle = Column(Integer)


class Cards(Base):
    __tablename__ = "cards"
    id_cards = Column(Integer, primary_key=True)
    image = Column(String(130))
    nickname = Column(String(120))
    all_likes = Column(Integer, default=0)
    battle_self = relationship('Battles', back_populates='_battle_self', foreign_keys='Battles.id_to_battle_self')
    battle_enemy = relationship('Battles', back_populates='_battle_enemy', foreign_keys='Battles.id_to_battle_enemy')
    user_id = Column(Integer, ForeignKey('user.id'))
    id_battle = Column(Integer, ForeignKey('battles.id_battles'))


class Battles(Base):
    __tablename__ = "battles"
    id_battles = Column(Integer, primary_key=True)
    id_to_battle_self = Column(Integer, ForeignKey('cards.id_cards'))
    id_to_battle_enemy = Column(Integer, ForeignKey('cards.id_cards'))


class Queue(Base):
    __tablename__ = "queue"
    id_queue = Column(Integer, primary_key=True)
    card_id = Column(Integer)

