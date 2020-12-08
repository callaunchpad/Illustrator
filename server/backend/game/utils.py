"""
Class for defining a simple timer
"""
import time

class Timer:
  def __init__(self, seconds):
    self.seconds = seconds
    self.start_time = None
  
  """
  starts the timer by setting the start_time instance variable to the current time
  """
  def start(self):
    self.start_time = time.perf_counter()

  """
  checks to see if time is up or not
  """
  def check(self):
    if (not self.start_time):
      print("timer has not started yet!")
      return False
    curr_time = time.perf_counter()
    if curr_time - self.start_time <= self.seconds:
      return True
    return False

  """
  returns the amount of time passed since the timer started
  """
  def current_time(self):
    if (not self.start_time):
      print("timer has not started yet!")
      return 0
    curr_time = time.perf_counter()
    return curr_time - self.start_time

  @staticmethod
  def wait_time(seconds):
    start_time = time.perf_counter()
    curr_time = time.perf_counter()
    while curr_time - start_time <= seconds:
      curr_time = time.perf_counter()
 