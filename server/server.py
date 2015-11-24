from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

class MyServerProtocol(WebSocketServerProtocol):
    # Class variable to store connection data
    players_vec = []
    game_config = []

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        
    def onOpen(self):
        print("WebSocket connection open.")
        
    def onMessage(self, payload, isBinary):
        # Get the data
        data = json.loads(payload.decode('utf8'))
    
        # Waiting for players
        def waiting(data):
            if not self.game_config:
                self.game_config.append(data['playersSetup'])
            
            #Send the current players information
            self.sendMessage(json.dumps(self.players_vec, ensure_ascii = False).encode('utf8'), isBinary)
            
        # Player ask to join the game
        def want_to_play(data):
            # If we have game data and there is still room the other player 
            if self.game_config and (len(self.players_vec) < self.game_config[0]['maxPlayers']):
                game_setup = self.game_config[0]
                main_player = [i for i in self.players_vec if i['role'] == 'player']
                
                # Generate properties for the current player (main player or ghosts)
                name = data['name']
                if len(main_player) > 0:
                    # If the main player exists
                    color = game_setup['attributes'][len(self.players_vec)]['color']
                    role = game_setup['attributes'][len(self.players_vec)]['role']
                    position = len(self.players_vec)
                    # Reserve a position in the game for the player
                    self.players_vec.append({'color':color, 'role': role, 'name': name,'position': position, 'direction': 'left'})
                else:
                    # If don't, we know the main player data is in the first pos
                    color = game_setup['attributes'][0]['color']
                    role = game_setup['attributes'][0]['role']
                    position = 0
                    # Insert in the first position the player info
                    self.players_vec.insert(0, {'color':color, 'role': role, 'name': name,'position': position, 'direction': 'left'})

                # Send the assigned player info back
                self.sendMessage(json.dumps(self.players_vec[position], ensure_ascii = False).encode('utf8'), isBinary)
                            
        # Player send direction
        def direction(data):
            currentPlayer = self.players_vec[data['position']]
            currentPlayer['direction'] = data['direction']
        
        # Available messages types
        options = {
            'waiting' : waiting,
            'want-to-play' : want_to_play,
            'direction' : direction
        }
        
        # Launch the proper action
        options[data['action']](data)
                      
    def onClose(self, wasClean, code, reason):
        if code == 1000:
            # Remove data of player who close the connection
            if reason and self.players_vec:
                # 'reason' match with the 'position' list's attribute
                aux = [i for i in self.players_vec if i['position'] == int(reason)]
                self.players_vec.remove(aux[0])
        else:
            print 'Bad attempt to close the connection'
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys
    import random
    import json

    from twisted.python import log
    from twisted.internet import reactor
    from twisted.internet import task

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = MyServerProtocol

    reactor.listenTCP(9000, factory)
    reactor.run()