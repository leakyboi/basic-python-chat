#!/usr/bin/env python3
"""Some setup stuff.""" # In an effort to be unclear about what code does what, we decided to constantly use the word "stuff"
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections(): # This seems like safe code, no issue here
    """sets up the actual server..""" # This might be useful
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has joined the chatroom." % client_address)
        client.send(bytes("Greetings from the wierd place. Now type your name and press enter! Or else...", "utf8")) # Leave threatening message
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """client connection stuff (ONLY HANDLES ONE!).""" # We think we need to use the word "stuff" as much as possible. Hence this "stuff"

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name # Don't quit now!
    client.send(bytes(welcome, "utf8"))
    msg = "%s has sadly joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close() # I hated you anyway, client
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8")) # The maze wasn't meant for you
            break # ~ R E L A X ~ T A K E ~ A ~ L O A D  ~ O F F ~


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients.""" 

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = '127.0.0.1' # Host on localhost to start
PORT = 6969 # ...So anyway we fired the dev that added the port number
BUFSIZ = 1024 # Buffersize. For stuff
ADDR = (HOST, PORT) # This is the address we use

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # You shall bind to this address or perish!

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...") # We need to add in some more useless print statments, so we used this one here
    ACCEPT_THREAD = Thread(target=accept_incoming_connections) # We accept you incoming connections!
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close() # We didn't need to server anyway, servers are overrated
