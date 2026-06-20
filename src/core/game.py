import pygame

from src.config import (
    BACKGROUND_COLOR,
    BLUE,
    FPS,
    GREEN,
    METEOR_IMAGE,
    RED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIP_IMAGE,
    SHIP_START_Y_OFFSET,
    WHITE,
    WIN_SCORE,
    WIN_SURVIVAL_SECONDS,
    YELLOW,
)
from src.core.state import GameState
from src.entities.ship import Ship
from src.factories.meteor_factory import MeteorFactory
from src.mediators.game_mediator import GameMediator
from src.utils.assets import load_image


class Game:
    """Main game application and central loop."""

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Desvio Astral")
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = self._create_background_surface()

        self.title_font = self._create_font(82)
        self.large_font = self._create_font(54)
        self.medium_font = self._create_font(34)
        self.small_font = self._create_font(26)

        ship_image = load_image(SHIP_IMAGE, size=(64, 64))
        meteor_image = load_image(METEOR_IMAGE, size=(54, 54))
        ship = Ship(
            image=ship_image,
            start_position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - SHIP_START_Y_OFFSET),
        )
        self.mediator = GameMediator(ship, MeteorFactory(meteor_image))

    def run(self) -> None:
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self.mediator.update(delta_time)
            self._draw()

        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RETURN:
                    self.mediator.handle_enter()

    def _draw(self) -> None:
        self.screen.blit(self.background, (0, 0))

        if self.mediator.state == GameState.START_MENU:
            self._draw_start_menu()
        elif self.mediator.state == GameState.GAMEPLAY:
            self._draw_gameplay()
        elif self.mediator.state == GameState.VICTORY:
            self._draw_victory_screen()
        elif self.mediator.state == GameState.GAME_OVER:
            self._draw_game_over_screen()

        pygame.display.flip()

    def _draw_start_menu(self) -> None:
        self._draw_centered_text("Desvio Astral", self.title_font, YELLOW, 130)
        self._draw_centered_text("2D Avoidance / Survival", self.medium_font, WHITE, 205)
        self._draw_centered_text("← / → Arrow Keys - Move", self.medium_font, BLUE, 290)
        self._draw_centered_text("ENTER - Start Game", self.medium_font, BLUE, 330)
        self._draw_centered_text(
            f"Survive {WIN_SURVIVAL_SECONDS}s or reach {WIN_SCORE:,} points",
            self.small_font,
            WHITE,
            405,
        )

    def _draw_gameplay(self) -> None:
        self.mediator.draw_gameplay(self.screen)
        self._draw_text(f"Score: {self.mediator.score}", self.medium_font, WHITE, 20, 18)
        self._draw_text(f"Time: {int(self.mediator.elapsed_time)}s", self.medium_font, WHITE, 20, 52)

    def _draw_victory_screen(self) -> None:
        self._draw_centered_text("Mission Complete!", self.large_font, GREEN, 180)
        self._draw_centered_text(f"Final Score: {self.mediator.final_score}", self.medium_font, WHITE, 265)
        self._draw_centered_text("Press ENTER to Play Again", self.medium_font, BLUE, 340)

    def _draw_game_over_screen(self) -> None:
        self._draw_centered_text("Game Over", self.large_font, RED, 180)
        self._draw_centered_text(f"Final Score: {self.mediator.final_score}", self.medium_font, WHITE, 265)
        self._draw_centered_text("Press ENTER to Retry", self.medium_font, BLUE, 340)

    def _draw_centered_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        y_position: int,
    ) -> None:
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        self.screen.blit(rendered, rect)

    def _draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        x_position: int,
        y_position: int,
    ) -> None:
        rendered = font.render(text, True, color)
        self.screen.blit(rendered, (x_position, y_position))

    @staticmethod
    def _create_font(size: int) -> pygame.font.Font:
        font_name = pygame.font.match_font("DejaVu Sans")
        if font_name is not None:
            return pygame.font.Font(font_name, size)

        return pygame.font.Font(None, size)

    @staticmethod
    def _create_background_surface() -> pygame.Surface:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        top_color = (23, 34, 79)
        bottom_color = BACKGROUND_COLOR

        for y_position in range(SCREEN_HEIGHT):
            mix = y_position / max(1, SCREEN_HEIGHT - 1)
            red = int(top_color[0] + (bottom_color[0] - top_color[0]) * mix)
            green = int(top_color[1] + (bottom_color[1] - top_color[1]) * mix)
            blue = int(top_color[2] + (bottom_color[2] - top_color[2]) * mix)
            pygame.draw.line(background, (red, green, blue), (0, y_position), (SCREEN_WIDTH, y_position))

        for index in range(80):
            alpha = 64 + (index % 5) * 26
            star_surface = pygame.Surface((2, 2), pygame.SRCALPHA)
            star_surface.fill((255, 255, 255, alpha))
            background.blit(star_surface, ((index * 97) % SCREEN_WIDTH, (index * 53) % SCREEN_HEIGHT))

        return background
