#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# Guessing Algorithm:
#   > Start with a possible high and low of 2147483647 and 0, respectively.
#   > The guess is ('high' + 'low') / 2
#       > If guess was too high, reduce value of 'high' to value of 'guess'
#       > If guess was too low, reduce value of 'low' to value of 'guess'
#   > Repeat
#   > If another client guesses the value before this one, the values of 'low'
#       and 'high' are reset and the guess begins anew


import socket, time

# this function will connect to the 'mutex' server
# The 'mutex' will return either a b'0', b'1', or b'2'
def connect_mutex(address=(),message=b''):
    message_back = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # print("Client said: Let's see if I can connect!")
        sock.connect(address)
        # print("Client said: Connected!")
        # print("Client said: Sending a message to the Mutex")
        sock.sendall(message)
        sock.shutdown(socket.SHUT_WR)
        # print("Client said: Sent!")
        while True:
            # print("Still data left")
            data = sock.recv(64)
            if data == b'':
                # print("breaking")
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
    low = 0
    high = 2147483647
    count = initial_count = 0
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        if count == 0:
            # calls signal on the mutex 
            connect_mutex(mutex, signal) == b'2'
        # calculate the guess
        guess = int((high + low) / 2)
        sock.sendall(bytes(str(guess), "ascii"))
        message_back = sock.recv(64)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        # process the 'server's response
        if message_back == b'-1':
            low = guess
        elif message_back == b'1':
            high = guess
        # if another client had guessed the correct number before
        elif message_back == b'2':
            print("client1 was too late")
            low = 0
            high = 2147483647
            initial_count = count
        elif message_back == b'0':
            print("client1 guessed it")
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
        print('client1 will start guessing')
        connect_server(server, signal)
    else:
        # another client has a lock, so this client must wait
        print("client1 must wait")
    time.sleep(1)
    counter += 1
time.sleep(10)