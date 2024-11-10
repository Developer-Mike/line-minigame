import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class GameObject:
  def update(self, game: 'Game'):
    pass
  
  def render(self, surface: pygame.Surface):
    pass