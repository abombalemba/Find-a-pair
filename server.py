import socket
from time import sleep
import brain
from settings import TIMER


HOST, PORT = '127.0.0.1', 6789


class Room:
    def __init__(self, uid: str = f'{HOST}:{PORT}', backlog: int = 4) -> None:
        self.uid, self.backlog = uid, backlog
        self.USERS = list()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(backlog)
        new = self.socket.accept()
        self.USERS.append(new)

    def accept(self, who: socket.socket = None) -> None:
        try:
            who.connect((HOST, PORT))
            self.USERS.append(self.socket.accept())
        except ConnectionRefusedError:
            print(124)

    def disconnect(self, who: socket.socket) -> None:
        try:
            who.shutdown(socket.SHUT_RDWR)
        except ConnectionRefusedError:
            print(125)

    def send(self, what: list) -> None:
        for user in self.USERS:
            self.socket.sendto(what, user[1])

    def users(self) -> None:
        for user in self.USERS:
            print(user)

    def delete(self) -> None:
        self.socket.close()


room = Room()

while True:
    try:
        data = '\n'.join([i[0].recv(1024).decode() for i in room.USERS]) + '\n'
        print(data)
    except KeyboardInterrupt:
        pass
    except OSError:
        print('нет подключения')
        room.accept()
    sleep(TIMER)

room.delete()
