from enum import StrEnum

from allpay import Player


class Mode(StrEnum):
    PVP = "pvp"
    PVA = "pva"
    ANALYSIS = "analysis"


class AuctionKind(StrEnum):
    POORMAN = "poorman"
    RICHMAN = "richman"


class Phase(StrEnum):
    P1_BID = "p1-bid"
    P2_BID = "p2-bid"
    MOVING = "moving"
    GAME_OVER = "game-over"


class GameType(StrEnum):
    TOW = "tow"
    RACE = "race"


class Side(StrEnum):
    P1 = "p1"
    P2 = "p2"


SIDE_TO_PLAYER = {Side.P1: Player.P1, Side.P2: Player.P2}
PLAYER_TO_SIDE = {Player.P1: Side.P1, Player.P2: Side.P2}
