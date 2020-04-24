# the client will try to connect to the server by checking if a semaphore/mutex says
# the server is available. Multiple clients could be checking that mutex simulateously.
# The instant the mutex "turns green", the first client to notice claims the mutex, which
# turn it red again; no client is allowed to connect to the server until the client who
# noticed green first has connected to the server. ONce a client has connected, it can
# start the guessing game.