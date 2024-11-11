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
  line_spawn_interval_decrease = 0.1
  min_line_spawn_interval = 1
  line_start_speed = 10
  line_speed_increase = 0.1
  max_line_speed = 35
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
    
    self.lines: list[Line] = []
    self.spawn_timer = 0

  def update(self):
    self.spawn_timer -= self.game.deltaTime
    
    if self.spawn_timer <= 0:
      elapsed_time = self.game.get_elapsed_time()
      self.spawn_timer = max(
        self.line_spawn_interval - elapsed_time * self.line_spawn_interval_decrease, 
        self.min_line_spawn_interval
      )
      
      line_direction = random.choice(self.line_directions)
      line_speed = min(
        self.line_start_speed + elapsed_time * self.line_speed_increase,
        self.max_line_speed
      )
      
      line = Line(self.game, line_direction, line_speed)
      self.lines.append(line)
      
    for line in self.lines: line.update()

  def render(self, surface: pygame.Surface):
    pygame.draw.rect(
      surface,
      self.arena_color,
      self.rect
    )
    
    for line in self.lines: line.render(surface)