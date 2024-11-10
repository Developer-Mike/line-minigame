from game_object import GameObject
import pygame
import random
from pygame import Rect
from constants import COLOR_ARENA, ARENA_SIZE, GAME_SIZE
from line import Line, DIRECTION

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class Arena(GameObject):
  def __init__(self):
    self.spawn_interval = 5
    
    self.rect = Rect(
      (GAME_SIZE - ARENA_SIZE) / 2,
      (GAME_SIZE - ARENA_SIZE) / 2,
      ARENA_SIZE,
      ARENA_SIZE
    )
    
    self.spawn_timer = 0

  def update(self, game: 'Game'):
    self.spawn_timer -= game.deltaTime
    
    if self.spawn_timer <= 0:
      self.spawn_timer = self.spawn_interval
      
      direction = random.choice(list(DIRECTION.values()))
      game.lines.append(Line(direction))

  def render(self, surface: pygame.Surface):
    pygame.draw.rect(
      surface,
      COLOR_ARENA,
      self.rect
    )