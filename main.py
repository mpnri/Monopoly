from __future__ import annotations
from typing import Union

MAP_SIZE = 40


class Country:
  def __init__(self, id: int, name: str):
    self.id = id
    self.name = name
    self.cities: list[Place] = []


class Cell:
  def __init__(self, id: int):
    self.id = id


class Place(Cell):
  def __init__(self, id: int, country: Country, price: int, rent: int):
    super().__init__(id)
    self.country = country
    self.price = price
    self.rent = rent
    self.owner: Player | None = None
    self.is_mortgaged: bool = False


class Player:
  def __init__(self, name: str, money: int):
    self.name = name
    self.money = money
    # dictionary by country key
    self.owned_places: dict[int, list[Place]] = {}
    self.location: int = 0

  def move(self, move_number: int):
    self.location += move_number
    self.location %= MAP_SIZE
    return self.location

  def buy(self, place: Place):
    self.money -= place.price
    country_id = place.country.id
    if country_id in self.owned_places:
      self.owned_places[country_id].append(place)
    else:
      self.owned_places[country_id] = [place]

if __name__ == "__main__":
  # Player("sa", 1000).buy(Place(0,Country(1,"s"),10,10))
  pass
