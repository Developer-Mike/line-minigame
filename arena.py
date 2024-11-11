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
  
  score_color = (138, 54, 55)
  score_font_type = 'assets/tiny-5.ttf'
  score_font_size = 16
  tenths_font_size = 8
  
  line_directions = [
    Vector2(1, 0),
    Vector2(-1, 0),
    Vector2(0, 1),
    Vector2(0, -1)
  ]
  
  line_spawn_interval = 5
  line_spawn_interval_decrease = 0.1
  min_line_spawn_interval = 1
  
  line_start_speed = 10
  line_speed_increase = 0.1
  max_line_speed = 35
  
  def __init__(self, game: 'Game'):
    super().__init__(game)
    
    self.score_font = pygame.font.Font(self.score_font_type, self.score_font_size)
    self.tenths_font = pygame.font.Font(self.score_font_type, self.tenths_font_size)
    
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
    # Draw arena
    pygame.draw.rect(
      surface,
      self.arena_color,
      self.rect
    )
    
    # Draw score
    score_text_content = str(int(self.game.get_elapsed_time()))
    score_text = self.score_font.render(
      score_text_content,
      False,
      self.score_color
    )
    
    score_text_rect = score_text.get_rect()
    score_text_rect.width -= self.score_font_size // 8 # Adjust for the font's padding
    score_text_rect.top = int((self.game.game_size - score_text_rect.height) / 2)
    score_text_rect.left = int((self.game.game_size - score_text_rect.width) / 2)
    
    surface.blit(score_text, score_text_rect)
    
    
    
    # Draw tenths of a second
    tenths_text_content = str(int(self.game.get_elapsed_time() * 10) % 10)
    tenths_text = self.tenths_font.render(
      tenths_text_content,
      False,
      self.score_color
    )
    
    tenths_text_rect = tenths_text.get_rect()
    score_text_content_bottom = score_text_rect.bottom - (self.score_font_size // 8) # Adjust for the font's padding
    tenths_text_rect.top = score_text_content_bottom - tenths_text_rect.height
    tenths_text_rect.left = score_text_rect.right + (self.score_font_size // 8)
    
    surface.blit(tenths_text, tenths_text_rect)
    
    # Draw lines    
    for line in self.lines: line.render(surface)