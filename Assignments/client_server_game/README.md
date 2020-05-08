## Client-Server Guessing Game
#### Operating Systems Spring 2020

#### Authors

| Name                                             | Email                     | Github Username |
| ------------------------------------------------ | ------------------------- | --------------- |
| [Corbin Matamoros](https://github.com/Pirhomega) | corbinmatamoros@yahoo.com | Pirhomega       |

#### Dates

None, I'm single.
Otherwise, **May 8th, 2020**

#### Contributions

| Name                                             | Email                     | Github Username |
| ------------------------------------------------ | ------------------------- | --------------- |
| [Corbin Matamoros](https://github.com/Pirhomega) | corbinmatamoros@yahoo.com | Pirhomega       |

#### Instructions

1. Make sure you have Python 3 installed. I programmed in Python 3.7.5

2. To start the mutex and server classes, navigate to the directory they are in and run `./server.py; ./mutex.py`

3. To start the game, from that same directory, run `./client1.py; ./client2.py; ./client3.py`

4. Once client1 wins, close the server and mutex windows and wait about a minute before running again

#### Platform developed on

Windows 10 Education, Version 1909, Build 18363.778

#### Known issues and flaws

Unfortunately, the only way I could get clients to submit guesses to the server was to create a new socket for every guess. For `client1.py`, this isn't a big deal since it runs a binary algorithm, creating < 100 sockets. However, for `client2.py` and `client3.py` which use linear algorithms, your computer will run out of available ports before they can guess a value, crashing both. There is an option to bind a client to an previously-used address so I wouldn't have to create a new port, but that does not work if you connect that reused port to the same remote location (you'd have to connect it to a different server). The alternative is to have the client always close any connections with a remote connection first, before the server closes it; however, I could not get that to work either.

#### Directory Structure

```txt
/client_server_game
├── README.md
├── client1.py
├── client2.py
├── client3.py
├── server.py
├── mutex.py
```
