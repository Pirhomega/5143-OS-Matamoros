#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# the client will try to connect to the server by checking if a semaphore/mutex says
# the server is available. Multiple clients could be checking that mutex simulateously.
# The instant the mutex "turns green", the first client to notice claims the mutex, which
# turn it red again; no client is allowed to connect to the server until the client who
# noticed green first has connected to the server. ONce a client has connected, it can
# start the guessing game.

import queue, socket, time, types

def connect_mutex(address=(),message=b''):
    message_back = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print("Client said: Let's see if I can connect!")
        sock.connect(address)
        print("Client said: Connected!")
        print("Client said: Sending a message to the Mutex")
        sock.sendall(message)
        sock.shutdown(socket.SHUT_WR)
        print("Client said: Sent!")
        while True:
            print("Still data left")
            data = sock.recv(64)
            if data == b'':
                print("breaking")
                break
            message_back += data
        return message_back
        
def connect_server(address=(), message=b''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(address)
        if connect_mutex(mutex, signal) == b'2':
            while True:
                # message_to = len(bytes(str(123123), "ascii"))
                # sock.sendall(message_to)
                sock.sendall(bytes(str(123123), "ascii"))
                # sock.shutdown(socket.SHUT_WR)
                # I can do this without a while loop since I know
                # the server will only send 1 byte back as a response
                message_back = sock.recv(64)
                if message_back == b'-1':
                    print("My guess was too low!")
                elif message_back == b'1':
                    print("My guess was too high!")
                elif message_back == b'2':
                    print("Dang! Someone got it first!")
                else:
                    print("I won!")
                    sock.close()
                    break
        else:
            print("Something went wrong.")

mutex = ('127.0.0.1', 8080)
server = ('127.0.0.1', 6060)
wait = b'0'
signal = b'1'
# this outer loop will control the entire client side,
# keeping the client-server game running until the user stops it
# while True:
    # connect to the mutex to get permission to connect to the server
mutex_response = connect_mutex(mutex, wait)
if mutex_response == b'1':
    # try to connect to the server
    connect_server(server, signal)
elif mutex_response == b'0':
    print("placeholder")
    # try again