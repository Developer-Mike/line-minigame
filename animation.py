from game_object import GameObject
import pygame
import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class Animation(GameObject):
  def __init__(self, game: 'Game', duration: float):
    self.game = game
    self.duration = duration
    self.start_time = time.time()

  def update(self):
    pass

  def render(self, surface: pygame.Surface):
    pass
  
  def get_progress(self) -> float:
    return (time.time() - self.start_time) / self.duration
  
  def is_finished(self) -> bool:
    return self.get_progress() >= 1.0