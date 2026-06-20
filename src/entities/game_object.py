from abc import ABC, abstractmethod

import pygame


class GameObject(ABC):
    """Abstract base contract for drawable and updatable game entities."""

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update the object using the elapsed seconds since the previous frame."""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the object on the target surface."""

    @property
    @abstractmethod
    def rect(self) -> pygame.Rect:
        """Return the rectangle used for positioning and collision detection."""
