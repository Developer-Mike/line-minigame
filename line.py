from game_object import GameObject
import pygame
from pygame import Vector2, Rect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class Line(GameObject): 
  line_width = 2
  line_color = (255, 255, 255)
  teeth_frequency = 3
  
  def __init__(self, game: 'Game', direction: Vector2, speed: float):
    super().__init__(game)
    self.direction = direction
    self.speed = speed
    
    self.position = Vector2(0, 0)
    if self.direction.x < 0: self.position.x = self.game.game_size
    if self.direction.y < 0: self.position.y = self.game.game_size
    
  def update(self):
    self.position += self.direction * self.speed * self.game.deltaTime

  def render(self, surface: pygame.Surface):
    line_rect = Rect(
      round(self.position.x),
      round(self.position.y),
      max(self.line_width, abs(self.direction.y * self.game.game_size)),
      max(self.line_width, abs(self.direction.x * self.game.game_size))
    )
     
    pygame.draw.rect(
      surface,
      self.line_color,
      line_rect
    )
    
    # Draw teeth
    offset = (line_rect.top if self.direction.x == 0 else line_rect.left) % self.teeth_frequency
    
    for i in range(0, self.game.game_size, self.teeth_frequency):
      for j in range(2):
        tooth_offset_width = -1
        tooth_offset_blade = offset + i
        
        if j % 2 == 0: 
          tooth_offset_blade = self.game.game_size - tooth_offset_blade
          tooth_offset_width = self.line_width
        
        tooth_rect = Rect(
          line_rect.left + (tooth_offset_width if self.direction.y == 0 else tooth_offset_blade),
          line_rect.top + (tooth_offset_width if self.direction.x == 0 else tooth_offset_blade),
          1, 1
        )
        
        pygame.draw.rect(
          surface,
          self.line_color,
          tooth_rect
        )