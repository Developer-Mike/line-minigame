from game_object import GameObject
import pygame
from pygame import Vector2, Rect
from constants import GAME_SIZE

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
    self.direction = direction
    
    if direction == DIRECTION['RIGHT'] or direction == DIRECTION['DOWN']: 
      self.position = Vector2(0, 0)
    elif direction == DIRECTION['LEFT']: self.position = Vector2(GAME_SIZE, 0)
    elif direction == DIRECTION['UP']: self.position = Vector2(0, GAME_SIZE)
    
  def update(self, game: 'Game'):
    self.position += self.direction * self.speed * game.deltaTime

  def render(self, surface: pygame.Surface):    
    pygame.draw.rect(
      surface,
      (255, 255, 255),
      Rect(
        round(self.position.x),
        round(self.position.y),
        GAME_SIZE if self.direction in [DIRECTION['UP'], DIRECTION['DOWN']] else 1,
        GAME_SIZE if self.direction in [DIRECTION['LEFT'], DIRECTION['RIGHT']] else 1
      )
    )