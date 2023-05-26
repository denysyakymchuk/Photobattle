from pydantic import BaseModel
from pydantic.typing import Optional


class Battles(BaseModel):
    id_battles: int
    id_to_battle_self: int
    id_to_battle_enemy: int


class Cards(BaseModel):
    image: str
    nickname: str
    all_likes: int
    battle_self: list[Battles] = None
    battle_enemy: list[Battles] = None
    user_id: int
    id_battle: int


class User(BaseModel):
    username: str
    password: str
    email: str
    gender: str


class Likes(BaseModel):
    id_user: int
    id_card: int
    id_battle: int


class Queue(BaseModel):
    card_id: int