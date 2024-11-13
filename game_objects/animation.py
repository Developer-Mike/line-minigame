from game_objects.game_object import GameObject
import pygame
import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class Animation(GameObject):
  def __init__(self, game: 'Game', duration: float, ping_pong: bool = False):
    self.game = game
    self.duration = duration
    self.ping_pong = ping_pong
    self.start_time = time.time()

  def update(self):
    pass

  def render(self, surface: pygame.Surface):
    pass
  
  def get_progress(self) -> float:
    progress = (time.time() - self.start_time) / self.duration
    
    if self.ping_pong:
      progress = progress % 2
      if progress > 1: progress = 2 - progress
    
    return progress
  
  def is_finished(self) -> bool:
    if self.ping_pong: return False
    return self.get_progress() >= 1.0