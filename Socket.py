"""
    начнём всё переписывать на ооп
    сделаем родительский класс сокета для клиента и для сервера
    зачем?
    1) Безопасно. Нет глобальных переменных
    2) DRY. У клиента и сервера много общего -- функции прослушивания, отправки, один протокол
"""
from socket import socket, AF_INET, SOCK_STREAM

class Socket(socket):
    def __init__(self):
        # всё равно, что мы делали socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super(Socket, self).__init__(AF_INET,
                                     SOCK_STREAM)
    def send_data(self):
        # проектируем метод для реализации в других классах (абстракция)
        raise NotImplementedError()

    def listen_socket(self):
        # проектируем метод для реализации в других классах (абстракция)
        raise NotImplementedError()
    
    # соединение 
    def set_up(self):
        raise NotImplementedError()



