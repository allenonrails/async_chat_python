import asyncio

from os import system
from Socket import Socket
from datetime import datetime
from settings import SERVER_IP, SERVER_PORT

class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()
        # сообщения, которые отправляем
        self.messages = ""

    def set_up(self, ip: str, port: int):
        # если подключения к серверу нет -- заканчиваем программу
        try:
            self.socket.connect((ip, port))
        except ConnectionRefusedError:
            print("Server is not online right now :(")
            exit(0)
                
        self.socket.setblocking(False)

        # убираем threads

    async def listen_socket(self, listened_socket: object =None):
        while True:
            # снова принятие данных делаем асинхронно
            data = await self.main_loop.sock_recv(self.socket, 2048) 
            
            # шлём дату перед сообщением, когда оно было отправлено
            self.messages += f"{datetime.now().date()}: {data.decode('utf-8')}\n"
            
            # очищаем экран, чтобы не дублировать написанное сообщение
            system('cls')
            
            # теперь шлём сообщение 
            print(self.messages)

    async def send_data(self, data=None):
        while True:
            # что же делать с функцией input? 
            # ведь он полностью стопит всё и какой аналог есть в asyncio
            # к сожалению здорового аналога ему, поэтому мы просто
            # запустим поток с asyncio
            data = await self.main_loop.run_in_executor(None, input, ">>> ")
            # и так же 
            # асинхронный send с asyncio
            await self.main_loop.sock_sendall(self.socket, data.encode("utf-8"))

    async def main(self):
        # одновременно await 2 таска
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket()),
            self.main_loop.create_task(self.send_data())
        )


if __name__ == "__main__":
    client = Client()
    client.set_up(SERVER_IP, SERVER_PORT)

    # запуск сокета (main loop)
    client.start()

