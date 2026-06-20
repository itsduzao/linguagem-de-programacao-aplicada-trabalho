from enum import Enum, auto


class GameState(Enum):
    """Available screens/states for the central game loop."""

    START_MENU = auto()
    GAMEPLAY = auto()
    VICTORY = auto()
    GAME_OVER = auto()
