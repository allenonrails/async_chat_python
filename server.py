import asyncio
from Socket import Socket

from settings import SERVER_IP, SERVER_PORT

class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        # теперь обращаемся по переменной класса
        self.clients = []

    def set_up(self, ip: str, port: int):
        self.socket.bind((ip, port))
        self.socket.listen()
        # устанавливаем сокет на неблокирующее состояние
        self.socket.setblocking(False)

        # по хорошему убираем accept_sockets, дабы
        # не нарушать принцип единственной ответственности
    
    # как и договаривались, делаем отправку данных асинронной
    async def send_data(self, data: str) -> None:
        # туt так же используем асинхронную
        # так как нужно дождаться, что данные успешно отправлены одному юзеру,
        # то я могу переходить к следующему, поэтому ставим await
        for client in self.clients: await self.main_loop.sendall(client, data)
    
    async def listen_socket(self, listened_socket: object =None):
        # если сокет не передан, то стопимся во избежание ошибок
        if not listened_socket: return

        while True:
            # recv тоже блокирующая функция, но, спасибо, asyncio уже изобрёл за нас
            # асинхронный вариант recv
            # 2 параметра
            #   сокет клиента
            #   количество принимаемых байт
            data = self.main_loop.sock_recv(listened_socket, 2048) 
            print(f"User sent {data}")
            
            # результат выполнения тут ждать хотим, поэтому await
            await self.send_data(data)

    async def accept_sockets(self):
        while True:
            # так как self.socket.accept будет постоянно ждать сокетов (нас это вряд ли устраивает)
            # мы будем делать другое -- брать готовый модуль от asyncio
            # работает почти так же, только работает асинхронно
            # то есть не создаёт очередь клиентов
            # Ну, и каждую асинхронную функцию нам нужно await, чтобы ждать её исполнения
            # так же мы передаём параметр -- наш сервер, так как он о нас не знает
            client_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"{address[1]} connected")

            self.clients.append(client_socket)
            # так же создаём таск на прослушку пользователя
            # await писать не нужно, так как ждать значений оттуда нам не надо
            # у нас там стоит while True и работать он будет всё равно, пока есть соединение
            self.main_loop.create_task(self.listen_socket(client_socket))

    # нужно написать глвный поток, который будет подключать другие задачи нашего сервера
    async def main(self):
        # пока задача какая-то выполняется мы не должны завершать наш main
        # поэтому создаём таск, чтобы не стопиться на других задачах
        # на каждую итерацию цикла в accpet_sockets будет создаваться новая задача
        # обязательно нужно ожидать удачного соедниния сокета
        await self.main_loop.create_task(self.accept_sockets())

if __name__ == "__main__":
    server = Server()
    server.set_up(SERVER_IP, SERVER_PORT)
    
    # запускаем главный поток
    server.start()

