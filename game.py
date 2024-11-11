import pygame
from pygame.time import Clock
import ctypes
from player import Player
from arena import Arena
import time

class GameState:
  MENU = 0
  PLAYING = 1
  GAME_OVER = 2

class Game:
  background_color = (0, 0, 0)
  game_size = 64
  
  def __init__(self):
    user32 = ctypes.windll.user32
    self.screen_size = [user32.GetSystemMetrics(1), user32.GetSystemMetrics(1)]
    
    self.window = pygame.display.set_mode(self.screen_size)
    self.surface = pygame.Surface([self.game_size, self.game_size])
    pygame.init()
    
    self.clock = Clock()
    self.state = GameState.MENU
    
    self.start_game() # TODO: Implement menu screen

  def get_elapsed_time(self):
    return time.time() - self.start_time

  def mainloop(self):
    while True:
      if pygame.event.get(pygame.QUIT): break
      
      self.deltaTime = self.clock.tick(60) / 1000
        
      # Clear screen
      self.surface.fill(self.background_color)
      
      if self.state == GameState.MENU:
        pass # TODO: Implement menu screen
      elif self.state == GameState.PLAYING:        
        self.arena.update()
        self.player.update()
        
        self.arena.render(self.surface)
        self.player.render(self.surface)
      elif self.state == GameState.GAME_OVER:
        pass # TODO: Implement game over screen
      
      self.draw()

  def draw(self):
    frame = pygame.transform.scale(self.surface, self.screen_size)
    self.window.blit(frame, frame.get_rect())
    pygame.display.flip()
    
  def start_game(self):
    self.state = GameState.PLAYING
    self.start_time = time.time()
    
    self.arena = Arena(self)
    self.player = Player(self)
  
  def game_over(self):
    self.state = GameState.GAME_OVER