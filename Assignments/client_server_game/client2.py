#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# Guessing Algorithm:
#   > Linear, starting from 0 and increasing to 2147483647
# This client is rigged for failure. If run solo, it will crash since all available ports
# will have been used and are now stuck in TIME_WAIT until the OS closes them.

import socket, time

# this function will connect to the 'mutex' server
# The 'mutex' will return either a b'0', b'1', or b'2'
def connect_mutex(address=(),message=b''):
    message_back = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(address)
        sock.sendall(message)
        sock.shutdown(socket.SHUT_WR)
        while True:
            data = sock.recv(64)
            if data == b'':
                break
            message_back += data
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        return message_back

# this function will connect to the 'server' to start guessing
# the random number using the algorithm describe at the top of this
# script. 
# Each guess is initiated by creating a socket to connect to the 'server' with.
# I did this because Python or something else wouldn't let me bind the client to a port
# and just reuse the port.          
def connect_server(address=(), message=b''):
    count = initial_count = 0
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        if count == 0:
            # calls signal on the mutex 
            connect_mutex(mutex, signal) == b'2'
        sock.sendall(bytes(str(count), "ascii"))
        message_back = sock.recv(64)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        # process the 'server's response
        # There are no if statements for the 'server' responses
        #   b'-1' and b'1' since it doesn't matter if our guess is too high or low
        #   The algorithm is linear and will eventually traverse all values between zero
        #   and 2147483647.
        if message_back == b'2':
            print("client2 was too late")
            initial_count = count
        elif message_back == b'0':
            print("client2 got it")
            print("It took", count - initial_count, "guesses to reach the correct answer")
            break
        count += 1

# 'mutex' and 'server' are the addresses
# 'mutex' holds the mutex class that will govern access to the server, while
# 'server' will handle the random number generation and the guesses
mutex = ('127.0.0.1', 8080)
server = ('127.0.0.1', 6060)
# 'wait' and 'signal' are calls to the mutex
wait = b'0'
signal = b'1'
counter = 0
# this outer loop will control the entire client side,
# keeping the client-server game running for five numbers
while counter < 5:
    # connect to the mutex to get permission to connect to the server
    mutex_response = connect_mutex(mutex, wait)
    # obtained a lock and can proceed to connect to the 'server'
    if mutex_response == b'1':
        # try to connect to the server
        print('client2 will start guessing')
        connect_server(server, signal)
    else:
        # another client has a lock, so this client must wait
        print("client2 must wait")
    time.sleep(1)
    counter += 1
time.sleep(10)