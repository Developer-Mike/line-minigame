import pygame
from pygame.time import Clock
import ctypes
from player import Player
from arena import Arena
import time
from game_over_animation import GameOverAnimation
from start_game_animation import StartGameAnimation
from title_text import TitleText
from start_text import StartText

class GameState:
  MENU = 0
  PLAYING = 1
  GAME_OVER = 2

class Game:
  background_color = (0, 0, 0)
  accent_color = (189, 75, 76)
  accent_color_dark = (138, 54, 55)
  game_size = 64
  
  @property
  def state(self) -> int: return self.__state
  
  def __init__(self):
    user32 = ctypes.windll.user32
    self.screen_size = [user32.GetSystemMetrics(1), user32.GetSystemMetrics(1)]
    
    self.window = pygame.display.set_mode(self.screen_size)
    self.surface = pygame.Surface([self.game_size, self.game_size])
    
    pygame.display.set_caption('Line')
    
    self.clock = Clock()
    pygame.init()
    
    self.return_to_menu()
    
  def return_to_menu(self):
    self.__state = GameState.MENU
    
    self.title_text = TitleText(self)
    self.start_text = StartText(self)
    self.start_game_animation = None
    
  def start_game(self):      
    self.__state = GameState.PLAYING
    self.start_time = time.time()
    
    self.arena = Arena(self)
    self.player = Player(self)
  
  def game_over(self):
    self.__state = GameState.GAME_OVER
    self.game_over_animation = GameOverAnimation(self)

  def mainloop(self):
    while True:
      if pygame.event.get(pygame.QUIT): break
      
      self.deltaTime = self.clock.tick(60) / 1000
      
      if self.state == GameState.MENU:
        self.render_menu()
      elif self.state == GameState.PLAYING:
        self.render_game()
      elif self.state == GameState.GAME_OVER:
        self.render_game_over()
      
      self.draw()

  def draw(self):
    frame = pygame.transform.scale(self.surface, self.screen_size)
    self.window.blit(frame, frame.get_rect())
    pygame.display.flip()
    
  def render_menu(self):
    if self.start_game_animation is not None:
      self.start_game_animation.update()
      self.start_game_animation.render(self.surface)
      
      if self.start_game_animation.is_finished():
        self.start_game()
      
      return
    
    # Clear screen
    self.surface.fill(self.accent_color)
    
    self.title_text.update()
    self.start_text.update()
    
    self.title_text.render(self.surface)
    self.start_text.render(self.surface)
    
    if pygame.event.get(pygame.KEYDOWN) and pygame.key.get_pressed()[pygame.K_SPACE]:
      if self.start_game_animation is not None: return
      self.start_game_animation = StartGameAnimation(self)
    
  def render_game(self):
    # Clear screen
    self.surface.fill(self.background_color)
    
    self.score = time.time() - self.start_time
    
    self.arena.update()
    self.player.update()
    
    self.arena.render(self.surface)
    self.player.render(self.surface)
    
  def render_game_over(self):
    if not self.game_over_animation.is_finished():
      self.game_over_animation.update()
      
      self.game_over_animation.render(self.surface)
      self.arena.render_score(self.surface) # Render score on top of the overlay
      
      return
    
    # Only allow to restart the game after the animation is finished
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        self.return_to_menu()