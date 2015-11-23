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
            if self.game_config:
                # Generate properties for the current player
                game_setup = self.game_config[0]
                color = game_setup[len(self.players_vec)]['color']
                role = game_setup[len(self.players_vec)]['role']
                name = data['name']
                position = len(self.players_vec)

                # Reserve a position in the game for the player
                self.players_vec.append({'color':color, 'role': role, 'name': name,'position': position, 'direction': 'left'})

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
        if reason:
            print int(reason)
            del self.players_vec[int(reason)]
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