# импортируем наш класс socket
from Socket import Socket
from threading import Thread

# импорт настроек
from settings import SERVER_IP, SERVER_PORT

# пишем класс сервера, который наследуется от нашего сокета 
class Server(Socket):
    def __init__(self):
        # создание сокета 
        super(Server, self).__init__()
        self.clients = []

    def set_up(self, ip: str, port: int):
        self.bind((ip, port))
        self.listen() 
        self.accept_sockets()
    
    def send_data(self, data: str) -> None:
        for client in self.clients: client.send(data)
    
    # тут передаём сокет, в клиенте не будем, поэтому None
    def listen_socket(self, listened_socket: object =None):
        while True:
            data = listened_socket.recv(2048)
            print(f"User sent {data}")
            self.send_data(data)

    def accept_sockets(self):
        while True:
            user_socket, address = self.accept() 
            print(f"{address[1]} connected")

            self.clients.append(user_socket)

            listen_accepted_client = Thread(target=self.listen_socket, args=(user_socket,))
            listen_accepted_client.start()

if __name__ == "__main__":
    server = Server()
    server.set_up(SERVER_IP, SERVER_PORT)

