"""
Classes for defining a game instance
"""
from enum import Enum
# from .game_round import Round, Drawing
from .utils import Timer
import eventlet
import numpy as np
from .human import Human
from .bot import Bot
from .. import socketio
import asyncio

class Game:
  def __init__(self, id, socketio_instance, num_rounds=3, players=[], deck=["apple","broccoli","baseball"]):
    self.players = players
    self.bot = Bot('ResNet50', deck)
    self.players.append(self.bot)
    self.state = GameState()
    self.deck = deck
    self.leaderboard = {'bot': 0}
    self.num_rounds = num_rounds   # initialized by game creator
    self.curr_round = 1
    self.id = id
    self.game_round = None
    self.socketio_instance = socketio_instance

  async def playGame(self):
    print("STARTING GAME...")
    self.state.status="started"
    while self.curr_round != self.num_rounds:
      print('curr_round is: ', self.curr_round)
      await self.playRound()
    await self.endGame()

  async def endGame(self):
    print("ENDING GAME...")
    self.showLeaderboard()
    self.state.status = 'ended'
    await self.socketio_instance.emit("end_game", {"leaderboard": self.leaderboard}, room=self.id)
    self.curr_round = 1
    for elem in self.leaderboard.keys():
      self.leaderboard[elem] = 0
  
  def addPlayer(self, id, username):
    self.players.append(Human(username, id))
    self.leaderboard[username] = 0
    # self.leaderboard[id] = 0

  async def playRound(self):
    print("STARTING ROUND" + str(self.curr_round))
    self.game_round = Round(self)
    await self.game_round.runRound()
    self.curr_round += 1
  
  def showLeaderboard(self):
    # TODO display leaderboard via socket

    # EVENTUALLY ADD 
    # await self.socketio_instance.emit("show_leaderboard", {"leaderboard": self.leaderboard}, room=self.id)
    None

"""
Class for defining a game state
"""
class GameState: 
  def __init__(self):
    self.status = 'started'

class Round:
  def __init__(self, game):
    self.players_drawn = []
    self.players_copy = game.players.copy()
    self.game = game
    self.drawing = Drawing("",0,"")
    self.choice = ""
  
  async def runRound(self):
    while len(self.players_drawn) < len(self.game.players):
      player = self.choosePlayer()
      await self.next_drawing(player)
      await self.game.socketio_instance.emit('clear_canvas', {}, roomId=self.game.id)
  
  async def next_drawing(self, player):
    # choice = await self.chooseDrawing(player)
    await self.chooseDrawing(player)
    # TODO: emit the chosen drawing to all users in the same room
    print("THE CHOICE IS...." + self.choice)
    self.drawing = Drawing(player, self, self.choice, 30)
    print("WAITING FOR DRAWING, you have 30 seconds")
    if (isinstance(self.drawing.artist, Bot)):
      await self.drawing.draw()
    else:
      await asyncio.wait([self.drawing.draw(), self.drawing.bot_guess(), self.drawing.revealLetters()])
    self.players_drawn.append(player)

  def choosePlayer(self):
    player = self.players_copy[0]   # choose player who hasn't drawn
    self.players_copy.remove(player)  # delete from possible players to draw
    return player    # return player object
    
  async def chooseDrawing(self, player):
    options = np.random.choice(self.game.deck, 3, replace=False)
    # TODO remove those choices from self.deck

    self.choice = ""
    # if the player is a bot, choose the word immediately
    if isinstance(player, Bot):
      self.choice = np.random.choice(options)
      print("Bot chose: ", self.choice)
      return

    # TODO SOCKET: make choose_word REQUEST PLAYER TO CHOOSE from choices
    print("CHOOSING WORD")
    await self.game.socketio_instance.emit("choose_word", {'options': list(options), 'player': player.sid}, room=player.sid)
    seconds_slept = 0
    # poll every second
    while (len(self.choice) == 0 and seconds_slept < 10):
      await self.game.socketio_instance.sleep(1)
      seconds_slept += 1
    if (len(self.choice) == 0):
      self.choice = np.random.choice(options)
      await self.game.socketio_instance.emit("close_word", room=player.sid)
    print("word is: ", self.choice)
    # return self.choice

