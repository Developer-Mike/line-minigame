from game_object import GameObject
import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class StartText(GameObject):
  font_color = (255, 255, 255)
  font_type = 'assets/tiny-5.ttf'
  font_size = 16
  
  def __init__(self, game: 'Game'):
    super().__init__(game)

  def update(self):
    pass

  def render(self, surface: pygame.Surface):
    pass