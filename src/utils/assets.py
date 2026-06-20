from pathlib import Path

import pygame


def load_image(path: Path, size: tuple[int, int] | None = None) -> pygame.Surface:
    """
    Load an image with a relative path and optimize it for alpha blitting.

    Args:
        path: Relative path to the image file.
        size: Optional target size.

    Returns:
        Optimized pygame Surface.
    """
    if path.is_absolute():
        raise ValueError(f"Asset path must be relative: {path}")

    surface = pygame.image.load(str(path)).convert_alpha()

    if size is not None:
        surface = pygame.transform.smoothscale(surface, size).convert_alpha()

    return surface
