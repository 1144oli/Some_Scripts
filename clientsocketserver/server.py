import threading
import socket
from colorama import Fore, Style, init as colorama_init
import hashlib

colorama_init()

host = '192.168.244.1'  # host
port = 37508

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def generate_color(username):
    hash_object = hashlib.sha256(username.encode())
    hex_dig = hash_object.hexdigest()
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    index = int(hex_dig, 16) % len(colors)
    return colors[index]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            decoded_message = message.decode('ascii')
            if decoded_message.startswith('/kick '):
                if nicknames[clients.index(client)] == 'admin':  # Check if the user is admin
                    nickname_to_kick = decoded_message.split(' ')[1]
                    kick(nickname_to_kick)
                else:
                    client.send("You don't have permission to use this command.".encode('ascii'))
            else:
                nickname = nicknames[clients.index(client)]
                broadcast_message = f'{nickname}: {decoded_message}'
                print(broadcast_message)
                broadcast(broadcast_message.encode('ascii'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick(nickname_to_kick):
    if nickname_to_kick in nicknames:
        index = nicknames.index(nickname_to_kick)
        client_to_kick = clients[index]
        client_to_kick.send("You've been kicked by the admin.".encode('ascii'))
        client_to_kick.close()
        clients.remove(client_to_kick)
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast(f'{nickname} has been kicked from the chat!'.encode('ascii'))

def colored_print(message, color=Fore.WHITE):
    print(f"{color}{message}{Style.RESET_ALL}")

def console_input():
    while True:
        command = input(Fore.CYAN + "Enter command (kick {nickname}): " + Style.RESET_ALL)
        if command.startswith('kick '):
            nickname_to_kick = command.split(' ')[1]
            kick(nickname_to_kick)
        else:
            colored_print("Invalid command.", Fore.RED)

colored_print(Fore.GREEN + "Server is listening..." + Style.RESET_ALL)
threading.Thread(target=receive).start()
threading.Thread(target=console_input).start()
