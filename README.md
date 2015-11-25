Prototype Pacman SERVER
=======================

Python server to support [prototypePacman](https://github.com/jvalen/prototypePacman) multiplayer and machine learning modes.


## Install:

``` bash
python-twisted module
```

``` bash
pip install autobahn
```

## Run server

``` bash
$ python server.py
```

## Multiplayer mode

All players will play in the same screen where [prototypePacman](https://github.com/jvalen/prototypePacman) game will be running, they will control their avatar with his/her own device (cell-phone, computer or any other device which has a web browser) with [d-pad](https://github.com/jvalen/d-pad).

## Machine learning mode


Define **onOpen** method to send the first message to [prototypePacman](https://github.com/jvalen/prototypePacman) and start the communication.
```python
def onOpen(self):

```

Also define **ml_direction** method, saying what to do when a message is received. e.g:  

```python

def  ml_direction(data):
          newDirection = random.choice(['up', 'down', 'left', 'right'])
          payload = newDirection.encode('utf8')
          self.sendMessage(json.dumps(payload, ensure_ascii = False).encode('utf8'), isBinary = False)
```

NOTE: In this mode, the game update is synchronous, meaning the game logic will be only updated when it receives a message from the [prototypePacman-server](https://github.com/jvalen/prototypePacman-server) 


