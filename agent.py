from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    from player import Player
    from main import Game


def get_func_val(game: Game, player: Player):
    total_rent_price = 0
    for [key, cell_list] in player.owned_places.items():
        if len(cell_list) == (len(country.cities) for country in game.countries if country.name == key):
            total_rent_price += max((cell.rents[5] for cell in cell_list))
        for cell in cell_list:
            if cell.is_mortgaged:
                total_rent_price += int(0.45 * cell.price)
            else:
                total_rent_price += cell.price

    return player.money + total_rent_price


def agent_action(game: Game, dice_val: int, isDouble: bool):
    def dfs(node, state):
        pass
    pass
