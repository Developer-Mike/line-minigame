from  animation import Animation
import pygame
from pygame import Rect
from arena import Arena

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class GameOverAnimation(Animation):
  duration = .5
  inflate_step = 2
  overlay_color = Arena.arena_color
 
  def __init__(self, game: 'Game'):
    super().__init__(game, self.duration)
    
    self.rect = Rect(
      game.player.position,
      game.player.player_size
    )
    
    self.last_step = self.get_progress()
    steps_count = max(
      game.player.position.x,
      game.player.position.y,
      game.game_size - game.player.position.x,
      game.game_size - game.player.position.y
    )
    self.step_interval = self.duration / steps_count

  def update(self):
    if self.get_progress() - self.last_step >= self.step_interval:
      skipped_steps = int((self.get_progress() - self.last_step) / self.step_interval)
      self.last_step = self.get_progress()
      
      self.rect.inflate_ip(
        self.inflate_step * skipped_steps,
        self.inflate_step * skipped_steps
      )
      
      # Center the rectangle around the player
      self.rect.left = int(self.game.player.position.x - self.rect.width / 2)
      self.rect.top = int(self.game.player.position.y - self.rect.height / 2)

  def render(self, surface: pygame.Surface):
    pygame.draw.rect(
      surface,
      self.overlay_color,
      self.rect
    )