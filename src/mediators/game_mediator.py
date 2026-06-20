import pygame

from src.config import (
    POINTS_PER_SECOND,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIP_START_Y_OFFSET,
    WIN_SCORE,
    WIN_SURVIVAL_SECONDS,
)
from src.core.state import GameState
from src.entities.meteor import Meteor
from src.entities.ship import Ship
from src.factories.meteor_factory import MeteorFactory


class GameMediator:
    """
    Coordinates entity interactions, state transitions, collisions, scoring,
    spawning, pruning, and safe game resets.
    """

    def __init__(self, ship: Ship, meteor_factory: MeteorFactory) -> None:
        self.ship = ship
        self.meteor_factory = meteor_factory
        self.meteors: list[Meteor] = []
        self.state = GameState.START_MENU
        self.elapsed_time = 0.0
        self.score = 0
        self.final_score = 0
        self.spawn_timer = 0.0

    def start_game(self) -> None:
        self.state = GameState.GAMEPLAY
        self.elapsed_time = 0.0
        self.score = 0
        self.final_score = 0
        self.spawn_timer = 0.0
        self.meteors = []
        self.ship.reset(self._ship_start_position())

    def update(self, delta_time: float) -> None:
        if self.state != GameState.GAMEPLAY:
            return

        self.elapsed_time += delta_time
        self.score = int(self.elapsed_time * POINTS_PER_SECOND)
        self.ship.update(delta_time)
        self._update_meteors(delta_time)
        self._spawn_meteors(delta_time)
        self._handle_collisions()
        self._handle_victory_condition()

    def draw_gameplay(self, surface: pygame.Surface) -> None:
        self.ship.draw(surface)
        for meteor in self.meteors:
            meteor.draw(surface)

    def handle_enter(self) -> None:
        if self.state in {GameState.START_MENU, GameState.VICTORY, GameState.GAME_OVER}:
            self.start_game()

    def _update_meteors(self, delta_time: float) -> None:
        for meteor in self.meteors:
            meteor.update(delta_time)

        self.meteors = [
            meteor
            for meteor in self.meteors
            if not meteor.is_out_of_bounds(SCREEN_HEIGHT)
        ]

    def _spawn_meteors(self, delta_time: float) -> None:
        self.spawn_timer += delta_time
        current_interval = self.meteor_factory.spawn_interval(self.elapsed_time)

        if self.spawn_timer >= current_interval:
            self.meteors.append(self.meteor_factory.create(self.elapsed_time))
            self.spawn_timer = 0.0

    def _handle_collisions(self) -> None:
        if any(self.ship.rect.colliderect(meteor.rect) for meteor in self.meteors):
            self.final_score = self.score
            self.state = GameState.GAME_OVER

    def _handle_victory_condition(self) -> None:
        if self.elapsed_time >= WIN_SURVIVAL_SECONDS or self.score >= WIN_SCORE:
            self.final_score = self.score
            self.state = GameState.VICTORY

    @staticmethod
    def _ship_start_position() -> tuple[int, int]:
        return SCREEN_WIDTH // 2, SCREEN_HEIGHT - SHIP_START_Y_OFFSET
