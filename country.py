from __future__ import annotations
from cells import Place
from game import Country_Name


class Country:
    def __init__(self, id: int, name: Country_Name):
        self.id = id
        self.name = name
        self.cities: list[Place] = []
        if name == Country_Name.Gray or name == Country_Name.Blue:
            self.cities = [Place(id*3+0, self, 0), Place(id*3+1, self, 1)]
        else:
            self.cities = [Place(id*3+0, self, 0), Place(id*3+1, self, 1), Place(id*3+2, self, 2)]
