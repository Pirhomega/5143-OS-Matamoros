#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# Guessing Algorithm:
#   > Start at 1 and double the guess
#       > If guess is too low, double the guess and repeat
#       > If guess is too high, reduce the guess
#           > Take the sum of the previous guess and the current guess, and divide by two
#               > If guess is too high, repeat
#               > If guess is too low, increment guess by 1 until guess is correct


import queue, socket, time, types

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
    guess = prev = 1
    increase = True
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        if count == 0:
            # calls signal on the mutex 
            connect_mutex(mutex, signal) == b'2'
        sock.sendall(bytes(str(guess), "ascii"))
        message_back = sock.recv(64)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        if message_back == b'-1':
            # double guess until guess is too high
            if increase:
                guess *= 2
            # if 'increase' is False, that means we can not increase our guess
            # by multiplying it by two. That would put the guess too high.
            # Therefore, just increment. 
            else:
                guess += 1
        elif message_back == b'1':
            # only define 'prev' once, otherwise the algorithm will not work
            if increase:
                prev = guess
                increase = False
            guess = int((guess + prev)/2)
        elif message_back == b'2':
            print("client3 was too late")
            guess = prev = 0
            initial_count = count
        elif message_back == b'0':
            print("client3 got it")
            print("It took", count - initial_count, "guesses to reach the correct answer")
            break
        else:
            print("client3 broke.")
        count += 1

# 'mutex' and 'server' are the addresses
# 'mutex' holds the mutex class that will govern access to the server, while
# 'server' will handle the random number generation and the guesses
mutex = ('127.0.0.1', 8080)
server = ('127.0.0.1', 6060)
wait = b'0'
signal = b'1'
counter = 0
# this outer loop will control the entire client side,
# keeping the client-server game running until the user stops it
while counter < 5:
    # connect to the mutex to get permission to connect to the server
    mutex_response = connect_mutex(mutex, wait)
    # obtained a lock and can proceed to connect to the 'server'
    if mutex_response == b'1':
        # try to connect to the server
        connect_server(server, signal)
        print('client3 will start guessing')
    else:
        # another client has a lock, so this client must wait
        print("client3 must wait")
    time.sleep(1)
    counter += 1
time.sleep(10)