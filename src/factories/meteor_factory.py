import random

import pygame

from src.config import (
    BASE_METEOR_SPEED,
    BASE_SPAWN_INTERVAL,
    DIFFICULTY_INTERVAL_SECONDS,
    METEOR_SPEED_INCREMENT,
    MIN_SPAWN_INTERVAL,
    SCREEN_WIDTH,
    SPAWN_INTERVAL_DECREMENT,
)
from src.entities.meteor import Meteor


class MeteorFactory:
    """Factory responsible for meteor creation and difficulty scaling."""

    def __init__(self, meteor_image: pygame.Surface) -> None:
        self.meteor_image = meteor_image

    def create(self, elapsed_time: float) -> Meteor:
        difficulty_level = self._difficulty_level(elapsed_time)
        speed = BASE_METEOR_SPEED + difficulty_level * METEOR_SPEED_INCREMENT
        half_width = self.meteor_image.get_width() // 2
        x_position = random.randint(half_width, SCREEN_WIDTH - half_width)

        return Meteor(
            image=self.meteor_image,
            position=(x_position, -self.meteor_image.get_height()),
            speed=speed,
        )

    def spawn_interval(self, elapsed_time: float) -> float:
        difficulty_level = self._difficulty_level(elapsed_time)
        interval = BASE_SPAWN_INTERVAL - difficulty_level * SPAWN_INTERVAL_DECREMENT
        return max(MIN_SPAWN_INTERVAL, interval)

    @staticmethod
    def _difficulty_level(elapsed_time: float) -> int:
        return int(elapsed_time // DIFFICULTY_INTERVAL_SECONDS)
