import asyncio
"""
    low-level - пишем библиотеки
    high-level - работаем с готовым
"""
from socket import socket, AF_INET, SOCK_STREAM

# сначала убираем наследование с класса Socket
# это нам поможет удобнее писать асинхронные функции
class Socket():
    """
        Почему send_data & listen_socket должны работать асинхронно?
        Потому что они работают по сути постоянно на каких-то пользователей.
        Если мы всё так и оставим, когда у нас один поток (main loop),
        то консоль снова зависнет. Поэтому мы делаем все функции асинхронными, которые
        тормозят работу программы, останавливаются и выполняются синхронно
    """
    def __init__(self):
        # так как убрали наследование, то объявим так
        self.socket = socket(AF_INET, SOCK_STREAM)
        # создаём один текущий поток
        self.main_loop = asyncio.get_event_loop()
   
    # делаем функцию асинхронной
    async def send_data(self):
        raise NotImplementedError()

    # делаем функцию асинхронной
    async def listen_socket(self):
        raise NotImplementedError()

    async def main(self):
        raise NotImplementedError()

    def start(self):
        self.main_loop.run_until_complete(self.main())
    
    def set_up(self):
        raise NotImplementedError()

