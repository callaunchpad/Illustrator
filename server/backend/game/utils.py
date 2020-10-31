"""
Class for defining a simple timer
"""
import time

class Timer:
  def __init__(self, seconds):
    self.seconds = seconds
    self.start_time = time.perf_counter()
  
  def check(self):
    curr_time = time.perf_counter()
    if curr_time - self.start_time <= self.seconds:
      return True
    return False

  def current_time(self):
    curr_time = time.perf_counter()
    return curr_time - self.start_time

  @staticmethod
  def wait_time(seconds):
    start_time = time.perf_counter()
    curr_time = time.perf_counter()
    while curr_time - start_time <= seconds:
      curr_time = time.perf_counter()
 