#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# The server's job is to randomly generate a number between two other randomly generated numbers.
# The server's ports are always open but guarded by a mutex sitting in another process. If a client
# is trying to connect, the server will do so and trade messages with it (figure that out later). 
# If the client guesses the correct number the server randomly generated, the client will disconnect.

import socket, queue, random

class Server:
    def __init__(self, bindto=(), num_conns=1):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(bindto)
        self.server.listen(num_conns)
        self.guess_q = queue.Queue(0)
        self.conn_list = {}
        self.value = self.decide_value()
        print(self.value)
    
    # accept an incoming connection
    def accept(self):
        print("Server said: Waiting for connections!")
        (connection, client_address) = self.server.accept()
        print("Server said: Got a connection from", client_address)
        # add the client connection to the dictionary for safe-keeping
        # self.conn_list[client_address] = connection
        try:
            while True:
                data = connection.recv(4096)
                if data:
                    print("Server said: Received a message from", client_address)
                    print("Client said:", data)
                    print("Server said: Sending a reply to", client_address)
                    connection.sendall(b'owo i wan u so badly client-senpai')
                else:
                    break
        finally:
            print("Server said: Closing connection with", client_address)
            connection.close()
    
    def decide_value(self):
        low = random.randint(0, 2147483646)
        print("The low is:", low)
        high = random.randint(low, 2147483647)
        print("The high is:", high)
        # returns a random value between two randomly chosen values (low, high)
        return random.randint(low, high)

###############################################################################################
#                                        MAIN                                                 #
###############################################################################################

server_object = Server( ('localhost', 6060), 4 )
server_object.accept()