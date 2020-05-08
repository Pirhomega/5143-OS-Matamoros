#!C:/Users/Owner/AppData/Local/Programs/Python/Python37/python.exe
import socket, queue, random, types, time

# this class will hold all functionality to provide locks to clients who
# call 'wait' on it if the mutex is 1, switching it to 0. If 'signal' is called, the mutex will 
# switch back to 1, indicating the caller has finished with the lock. 
class Mutex:
    def __init__(self, bindto=(), num_conns=1):
        # sets the server up, binds it to the indicated address from main, and 
        # sets it to listen for as many as 'num_comms' connections
        self.mutex = 1
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(bindto)
        self.server.listen(num_conns)
        self.data = types.SimpleNamespace(addr=bindto[0], outb=b'')
    
    # accept an incoming connection
    def accept(self):
        print('listening for incoming connections')
        # the server blocks here until it receives a connection from a client
        (connection, address) = self.server.accept()
        with connection:
            data = connection.recv(64)
            # if the client sends a 0, it is calling 'mutexWait'
            if data == b'0':
                print("Mutex said: It called WAIT. Sending a reply to", address)
                connection.sendall(self.mutexWait())
            # otherwise, it's calling 'mutexSignal'
            elif data == b'1':
                print("Mutex said: It called SIGNAL. Sending a reply to", address)
                connection.sendall(self.mutexSignal())
            # shutdown measures
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()

    # processes call this when they've finished using the resources the mutex guards
    # i.e. the lock can be released
    def mutexSignal(self):
        self.mutex = 1
        return b'2'

    # processes call this when they want to access a resource the mutex guards,
    # i.e. obtain a lock
    def mutexWait(self):
        # if the mutex is already 0, another client has a lock
        # The client making the 'wait' call must try again later
        if self.mutex == 0:
            return b'0'
        # if no one currently has a lock, the caller may obtain one
        else:
            self.mutex = 0
            return b'1'

###############################################################################################
#                                        MAIN                                                 #
###############################################################################################
# creates the server object with the ability to handle three connections
mutex_object = Mutex( ('localhost', 8080), 1 )
try:
    while True:
        mutex_object.accept()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    print("All done.")