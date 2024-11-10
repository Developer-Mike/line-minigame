from game_object import GameObject
import pygame
from pygame import Rect
from constants import COLOR_ARENA, ARENA_SIZE, GAME_SIZE

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class Arena(GameObject):
  def __init__(self):
    self.rect = Rect(
      (GAME_SIZE - ARENA_SIZE) / 2,
      (GAME_SIZE - ARENA_SIZE) / 2,
      ARENA_SIZE,
      ARENA_SIZE
    )

  def update(self, game: 'Game'):
    pass

  def render(self, surface: pygame.Surface):
    pygame.draw.rect(
      surface,
      COLOR_ARENA,
      self.rect
    )