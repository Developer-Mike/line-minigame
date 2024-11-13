from  animation import Animation
import pygame
from pygame import Rect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class StartGameAnimation(Animation):
  duration = .5
  inflate_step = 2
 
  def __init__(self, game: 'Game'):
    super().__init__(game, self.duration)
    
    self.rect = Rect(
      self.game.title_text.rect.centerx,
      self.game.title_text.rect.centery,
      1, 1
    )
    
    self.last_step = self.get_progress()
    self.step_interval = self.duration / (self.game.game_size / 2)

  def update(self):
    if self.get_progress() - self.last_step >= self.step_interval:
      skipped_steps = int((self.get_progress() - self.last_step) / self.step_interval)
      self.last_step = self.get_progress()
      
      self.rect.inflate_ip(
        self.inflate_step * skipped_steps,
        self.inflate_step * skipped_steps
      )
      
      # Center the rectangle
      self.rect.center = self.game.title_text.rect.center

  def render(self, surface: pygame.Surface):
    pygame.draw.rect(
      surface,
      self.game.background_color,
      self.rect
    )