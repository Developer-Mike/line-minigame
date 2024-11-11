import pygame
from pygame.time import Clock
import ctypes
from player import Player
from arena import Arena
from line import Line

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
    
    self.clock = Clock()
    self.state = GameState.PLAYING # TODO: Change to GameState.MENU
    
    # TODO: Deferring the creation of these objects to the start of the game
    self.arena = Arena(self)
    self.player = Player(self)
    self.lines: list[Line] = []

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
        for line in self.lines: line.update()
        
        self.arena.render(self.surface)
        self.player.render(self.surface)
        for line in self.lines: line.render(self.surface)
      elif self.state == GameState.GAME_OVER:
        pass # TODO: Implement game over screen
      
      self.draw()

  def draw(self):
    frame = pygame.transform.scale(self.surface, self.screen_size)
    self.window.blit(frame, frame.get_rect())
    pygame.display.flip()
    
  def start_game(self):
    pass
  
  def game_over(self):
    pass