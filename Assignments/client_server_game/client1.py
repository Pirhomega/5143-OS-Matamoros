#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# Guessing Algorithm:
#   > Start with a possible high and low of 2147483647 and 0, respectively.
#   > The guess is ('high' + 'low') / 2
#       > If guess was too high, reduce value of 'high' to value of 'guess'
#       > If guess was too low, reduce value of 'low' to value of 'guess'
#   > Repeat
#   > If another client guesses the value before this one, the values of 'low'
#       and 'high' are reset and the guess begins anew


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
    low = 0
    high = 2147483647
    count = initial_count = 0
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        if count == 0:
            # calls signal on the mutex 
            connect_mutex(mutex, signal) == b'2'
        print("Sending guess to server!")
        guess = int((high + low) / 2)
        print("My guess is", guess)
        sock.sendall(bytes(str(guess), "ascii"))
        # I can do this without a while loop since I know
        # the server will only send less than 64 bytes back as a response
        message_back = sock.recv(64)
        sock.close()
        if message_back == b'-1':
            low = guess
            print("My guess was too low!")
        elif message_back == b'1':
            high = guess
            print("My guess was too high!")
        elif message_back == b'2':
            print("Dang! Someone got it first!")
            low = 0
            high = 2147483647
            initial_count = count
        elif message_back == b'0':
            print("I won!")
            print("It took", count - initial_count, "guesses to reach the correct answer")
            break
        else:
            print("Something broke.")
        count += 1
        # if count == 100:
        #     break

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