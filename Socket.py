import asyncio
from socket import socket, AF_INET, SOCK_STREAM

class Socket():
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.main_loop = asyncio.new_event_loop()
  
    # так как данные у нас всегда будут на сервере, но
    # data клиента берётся из input, то ставим
    # по умолчанию None
    async def send_data(self, data=None):
        raise NotImplementedError()
    
    # то же скамое и с прослушкой сокета
    async def listen_socket(self, listened_socket=None):
        raise NotImplementedError()

    async def main(self):
        raise NotImplementedError()

    def start(self):
        self.main_loop.run_until_complete(self.main())
    
    def set_up(self):
        raise NotImplementedError()

