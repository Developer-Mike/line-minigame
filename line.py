from game_object import GameObject
import pygame
from pygame import Vector2, Rect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class Line(GameObject):
  line_width = 2
  line_color = (255, 255, 255)
  shadow_color = (0, 0, 0)
  teeth_frequency = 3
  
  def __init__(self, game: 'Game', direction: Vector2, speed: float):
    super().__init__(game)
    self.direction = direction
    self.speed = speed
    
    self.position = Vector2(0, 0)
    if self.direction.x < 0: self.position.x = self.game.game_size
    if self.direction.y < 0: self.position.y = self.game.game_size
    
  def get_rect(self) -> Rect:
    return Rect(
      round(self.position.x),
      round(self.position.y),
      max(self.line_width, abs(self.direction.y * self.game.game_size)),
      max(self.line_width, abs(self.direction.x * self.game.game_size))
    )
    
  def update(self):
    self.position += self.direction * self.speed * self.game.deltaTime

  def render(self, surface: pygame.Surface):
    line_rect = self.get_rect()     
    self.render_box(
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
        
        self.render_box(
          surface,
          self.line_color,
          tooth_rect
        )
        
  def render_box(self, surface: pygame.Surface, color: tuple[int, int, int], rect: Rect):
    for y in range(rect.top, rect.bottom):
      for x in range(rect.left, rect.right):
        pixel_rect = Rect(
          x, y,
          1, 1
        )
        
        pixel_color = color
        is_outside_of_arena = not self.game.arena.rect.contains(pixel_rect)
        
        # Chessboard pattern outside the arena
        if is_outside_of_arena:
          if x % 2 == y % 2: continue
          pixel_color = self.game.accent_color_dark
        
        # Shadow of pixel
        if not is_outside_of_arena:
          shadow_rect = pixel_rect.move(0, 1)
          
          target_pixel_color = surface.get_at(shadow_rect.topleft)
          target_pixel_rgb = target_pixel_color.r, target_pixel_color.g, target_pixel_color.b
          
          if target_pixel_rgb != color and target_pixel_rgb != self.shadow_color:
            pygame.draw.rect(
              surface,
              self.shadow_color,
              shadow_rect
            )
        
        # Pixel itself
        pygame.draw.rect(
          surface,
          pixel_color,
          pixel_rect
        )