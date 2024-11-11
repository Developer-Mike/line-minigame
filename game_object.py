import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class GameObject:
  def __init__(self, game: 'Game'):
    self.game = game
  
  def update(self):
    pass
  
  def render(self, surface: pygame.Surface):
    pass