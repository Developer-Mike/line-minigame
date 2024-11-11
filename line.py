from game_object import GameObject
import pygame
from pygame import Vector2, Rect
from constants import GAME_SIZE, COLOR_LINE

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

DIRECTION = {
  'LEFT': Vector2(-1, 0),
  'RIGHT': Vector2(1, 0),
  'UP': Vector2(0, -1),
  'DOWN': Vector2(0, 1)
}

class Line(GameObject):
  def __init__(self, direction: Vector2):
    self.speed = 10
    self.line_width = 2
    self.teeth_frequency = 3
    self.direction = direction
    
    self.position = Vector2(0, 0)
    if self.direction.x < 0: self.position.x = GAME_SIZE
    if self.direction.y < 0: self.position.y = GAME_SIZE
    
  def update(self, game: 'Game'):
    self.position += self.direction * self.speed * game.deltaTime

  def render(self, surface: pygame.Surface):
    line_rect = Rect(
      round(self.position.x),
      round(self.position.y),
      max(self.line_width, abs(self.direction.y * GAME_SIZE)),
      max(self.line_width, abs(self.direction.x * GAME_SIZE))
    )
     
    pygame.draw.rect(
      surface,
      COLOR_LINE,
      line_rect
    )
    
    # Draw teeth
    offset = (line_rect.top if self.direction.x == 0 else line_rect.left) % self.teeth_frequency
    
    for i in range(0, GAME_SIZE, self.teeth_frequency):
      tooth_offset = offset + i
      
      tooth_rect = Rect(
        line_rect.left + (-1 if self.direction.y == 0 else tooth_offset),
        line_rect.top + (-1 if self.direction.x == 0 else tooth_offset),
        1, 1
      )
      
      pygame.draw.rect(
        surface,
        COLOR_LINE,
        tooth_rect
      )
      
      tooth_rect = Rect(
        line_rect.left + (self.line_width if self.direction.y == 0 else GAME_SIZE - tooth_offset),
        line_rect.top + (self.line_width if self.direction.x == 0 else GAME_SIZE - tooth_offset),
        1, 1
      )
      
      pygame.draw.rect(
        surface,
        COLOR_LINE,
        tooth_rect
      )