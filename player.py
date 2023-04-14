from __future__ import annotations
import typing
from game import MAP_SIZE, JAIL_CELL, Country_Name
from cells import Place
if typing.TYPE_CHECKING:
  from country import Country


class Player:
  def __init__(self, name: str, id: int, money: int):
    self.id = id
    self.name = name
    self.money = money
    # * dictionary with country id key
    self.owned_places: dict[Country_Name, list[Place]] = {}
    self.location: int = 0
    self.is_in_jail: bool = False

  def move(self, move_number: int):
    self.location += move_number
    self.location %= MAP_SIZE
    return self.location

  def buy(self, place: Place):
    self.money -= place.price
    country_name = place.country.name
    if country_name in self.owned_places:
      self.owned_places[country_name].append(place)
    else:
      self.owned_places[country_name] = [place]

  def go_to_jail(self):
    self.location = JAIL_CELL
    self.is_in_jail = True

  def free_from_jain(self):
    self.is_in_jail = False

  def pay(self, rent: int) -> bool:
    if (self.money < rent):
      return False
    self.money -= rent
    return True

  def get_status(self):
    print(
        f"---> player: '{self.name}' || money: '{self.money}' chooge || location: {self.location} || is in jail: {self.is_in_jail}\n")
