#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe

# The server's job is to randomly generate a number between two other randomly generated numbers.
# The server's ports are always open but guarded by a mutex sitting in another process. If a client
# is trying to connect, the server will do so and trade messages with it (figure that out later). 
# If the client guesses the correct number the server randomly generated, the client will disconnect.

import socket, queue, random, types, selectors, time

class Server:
    def __init__(self, bindto=(), num_conns=1):
        # self.sel = selectors.DefaultSelector()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(bindto)
        self.server.listen(num_conns)
        # self.server.setblocking(False)
        # self.sel.register(self.server, selectors.EVENT_READ, data=None)

        self.data = types.SimpleNamespace(addr=bindto[0], outb=b'')
        self.value = self.decide_value()
        self.guessed = True
        self.count = 0
        self.response = b''
        print(self.value)
    
    # accept an incoming connection
    def accept(self):
        # events = self.sel.select(timeout=None)
        # for key, mask in events:
        #     if key.data is None:
        #         self.accept_wrapper(key.fileobj)
        #     else:
        #         self.service_connection(key, mask)
        print("Server said: Waiting for connections!")
        (connection, self.data.addr) = self.server.accept()
        print("Server said: Got a connection from", self.data.addr)
        # add the client connection to the dictionary for safe-keeping
        # self.conn_list[client_address] = connection
        with connection:
            # while True:
            print("Time to receive data!")
            self.data.outb = connection.recv(64)
            # if data == b'':
            #     print("No more data!")
            #     break
            # self.data.outb += data
            print("Server said: Sending a reply to", self.data.addr)
            if not self.guessed or self.count == 2:
                self.compare_number(int(self.data.outb))
                self.guessed = False
                self.count = 0
            else:
                print("Resetting them all because someone guessed correctly.")
                print(self.count)
                time.sleep(3)
                self.count += 1
                self.response = b'2'
            connection.sendall(self.response)
            # shutdown measures
            self.data.outb = b''

    def decide_value(self):
        low = random.randint(0, 2147483646)
        high = random.randint(low, 2147483647)
        # returns a random value between two randomly chosen values (low, high)
        return random.randint(low, high)
    
    def compare_number(self, number=int):
        if number < self.value:
            self.response = b'-1'
        elif number > self.value:
            self.response = b'1'
        else:
            self.response = b'0'
            # choose another number for clients to guess
            self.value = self.decide_value()
            print(self.value)

###############################################################################################
#                                        MAIN                                                 #
###############################################################################################

server_object = Server( ('localhost', 6060), 3 )
try:
    while True:
        print("And again")
        server_object.accept()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    print("All done.")