from __future__ import annotations
from enum import Enum
from typing import NewType, Any

MAP_SIZE = 40
JAIL_CELL = 10


class Country_Name(Enum):
  Gray = "Gray",
  Sky = "Sky",
  Pink = "Pink",
  Orange = "Orange",
  Red = "Red",
  Yellow = "Yellow",
  Green = "Green",
  Blue = "Blue"


PLACE_PRICE: dict[Country_Name, tuple[int, int, int]] = {
    Country_Name.Gray: (60, 60, 60),
    Country_Name.Sky: (100, 100, 120),
    Country_Name.Pink: (140, 140, 160),
    Country_Name.Orange: (180, 180, 200),
    Country_Name.Red: (220, 220, 240),
    Country_Name.Yellow: (260, 260, 280),
    Country_Name.Green: (300, 300, 320),
    Country_Name.Blue: (350, 400, 400),
}

PLACE_BUILDING_COST: dict[Country_Name, int] = {
    Country_Name.Gray: 50,
    Country_Name.Sky: 50,
    Country_Name.Pink: 100,
    Country_Name.Orange: 100,
    Country_Name.Red: 150,
    Country_Name.Yellow: 150,
    Country_Name.Green: 200,
    Country_Name.Blue: 200,
}


PLACE_BUILDING_RENTS: dict[Country_Name, tuple[list[int], list[int], list[int]]] = {
    Country_Name.Gray: ([2, 10, 30, 90, 160, 250],
                        [4, 20, 60, 180, 320, 450],
                        [4, 20, 60, 180, 320, 450]),
    Country_Name.Sky: ([6, 30, 90, 270, 400, 550],
                       [6, 30, 90, 270, 400, 550],
                       [8, 40, 100, 300, 450, 600]),
    Country_Name.Pink: ([10, 50, 150, 450, 625, 750],
                        [10, 50, 150, 450, 625, 750],
                        [12, 60, 180, 500, 700, 900]),
    Country_Name.Orange: ([14, 70, 200, 550, 700, 900],
                          [14, 70, 200, 550, 700, 950],
                          [16, 80, 220, 600, 800, 1000]),
    Country_Name.Red: ([18, 90, 250, 700, 875, 1050],
                       [18, 90, 250, 700, 875, 1050],
                       [20, 100, 300, 750, 925, 1100]),
    Country_Name.Yellow: ([22, 110, 330, 800, 975, 1150],
                          [22, 110, 330, 800, 975, 1150],
                          [24, 120, 360, 850, 1025, 1200]),
    Country_Name.Green: ([26, 130, 390, 900, 1100, 1275],
                         [26, 130, 390, 900, 1100, 1275],
                         [28, 150, 450, 1000, 1200, 1400]),
    Country_Name.Blue: ([35, 175, 500, 1100, 1300, 1500],
                        [50, 200, 600, 1400, 1700, 2000],
                        [50, 200, 600, 1400, 1700, 2000]),
}


class Country:
  def __init__(self, id: int, name: Country_Name):
    self.id = id
    self.name = name
    self.cities: list[Place] = []
    if name == Country_Name.Gray or name == Country_Name.Blue:
      self.cities = [Place(id*3+0, self, 0), Place(id*3+1, self, 1)]
    else:
      self.cities = [Place(id*3+0, self, 0), Place(id*3+1, self, 1), Place(id*3+2, self, 2)]


class Cell:
  def __init__(self, id: int):
    self.id = id


class Place(Cell):
  def __init__(self, id: int, country: Country, type: int):
    super().__init__(id)
    self.country = country
    type = min(max(type, 0), 2)
    self.price = PLACE_PRICE[country.name][type]
    self.rents = PLACE_BUILDING_RENTS[country.name][type]
    self.building_price = PLACE_BUILDING_COST[country.name]

    self.owner: Player | None = None
    self.mortgage_price = self.price // 2
    self.un_mortgage_price = int(1.1 * self.mortgage_price)
    self.is_mortgaged: bool = False
    self.building_level = 0

  def get_rent_value(self, player: Player) -> int:
    if self.owner == None or self.is_mortgaged:
      return 0
    return self.rents[self.building_level]


