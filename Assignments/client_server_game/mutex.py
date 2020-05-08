#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe
import socket, queue, random, types

class Mutex:
    def __init__(self, bindto=(), num_conns=1):
        self.mutex = 1
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(bindto)
        self.server.listen(num_conns)
        self.data = types.SimpleNamespace(addr=bindto[0], outb=b'')
    
    # accept an incoming connection
    def accept(self):
        print("Mutex said: Waiting for connections!")

        # the server blocks here until it receives a connection from a client
        (connection, self.data.addr) = self.server.accept()

        print("Mutex said: Got a connection from", self.data.addr)
        # add the client connection to the dictionary for safe-keeping
        # self.conn_list[client_address] = connection
        with connection:
            while True:
                data = connection.recv(64)
                if data == b'':
                    print("breaking")
                    break
                self.data.outb += data
            print("Mutex said: Received a message from", self.data.addr)
            print("Mutex said: Message now states:", self.data.outb)
            # if the client sends a 0, it is calling 'mutexWait'
            if self.data.outb == b'0':
                print("Mutex said: It called WAIT. Sending a reply to", self.data.addr)
                connection.sendall(self.mutexWait())
            # otherwise, it's calling 'mutexSignal'
            elif self.data.outb == b'1':
                print("Mutex said: It called SIGNAL. Sending a reply to", self.data.addr)
                connection.sendall(self.mutexSignal())
            print("Mutex said: Sent!")
            # shutdown measures
            self.data.outb = b''
            print("Shuttin' down.")
            connection.shutdown(socket.SHUT_WR)

    # processes call this when they've finished using the resources the mutex guards
    def mutexSignal(self):
        self.mutex = 1
        return b'2'

    # processes call this when they want to access a resource the mutex guards
    # Calls to mutexWait must pass the socket object of the client trying to connect
    def mutexWait(self):
        if self.mutex == 0:
            return b'0'
        else:
            self.mutex = 0
            return b'1'

###############################################################################################
#                                        MAIN                                                 #
###############################################################################################

mutex_object = Mutex( ('localhost', 8080), 1 )
try:
    while True:
        print("And again")
        mutex_object.accept()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    print("All done.")