from __future__ import annotations
from enum import Enum
import random
from typing import NewType, Any
from player import Player
from country import Country, Country_Name
from cells import Place, Property, Cell_Action
import agent


class Game:
    def __init__(self):
        INIT_MONEY = 1500
        self.players = [
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

    def role_dice(self, showLog=True):
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        if showLog:
            print(f"dices values: {x}, {y}\n")
        return x+y, x == y

    def start(self):
        limit = 10
        for i in range(limit):
            for player in self.players:
                if player.name == "AI":
                    input("end turn! ")
                    dice_val, isDouble = self.role_dice(showLog=False)
                    agent.agent_action(self, dice_val, isDouble)
                    continue
                if i == 0:
                    player.get_status()
                input(f"your turn.{' you are in jail!' if player.is_in_jail else ''} role dice!\n")
                dice_val, isDouble = self.role_dice()
                if player.is_in_jail:
                    if isDouble:
                        print("Double dice. you're free!\n")
                        player.free_from_jain()
                    else:
                        ans = input(
                            "no Double dice. If you want to be free, pay 50 choogh. yes or no? ")
                        if ans == "yes" or ans == "y":
                            if player.pay(50):
                                player.free_from_jain()
                            else:
                                # todo: rent place or lose!
                                pass
                            print("---> you get free from jail\n")
                            player.get_status()
                        continue

                # * free
                location = player.move(dice_val)
                cell = self.game_map[location]
                if isinstance(cell, Place):
                    if not cell.owner_id and player.money >= cell.price:
                        ans = input(
                            f"this place is for sale({cell.price} choogh). do you want to buy it. yes or no? ")
                        if ans == "yes" or ans == "y":
                            player.buy(cell)
                            print("---> you bought this place\n")
                    elif cell.owner_id:
                        rent = cell.get_rent_value(player)
                        if rent >= player.money:
                            player.pay(rent)
                        else:
                            # todo: rent place or lose
                            pass

                else:
                    cell.do_action(player)
                    pass
                player.get_status()


if __name__ == "__main__":
    # Player("sa", 1000).buy(Place(0,Country(1,"s"),10,10))
    game = Game()
    input("start game: press enter ")
    game.start()
    pass
