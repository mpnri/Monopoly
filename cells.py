from __future__ import annotations
from enum import Enum
import typing
from game import PLACE_PRICE, PLACE_BUILDING_RENTS, PLACE_BUILDING_COST
if typing.TYPE_CHECKING:
  from player import Player
  from country import Country

class Cell_Action(Enum):
  Go = "Go"
  GoToJail = "GoToJail"
  Jail = "Jail"
  Empty = "Empty"


class Cell:
  def __init__(self, id: int):
    self.id = id


class Place(Cell):
  def __init__(self, id: int, country: Country, type: int):
    super().__init__(id)
    type = min(max(type, 0), 2)
    self.country = country
    self.price = PLACE_PRICE[country.name][type]
    self.rents = PLACE_BUILDING_RENTS[country.name][type]
    self.building_price = PLACE_BUILDING_COST[country.name]

    self.owner_id: int | None = None
    self.mortgage_price = self.price // 2
    self.un_mortgage_price = int(1.1 * self.mortgage_price)
    self.is_mortgaged: bool = False
    self.building_level = 0

  def get_rent_value(self, owner_id) -> int:
    if self.owner_id == None or self.is_mortgaged or self.owner_id == owner_id:
      return 0
    return self.rents[self.building_level]


class Property(Cell):
  def __init__(self, id: int, type: Cell_Action):
    super().__init__(id)
    self.type = type

  def do_action(self, player: Player):
    if self.type == Cell_Action.Go:
      player.money += 200
    elif self.type == Cell_Action.GoToJail:
      player.go_to_jail()
      print("--------------> you went to JAIL!!\n")
    else:
      pass
