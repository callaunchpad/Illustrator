# Illustrator
A pictionary-like web game with a bot to **generate and classify** sketches. 

Play the game at [illustrator-game.com](http://illustrator-game.com)!

# Overview
The Illustrator project is organized into 3 parts
## Sketch Classification: 
* Given a snapshot of a drawing, what is the most likely word that the user is drawing?
* MobileNet trained over 20 classes
## Sketch Generation:
* Given a word, non-deterministically generate a sketch of that word
* Implementation of Sketch-RNN based on [this paper](https://arxiv.org/pdf/1704.03477.pdf).
## Application Architecture:
* The web infrastructure technologies holding up the application and game server
### Technologies Used:
**Python-socketio**
* Allows for communication in two directions (server <-> client)
* Rooms for games

**Aiohttp/Asyncio**
* Enables asynchronous socket handlers and coroutines between client and server
* Switched to this after having a problem with handling synchronous handlers

**React front-end**

