from game_object import GameObject
import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class StartText(GameObject):
  font_type = 'assets/tiny-5.ttf'
  font_size = 8
  text_content = "Press SPACE"
  text_y = 48
  
  def __init__(self, game: 'Game'):
    super().__init__(game)
    
    self.font_color = self.game.accent_color_dark
    self.font = pygame.font.Font(self.font_type, self.font_size)

  def update(self):
    pass

  def render(self, surface: pygame.Surface):
    text = self.font.render(self.text_content, False, self.font_color)
    text_rect = text.get_rect()
    
    text_rect.center = surface.get_rect().center
    text_rect.y = self.text_y
    
    surface.blit(text, text_rect)