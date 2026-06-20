import pygame

from src.config import SCREEN_WIDTH, SHIP_SPEED
from src.entities.game_object import GameObject


class Ship(GameObject):
    """Player-controlled spaceship restricted to horizontal movement."""

    def __init__(self, image: pygame.Surface, start_position: tuple[int, int]) -> None:
        self.image = image
        self._rect = self.image.get_rect(center=start_position)

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def reset(self, start_position: tuple[int, int]) -> None:
        """Return the ship to its initial gameplay position."""
        self._rect = self.image.get_rect(center=start_position)

    def update(self, delta_time: float) -> None:
        keys = pygame.key.get_pressed()
        movement = 0

        if keys[pygame.K_LEFT]:
            movement -= SHIP_SPEED
        if keys[pygame.K_RIGHT]:
            movement += SHIP_SPEED

        self._rect.x += int(movement * delta_time)
        self._rect.left = max(0, self._rect.left)
        self._rect.right = min(SCREEN_WIDTH, self._rect.right)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self._rect)
