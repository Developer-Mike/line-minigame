from animation import Animation
import pygame
from pygame import Rect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class TitleText(Animation):
  font_color = (255, 255, 255)
  font_shadow_color = (0, 0, 0)
  font_type = 'assets/tiny-5.ttf'
  font_size = 16
  text_content = "Line"
  text_start_y = 10
  text_y_bounce = 1
  text_y_bounce_duration = 1
  
  def __init__(self, game: 'Game'):
    super().__init__(game, self.text_y_bounce_duration, ping_pong=True)
    
    self.font = pygame.font.Font(self.font_type, self.font_size)
    self.rect = Rect(
      0, self.text_start_y,
      0, 0
    )

  def update(self):
    pass

  def render(self, surface: pygame.Surface):
    text = self.font.render(self.text_content, False, self.font_color)
    self.rect = text.get_rect()
    
    self.rect.center = surface.get_rect().center
    self.rect.y = round(self.text_start_y + self.text_y_bounce * self.get_progress())
    
    # Shadow
    shadow_text = self.font.render(self.text_content, False, self.font_shadow_color)
    shadow_rect = self.rect.move(1, 1)
    surface.blit(shadow_text, shadow_rect)
    
    # Text
    surface.blit(text, self.rect)