from game_object import GameObject
import pygame
import random
from pygame import Rect, Vector2
from line import Line

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class Arena(GameObject):
  arena_color = (189, 75, 76)
  arena_size = 48
  line_spawn_interval = 5
  line_start_speed = 10
  line_directions = [
    Vector2(1, 0),
    Vector2(-1, 0),
    Vector2(0, 1),
    Vector2(0, -1)
  ]
  
  def __init__(self, game: 'Game'):
    super().__init__(game)
    
    self.rect = Rect(
      (self.game.game_size - self.arena_size) / 2,
      (self.game.game_size - self.arena_size) / 2,
      self.arena_size,
      self.arena_size
    )
    
    self.spawn_timer = 0

  def update(self):
    self.spawn_timer -= self.game.deltaTime
    
    if self.spawn_timer <= 0:
      self.spawn_timer = self.line_spawn_interval
      
      line_direction = random.choice(self.line_directions)
      line_speed = self.line_start_speed # TODO: Implement line speed increase
      
      line = Line(self.game, line_direction, line_speed)
      self.game.lines.append(line)

  def render(self, surface: pygame.Surface):
    pygame.draw.rect(
      surface,
      self.arena_color,
      self.rect
    )