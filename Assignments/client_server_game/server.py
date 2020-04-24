# The server's job is to randomly generate a number between two other randomly generated numbers.
# The server's ports are always open but guarded by a mutex sitting in another process. If a client
# is trying to connect, the server will do so and trade messages with it (figure that out later). 
# If the client guesses the correct number the server randomly generated, the client will disconnect.

import socket

class Mutex:
    # if self.mutex is 0, the resource it's guarding are blocked from use
    # if self.mutex is 1, the resources it's guarding is free to use
    def __init__(self):
        self.mutex = 0
    # processes call this when they've finished using the resources the mutex guards
    def mutexSignal(self):
        if self.mutex == 0:
            self.mutex = 1
            return True
        else:
            self.mutex == 1
            return True
    # processes call this when they want to access a resource the mutex guards
    def mutexWait(self):
        if self.mutex == 0:
            return False
        else:
            self.mutex == 1
            return True

# create the semaphore class object
semaphore = Mutex()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(3)

while True:
    (clientsocket, address) = server.accept()
