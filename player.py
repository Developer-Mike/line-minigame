import pygame
from pygame import Vector2, Rect
from game_object import GameObject
from constants import COLOR_PLAYER, COLOR_SHADOW

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

class Player(GameObject):
  def __init__(self):
    self.player_size = Vector2(2, 3)
    self.shadow_height = 2
    self.speed = 60
    self.jump_force = 20
    self.gravity = 50
    self.ground_timer_limit = 0.1
    self.jump_timer_limit = 0.1
    
    self.last_position = Vector2(0, 0)
    self.position = Vector2(0, 0)
    self.velocity = Vector2(0, 0)
    
    self.position_y = 0
    self.velocity_y = 0
    
    self.ground_timer = 0
    self.jump_timer = 0

  def move(self, input_vector: Vector2, deltaTime: float):
    if input_vector.magnitude() == 0: return
    
    movement_vector = input_vector.normalize() * self.speed * deltaTime
    self.position += movement_vector
    
  def get_input_vector(self) -> Vector2:
    keys = pygame.key.get_pressed()
    input_vector = Vector2(0, 0)
    
    if keys[pygame.K_w] or keys[pygame.K_UP]: input_vector.y -= 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]: input_vector.y += 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: input_vector.x -= 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: input_vector.x += 1
    
    return input_vector
  
  def bind_to_arena(self, game: 'Game'):
    hitbox_rect = Rect(
      round(self.position.x), 
      round(self.position.y), 
      self.player_size.x, 
      self.player_size.y
    )
    
    if not game.arena.rect.contains(hitbox_rect):
      self.position = Vector2(
        max(game.arena.rect.left, min(game.arena.rect.right - self.player_size.x, self.position.x)),
        max(game.arena.rect.top, min(game.arena.rect.bottom - self.player_size.y, self.position.y))
      )
    
  def update(self, game: 'Game'):
    # Apply wasd movement and calculate velocity
    self.last_position = self.position.copy()
    self.move(self.get_input_vector(), game.deltaTime)
    self.bind_to_arena(game)
    self.velocity = (self.position - self.last_position) / (game.deltaTime if game.deltaTime > 0 else 1)
    
    # Reduce ground timer
    if self.ground_timer > 0: self.ground_timer -= game.deltaTime
    if self.jump_timer > 0: self.jump_timer -= game.deltaTime
    
    # Check for jump
    if pygame.key.get_pressed()[pygame.K_SPACE]:
      self.jump_timer = self.jump_timer_limit
    
    # Apply gravity
    if self.position_y > 0:
      self.velocity_y -= self.gravity * game.deltaTime
      self.position_y += self.velocity_y * game.deltaTime
    else:
      self.position_y = 0
      self.velocity_y = 0
      self.ground_timer = self.ground_timer_limit
      
    # Apply jump
    if self.jump_timer > 0 and self.ground_timer > 0:
      self.velocity_y = self.jump_force
      self.position_y += self.velocity_y * game.deltaTime
      
  def get_shadow_rect(self, player_rect: Rect) -> Rect:
    shadow_width = player_rect.width + 2
    
    return Rect(
      round(self.position.x + (player_rect.width - shadow_width) / 2),
      round(self.position.y + 2), 
      shadow_width,
      self.shadow_height
    )
    
  def get_player_rects(self) -> list[Rect]:
    basic_rect = Rect(
      round(self.position.x),
      round(self.position.y),
      self.player_size.x,
      self.player_size.y
    )
    
    basic_rect.y -= self.position_y
    
    if self.position_y > 0:
      basic_rect.width -= 1
      
    if abs(self.velocity.y) > 1:
      basic_rect.top += 1
      basic_rect.height -= 1
      
    if abs(self.velocity.x) > 1:
      top_rect = Rect(
        basic_rect.x + (-1 if self.velocity.x > 0 else 1),
        basic_rect.y,
        basic_rect.width,
        1
      )
      
      basic_rect.top += 1
      basic_rect.height -= 1
      
      return [top_rect, basic_rect]
    
    return [basic_rect]
    
  def render(self, surface: pygame.Surface):
    player_rects = self.get_player_rects()
    
    # Draw shadow
    shadow_rect = self.get_shadow_rect(player_rects[-1])
    shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, COLOR_SHADOW, shadow_surface.get_rect())
    surface.blit(shadow_surface, shadow_rect)
    
    # Draw player
    for player_rect in player_rects:
      pygame.draw.rect(surface, COLOR_PLAYER, player_rect)