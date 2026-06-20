from pathlib import Path

import pygame


def load_image(
    path: Path,
    size: tuple[int, int] | None = None,
    transparent_color: tuple[int, int, int] | None = None,
) -> pygame.Surface:
    """
    Load an image with a relative path and optimize it for alpha blitting.

    PNG assets with an alpha channel are converted directly with convert_alpha().
    The ``transparent_color`` argument is kept for backward-compatibility but
    is ignored when the source file already carries its own transparency (PNG).

    Args:
        path: Relative path to the image file.
        size: Optional target size ``(width, height)`` in pixels.
        transparent_color: Unused for PNG assets; kept for API compatibility.

    Returns:
        Optimized pygame Surface with per-pixel alpha.
    """
    if path.is_absolute():
        raise ValueError(f"Asset path must be relative: {path}")

    surface = pygame.image.load(str(path)).convert_alpha()

    if size is not None:
        surface = pygame.transform.smoothscale(surface, size).convert_alpha()

    return surface