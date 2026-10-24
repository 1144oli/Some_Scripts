import socket
import threading
from colorama import Fore, Style, init as colorama_init
import hashlib

colorama_init()

nickname = input(Fore.YELLOW + "Choose a nickname: " + Style.RESET_ALL)

# Function to generate a color based on a string
def generate_color(username):
    hash_object = hashlib.sha256(username.encode())
    hex_dig = hash_object.hexdigest()
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    index = int(hex_dig, 16) % len(colors)
    return colors[index]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.244.1', 37508))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                parts = message.split(': ')
                if len(parts) >= 2:
                    username = parts[0]
                    content = ': '.join(parts[1:])
                    if username == nickname:
                        username = "You"
                    user_color = generate_color(username)
                    print(user_color + username + ": " + content + Style.RESET_ALL)
                else:
                    print(Fore.CYAN + message + Style.RESET_ALL)
        except:
            print(Fore.RED + "An error occurred!" + Style.RESET_ALL)
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        message = message.replace(f'{nickname}: ', 'You: ')
        client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
