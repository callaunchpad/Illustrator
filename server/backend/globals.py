"""
Global data structures and constants that need to be accessed throughout the backend
"""
from collections import defaultdict
"""
dict for tracking active rooms
maps room to list of players
"""
ROOMS_GAMES = {}

"""
dict for mapping player sid to game id
"""
PlAYER_TO_GAME = {}

"""
dictionary that maps roomId to a set of all usernames within that room
"""
ROOM_USERNAMES = defaultdict(set)