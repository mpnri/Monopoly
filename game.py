from __future__ import annotations
from enum import Enum


class Country_Name(Enum):
    Gray = "Gray",
    Sky = "Sky",
    Pink = "Pink",
    Orange = "Orange",
    Red = "Red",
    Yellow = "Yellow",
    Green = "Green",
    Blue = "Blue"


MAP_SIZE = 40
JAIL_CELL = 10


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