class Cell_Action(Enum):
  Go = "Go"
  GoToJail = "GoToJail"
  Jail = "Jail"
  Empty = "Empty"


class Property(Cell):
  def __init__(self, id: int, type: Cell_Action):
    super().__init__(id)
    self.type = type

  def do_action(self, player: Player):
    if self.type == Cell_Action.Go:
      player.money += 200
    elif self.type == Cell_Action.GoToJail:
      player.go_to_jail()
    else:
      pass


class Player:
  def __init__(self, name: str, id: int, money: int):
    self.id = id
    self.name = name
    self.money = money
    # * dictionary with country id key
    self.owned_places: dict[int, list[Place]] = {}
    self.location: int = 0
    self.is_in_jail: bool = False

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

  def go_to_jail(self):
    self.location = JAIL_CELL
    self.is_in_jail = True

  def pay_rent(self, rent: int) -> bool:
    if (self.money < rent):
      return False
    self.money -= rent
    return True


class Game:
  def __init__(self):
    INIT_MONEY = 1500
    self.player = [
        Player(name="You", id=0, money=INIT_MONEY),
        Player(name="AI", id=1, money=INIT_MONEY),
    ]
    self.countries: list[Country] = [
        Country(0, Country_Name.Gray), Country(1, Country_Name.Sky),
        Country(2, Country_Name.Pink), Country(3, Country_Name.Orange),
        Country(4, Country_Name.Red), Country(5, Country_Name.Yellow),
        Country(6, Country_Name.Green), Country(7, Country_Name.Blue),
    ]
    self.game_map: list[Place | Property] = [
        Property(0, Cell_Action.Go),
        self.countries[0].cities[0],
        Property(1, Cell_Action.Empty),  # todo: Community Chest
        self.countries[0].cities[1],
        Property(2, Cell_Action.Empty),  # todo: Income Tax
        Property(3, Cell_Action.Empty),  # todo: King Cross Station
        self.countries[1].cities[0],
        Property(4, Cell_Action.Empty),  # todo: Chance
        self.countries[1].cities[1],
        self.countries[1].cities[2],

        Property(5, Cell_Action.Jail),
        self.countries[2].cities[0],
        Property(6, Cell_Action.Empty),  # todo: Electric Company
        self.countries[2].cities[1],
        self.countries[2].cities[2],
        Property(7, Cell_Action.Empty),  # todo: MARYLEBONE Station
        self.countries[3].cities[0],
        Property(8, Cell_Action.Empty),  # todo: Community Chest
        self.countries[3].cities[1],
        self.countries[3].cities[2],

        Property(9, Cell_Action.Empty),  # todo: Free Parking
        self.countries[4].cities[0],
        Property(10, Cell_Action.Empty),  # todo: Chance
        self.countries[4].cities[1],
        self.countries[4].cities[2],
        Property(11, Cell_Action.Empty),  # todo: Frenchurch ST. Station
        self.countries[5].cities[0],
        self.countries[5].cities[1],
        Property(12, Cell_Action.Empty),  # todo: Water Workers
        self.countries[5].cities[2],

        Property(13, Cell_Action.GoToJail),
        self.countries[6].cities[0],
        self.countries[6].cities[1],
        Property(14, Cell_Action.Empty),  # todo: Community Chest
        self.countries[6].cities[2],
        Property(15, Cell_Action.Empty),  # todo: LIVERPOOL ST. Station
        Property(16, Cell_Action.Empty),  # todo: Chance
        self.countries[7].cities[0],
        Property(17, Cell_Action.Empty),  # todo: Super Tax
        self.countries[7].cities[1],

    ]

    for i in range(4):
      for j in range(10):
        cell = self.game_map[i*10+j]
        if (isinstance(cell, Place)):
          print(cell.price, end=" ")
        else:
          print("-", end=" ")
      print()


if __name__ == "__main__":
  # Player("sa", 1000).buy(Place(0,Country(1,"s"),10,10))
  Game()
  pass
