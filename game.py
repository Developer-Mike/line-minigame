import pygame
from pygame.time import Clock
import ctypes
from player import Player
from arena import Arena
from constants import GAME_SIZE, COLOR_VOID

class Game:
  def __init__(self):
    user32 = ctypes.windll.user32
    self.screen_size = [user32.GetSystemMetrics(1), user32.GetSystemMetrics(1)]
    
    self.window = pygame.display.set_mode(self.screen_size)
    self.surface = pygame.Surface([GAME_SIZE, GAME_SIZE])
    
    self.clock = Clock()
    
    self.arena = Arena()
    self.player = Player()
    self.lines = []

  def mainloop(self):
    while True:
      if pygame.event.get(pygame.QUIT): break
      
      self.deltaTime = self.clock.tick(120) / 1000
      
      self.arena.update(self)
      self.player.update(self)
      
      self.surface.fill(COLOR_VOID)
      
      self.arena.render(self.surface)
      self.player.render(self.surface)
      
      self.draw()

  def draw(self):
    frame = pygame.transform.scale(self.surface, self.screen_size)
    self.window.blit(frame, frame.get_rect())
    pygame.display.flip()