"""
Class for defining a drawing
"""
class Drawing:
  def __init__(self, artist, game_round, choice, seconds=1):
    self.guesses = []  # incorrect guesses
    self.correct_players = []
    self.artist = artist
    self.choice = choice
    self.shown_letters = np.arange(len(choice))  # indexes of letters not shown
    self.timer = Timer(seconds + 3)  # to account for later wait_time stall
    self.time_limit = 30
    self.game_round = game_round
    self.stroke_list = []
  
  async def draw(self):
    # Wait for 3 seconds before beginning the drawing
    # Wait for x seconds as people guess, will later implement lowering / canceling 
    # clock as players get word and all players guess
  

    # if the artist is a bot
    roomId = self.game_round.game.id
    sio    = self.game_round.game.socketio_instance

    data =  {"roomId":roomId, "length_word":len(self.choice)}
    await sio.emit('establish_word', data, room=roomId)

    model_outputs = []
    if isinstance(self.artist, Bot):
      model_outputs = self.artist.generate(self.choice)

    while self.timer.check() and len(self.correct_players) < len(self.game_round.game.players) - 1:
      # self.showLeaderboard()

      if len(model_outputs) > 0:
        await sio.emit("receive_draw", model_outputs.pop(0), room=roomId)
        await sio.sleep(.05)
      else:
        await sio.sleep(0)
      # TODO start_draw stuff with socket responses
    
    await sio.emit("show_leaderboard", {"leaderboard": self.game_round.game.leaderboard}, room=self.game_round.game.id)

  def checkGuess(self, player_instance, username, guess):
    print("THE GUESS IS " + guess + " AND THE CORRECT ONE IS " + self.choice)
    if guess == self.choice and (player_instance not in self.correct_players):
      player = None
      for p in self.game_round.players_copy:
        if p.username == username:
          player = p
      if player == None:
        print("couldn't find player with username: ", username)
      self.correct_players.append(player)
      # TODO: have some score multiplier with the time?
      # add points to a player, maybe move to another method later
      self.game_round.game.leaderboard[username] += self.time_limit - self.timer.current_time()
      return True
    else:
      self.guesses.append(guess)
      return False

  def add_stroke(self, stroke):
    self.stroke_list.append(stroke)

  async def bot_guess(self):
    while self.timer.check() and len(self.correct_players) < len(self.game_round.game.players) - 1:
      roomId = self.game_round.game.id
      sio    = self.game_round.game.socketio_instance
      await sio.sleep(5)
      bot_instance = self.game_round.game.bot
      if isinstance(bot_instance, Bot):
        bot_guess = await bot_instance.classify(self.stroke_list)
        # TODO: maybe streamline this better??
        correct = self.checkGuess(bot_instance, 'bot', bot_guess)
        data = {'username': 'bot', 'roomId': roomId, 'guess': bot_guess}
        if correct:
          print("CORRECT GUESS!")
          await sio.emit('receive_answer', data, room=roomId)
        else:
          print("INCORRECT GUESS!")
          await sio.emit('receive_guess', data, room=roomId)

  async def revealLetters(self):
    len_choice = len(self.choice)
    revealed_letters = len_choice // 2   # the final result of the revealed letters will be 1/2 the word length

    delay = self.time_limit / revealed_letters  # delay time
    await sio.sleep(delay / 2)  # delay in beginning
    while self.timer.check() and len(self.correct_players) < len(self.game_round.game.players) - 1:
      roomId = self.game_round.game.id
      sio    = self.game_round.game.socketio_instance

      show = np.random.choice(self.shown_letters, 1, replace=False)[0]
      data = {'roomId': roomId, 'show': [int(show), self.choice[show]]}
      self.shown_letters = self.shown_letters[self.shown_letters != show]
      print("REVEALING DATA:")
      print(data["show"])
      await sio.emit("reveal_letter", data, room=roomId)
      await sio.sleep(delay)

