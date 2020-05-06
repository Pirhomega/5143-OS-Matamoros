#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# the client will try to connect to the server by checking if a semaphore/mutex says
# the server is available. Multiple clients could be checking that mutex simulateously.
# The instant the mutex "turns green", the first client to notice claims the mutex, which
# turn it red again; no client is allowed to connect to the server until the client who
# noticed green first has connected to the server. ONce a client has connected, it can
# start the guessing game.

import queue, socket, time

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    # while True:
    print("Client said: Let's see if I can connect!")
    sock.connect(server_address)
    try:
        print("Client said: Connected!")
        print("Client said: Sending a message to the server")
        sock.sendall(b'1')
        print("Client said: Sent!")
        data = sock.recv(64)
        if data == b'0':
            print("Aw... Server said:", data)
        elif data == b'1':
            print("Yay! Server said:", data)
        else:
            print("And we start over!")
    finally:
        print("Client said: Closing connection")
        sock.close()

