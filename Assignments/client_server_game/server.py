#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

import socket, queue, random, types, selectors, time

# This class will hold all functionality for the server to generate a random number,
# between a randomly generated range, handle connections from clients, and respond to
# client guesses of that randomize number sent over a network
class Server:
    def __init__(self, bindto=(), num_conns=1):
        # sets the server up, binds it to the indicated address from main, and 
        # sets it to listen for as many as 'num_comms' connections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(bindto)
        self.server.listen(num_conns)

        # self.data = types.SimpleNamespace(addr=bindto[0], outb=b'')
        self.value = self.decide_value()
        self.guessed = False
        self.count = 0
        self.response = b''
        print(self.value)
    
    # accept an incoming connection
    def accept(self):
        print('listening for incoming connections')
        (connection, _) = self.server.accept()
        with connection:
            # receive the data coming in from a client
            data = connection.recv(64)
            # if the random number has not been guessed yet OR
            # all clients have been notified the correct guess has been made
            if not self.guessed or self.count == 2:
                self.guessed = False
                self.count = 0
                # compare the guess from the client with the actual number
                self.compare_number(int(data))
            else:
                # if the random number has been correctly guessed
                self.count += 1
                # clients know this response indicates the value has been guessed
                # and a new value must be determined
                self.response = b'2'
            # send response to the client
            connection.sendall(self.response)
            # shutdown measures
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()

    # funtion that determines the random value to be guessed
    def decide_value(self):
        low = random.randint(0, 2147483646)
        high = random.randint(low, 2147483647)
        # returns a random value between two randomly chosen values (low, high)
        return random.randint(low, high)
    
    # compares a client's guess with the randomized number
    def compare_number(self, number=int):
        # if too low
        if number < self.value:
            self.response = b'-1'
        # if too high
        elif number > self.value:
            self.response = b'1'
        # if spot on the money
        else:
            self.response = b'0'
            # choose another number for clients to guess
            self.value = self.decide_value()
            self.guessed = True
            # prints the new number to guess
            print(self.value)

###############################################################################################
#                                        MAIN                                                 #
###############################################################################################
# creates the server object with the ability to handle three connections
server_object = Server( ('localhost', 6060), 3 )
try:
    # runs the server indefinitely
    while True:
        server_object.accept()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    print("All done.")