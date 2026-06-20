import pygame

from src.entities.game_object import GameObject


class Meteor(GameObject):
    """Falling obstacle; a single collision ends the current run."""

    def __init__(self, image: pygame.Surface, position: tuple[int, int], speed: float) -> None:
        self.image = image
        self.speed = speed
        self._rect = self.image.get_rect(midtop=position)

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def update(self, delta_time: float) -> None:
        self._rect.y += int(self.speed * delta_time)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self._rect)

    def is_out_of_bounds(self, screen_height: int) -> bool:
        return self._rect.top > screen_height
