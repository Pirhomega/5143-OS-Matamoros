#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# the client will try to connect to the server by checking if a semaphore/mutex says
# the server is available. Multiple clients could be checking that mutex simulateously.
# The instant the mutex "turns green", the first client to notice claims the mutex, which
# turn it red again; no client is allowed to connect to the server until the client who
# noticed green first has connected to the server. ONce a client has connected, it can
# start the guessing game.

import queue, socket, time

class Mutex:
    def __init__(self):
        self.mutex = 1

    # processes call this when they've finished using the resources the mutex guards
    def mutexSignal(self):
        self.mutex = 1

    # processes call this when they want to access a resource the mutex guards
    # Calls to mutexWait must pass the socket object of the client trying to connect
    def mutexWait(self, sock_obj):
        if self.mutex == 0:
            print("Mutex said: Connection denied!")
            return False
        else:
            print("Mutex said: Connection approved!")
            self.mutex = 0
            return True

if __name__ == "__main__":
    mutex_test = Mutex()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    # while True:
    if not mutex_test.mutexWait(sock):
        print("Client said: I'm being blocked by the mutex!")
    else:
        print("Client said: I've been given permission to connect!")
        print("Client said: Let's see if I can connect!")
        sock.connect(server_address)
        print("Client said: Connected!")
        try:
            print("CLient said: Sending a message to the server")
            sock.sendall(b'Hi, server! Pls respond bb! I wuv you watts an\' watts uwu!')
            print("Server responded with: ", sock.recv(4096))
        finally:
            print("Client said: Closing connection")
            sock.close()

