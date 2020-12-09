"""
Classes for defining a game instance
"""
from enum import Enum
from .utils import Timer
import eventlet
import numpy as np
from .human import Human
from .bot import Bot
from .. import socketio
import asyncio

# read in the deck of possible words from disk
from os import path
import csv
cwd = path.dirname(path.realpath(__file__))
words = open(path.join(cwd, 'deck.csv'), 'r')
deck = [row[0] for row in csv.reader(words)]

class Game:
  def __init__(self, room_id, socketio_instance, num_rounds=3, players=[], deck=deck):
    self.bot = Bot('ResNet50', deck)
    self.players = players + [self.bot]
    self.state = GameState()
    self.deck = deck
    self.leaderboard = {'bot': 0}
    self.num_rounds = num_rounds   # initialized by game creator
    self.curr_round = 1
    self.id = room_id
    self.game_round = None
    self.socketio_instance = socketio_instance

  async def playGame(self):
    print("STARTING GAME...")
    self.state.status = "started"
    while self.curr_round <= self.num_rounds:
      print('curr_round is: ', self.curr_round)
      await self.playRound()
    await self.endGame()

  async def endGame(self):
    print("ENDING GAME...")
    await self.showLeaderboard()
    self.state.status = 'ended'
    await self.socketio_instance.emit("end_game", {"leaderboard": self.leaderboard}, room=self.id)
    # await self.socketio_instance.sleep(7)
    # await self.socketio_instance.emit("close_word", {}, room=self.id)
    self.curr_round = 1
    for elem in self.leaderboard.keys():
      self.leaderboard[elem] = 0
    await self.showLeaderboard()
  
  async def addPlayer(self, sid, username):
    self.players.append(Human(username, sid))
    if (self.game_round):
      self.game_round.players_copy.append(Human(username, sid))
    self.leaderboard[username] = 0
    await self.showLeaderboard()
  
  async def removePlayer(self, sid):
    for human in self.players:
      print("human: ", human)
      if human.sid == sid:
        self.players.remove(human)
        del self.leaderboard[human.username]
        if self.game_round:
          for p in self.game_round.players_drawn:
            if p.sid == sid:
              self.game_round.players_drawn.remove(p)
              break
        if self.game_round:
          for p_c in self.game_round.players_copy:
            if p_c.sid == sid:
              self.game_round.players_copy.remove(p_c)
              break
    await self.showLeaderboard()

  async def playRound(self):
    print("STARTING ROUND" + str(self.curr_round))
    self.game_round = Round(self)
    await self.game_round.runRound()
    self.curr_round += 1
  
  async def showLeaderboard(self):
    await self.socketio_instance.emit("show_leaderboard", {"leaderboard": self.leaderboard}, room=self.id)

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
      await self.game.socketio_instance.emit('clear_canvas', {}, room=self.game.id)
      await self.game.showLeaderboard()
  
  async def next_drawing(self, player):
    await self.chooseDrawing(player)
    print("THE CHOICE IS...." + self.choice)
    self.drawing = Drawing(player, self, self.choice, 30)
    # print("WAITING FOR DRAWING, you have 30 seconds"
    if isinstance(player, Bot):
      model_outputs = await player.async_generate(self.choice)
      self.drawing.timer.start()
      await asyncio.wait([self.drawing.draw(model_outputs=model_outputs), self.drawing.revealLetters()])
    else:
      self.drawing.timer.start()
      await asyncio.wait([self.drawing.draw(), self.drawing.bot_guess(), self.drawing.revealLetters()])
    self.players_drawn.append(player)
    await self.game.socketio_instance.emit('draw_end', {}, room=self.game.id)

  def choosePlayer(self):
    # print("PLAYERSCOPY")
    # print(self.players_copy)
    player = self.players_copy[0]   # choose player who hasn't drawn
    self.players_copy.remove(player)  # delete from possible players to draw
    return player    # return player object
    
  async def chooseDrawing(self, player):
    options = np.random.choice(self.game.deck, 3, replace=False)

    self.choice = ""
    # if the player is a bot, choose the word immediately
    if isinstance(player, Bot):
      self.choice = np.random.choice(options)
      print("Bot chose: ", self.choice)
      self.game.deck.remove(self.choice)
      return

    # TODO SOCKET: make choose_word REQUEST PLAYER TO CHOOSE from choices
    print("CHOOSING WORD")
    await self.game.socketio_instance.emit("choose_word", {'options': list(options), 'player': player.sid, 'username':player.username}, room=player.sid)
    await self.game.socketio_instance.emit("set_drawer", {'username':player.username}, room=self.game.id)
    print("Sending to " + str(self.game.id))
    seconds_slept = 0
    # poll every second
    while (len(self.choice) == 0 and seconds_slept < 10):
      await self.game.socketio_instance.sleep(1)
      seconds_slept += 1
    if (len(self.choice) == 0):
      self.choice = np.random.choice(options)
      await self.game.socketio_instance.emit("close_word", {"word": self.choice}, room=player.sid)
    print("person chose: ", self.choice)
    self.game.deck.remove(self.choice)

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
    self.letters_list = []
  
  async def draw(self, model_outputs=[]):
    # Wait for 3 seconds before beginning the drawing
    # Wait for x seconds as people guess, will later implement lowering / canceling 
    # clock as players get word and all players guess
    # if the artist is a bot
    roomId = self.game_round.game.id
    sio = self.game_round.game.socketio_instance
    data = {"roomId": roomId, "word": self.choice, "show": []}
    NUM_SKETCHES =  3
    # if isinstance(self.artist, Bot):
    #   model_outputs = await self.artist.async_generate(self.choice)
    # self.timer.start()
    await sio.emit('establish_word', data, room=roomId)
    await sio.emit('reveal_letter', data, room=roomId)
    sketch_idx = 0
    while self.timer.check() and len(self.correct_players) < len(self.game_round.game.players) - 1:
      if isinstance(self.artist, Bot) and len(model_outputs[sketch_idx]) > 0:
        nextStroke = model_outputs[sketch_idx].pop(0)
        await sio.emit("receive_draw", nextStroke, room=roomId)
        await sio.sleep(.05)
      elif isinstance(self.artist, Bot):
        # if more than a of the time has passed since the last drawing was drawn, then draw another one
        if sketch_idx < NUM_SKETCHES - 1 and self.timer.current_time() > (sketch_idx + 1) * self.timer.seconds / NUM_SKETCHES:
          sketch_idx += 1
          await sio.emit('clear_canvas', {}, room=self.game_round.game.id)
        await sio.sleep(0)
      else: # this is the case where the artist is not a Bot. Just sleep over and over again
        await sio.sleep(0)
    # await sio.emit("show_leaderboard", {"leaderboard": self.game_round.game.leaderboard}, room=self.game_round.game.id)
    # await sio.sleep(0)
    print("draw finished")

  def checkGuess(self, player_instance, username, guess):
    print("THE GUESS IS " + guess + " AND THE CORRECT ONE IS " + self.choice)
    if (player_instance == self.artist.sid):
      return 3
    if (player_instance in self.correct_players):
      return 4
    if guess == self.choice and (player_instance != self.artist.sid) and (player_instance not in self.correct_players):
      player = None
      for p in self.game_round.players_copy:
        if p.username == username:
          player = p
      if player == None:
        print("couldn't find player with username: ", username)
      self.correct_players.append(player_instance)
      # TODO: have some score multiplier with the time?
      # add points to a player, maybe move to another method later
      self.game_round.game.leaderboard[username] += self.time_limit - self.timer.current_time() + 5
      return 1
    else:
      self.guesses.append(guess)
      return 2

  def add_stroke(self, stroke):
    self.stroke_list.append(stroke)
  
  async def clear_strokes(self):
    roomId = self.game_round.game.id
    sio = self.game_round.game.socketio_instance
    self.stroke_list = []
    await sio.emit('clear_canvas', {}, room=roomId)

  async def bot_guess(self):
    bot_guesses = []
    bot_instance = self.game_round.game.bot
    bot_instance.guess_idx = 0
    bot_instance.guesses = []
    print("bot guessing...")
    while self.timer.check() and len(self.correct_players) < len(self.game_round.game.players) - 1:
      roomId = self.game_round.game.id
      sio = self.game_round.game.socketio_instance
      # await sio.sleep(3)
      guess_interval = 3 # guess every 3 seconds
      if isinstance(bot_instance, Bot) and \
        (self.timer.current_time() > (len(bot_guesses) + 1) * guess_interval):
        bot_guess = await bot_instance.classify(self.stroke_list, len(self.choice))
        correct = self.checkGuess(bot_instance.sid, 'bot', bot_guess)
        data = {'username': 'bot', 'roomId': roomId, 'guess': bot_guess}
        if correct == 1:
          print("CORRECT GUESS!")
          await sio.emit('receive_answer', data, room=roomId)
          break
        else:
          print("INCORRECT GUESS!")
          if bot_guess not in bot_guesses:
            await sio.emit('receive_guess', data, room=roomId)
            bot_guesses.append(bot_guess)
      await sio.sleep(0)
    print("bot guessing done...", self.timer.check(), len(self.correct_players), len(self.game_round.game.players))
    # await sio.sleep(0)

  async def revealLetters(self):
    len_choice = len(self.choice)
    revealed_letters = len_choice // 2   # the final result of the revealed letters will be 1/2 the word length

    sio   = self.game_round.game.socketio_instance
    delay = self.time_limit / revealed_letters  # delay time
    reveal_interval = 6 # reveal every 6 seconds
    while self.timer.check() and len(self.correct_players) < len(self.game_round.game.players) - 1:
      if (len(self.letters_list) >= len(self.choice) - 2):
        break
      curr_time = self.timer.current_time()
      if (curr_time > delay / 2 and curr_time > (len(self.letters_list) + 1) * reveal_interval):
        roomId = self.game_round.game.id
        
        show = np.random.choice(self.shown_letters, 1, replace=False)[0]
        self.letters_list.append([int(show), self.choice[show]])
        data = {'roomId': roomId, 'show': self.letters_list}

        self.shown_letters = self.shown_letters[self.shown_letters != show]
        await sio.emit("reveal_letter", data, room=roomId)
      # await sio.sleep(delay)
      await sio.sleep(0)
    # await sio.sleep(0)
    print("reveal finished")

