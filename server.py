import socket

# чтобы работать со множеством потоков, нам нужна для этого библиотека
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 1234)) 
server.listen() 

# клиентов у нас может быть много, поэтому сделаем с ними список
clients = []

# функция, где мы будем слать сообщения всем пользователям
def send_all(data):
    # отправляем сообщения всем пользователям
    for client in clients: client.send(data)

# напишем функцию, что постоянно слушать информацию
def listen_client(client):
    # бесконечный цикл, чтобы всегда слушать клиента
    while True:
        # читаем 2048 байт за 1 пакет, не декодируем второй раз
        data = client.recv(2048)
        # давайте сделаем, когда дата приходит на сервер, такое сообщение
        print(f"User sent {data}")
        # прочитали дату и отправляем её всем пользователям (клиетам)
        send_all(data)

#теперь перепишем всё на функциях, чтобы было удобнее и понятнее
def start_server():
    while True:
        try:
            user_socket, address = server.accept() 
        except KeyboardInterrupt:
            server.close()
            break
        else:

            # делаем просто print
            print(f"{address[1]} connected")

            # добавляем пользователя сразу после подключения в наш список юзеров
            # чтобы потом каждому мы могли отправить сообщение от другого пользователя
            clients.append(user_socket)
            
            # запускаем поток в рамках конкретного клиента и передаём функцию для этого потока
            # listen_client, а вторым аргументом -- аргументы функции
            # ставим обязательно запятую, чтобы показать питону, что бы педераём именно список аргументов,
            # а не кортеж
            listen_accepted_client = Thread(target=listen_client, args=(user_socket,))
           
            # запуск потока
            listen_accepted_client.start()

            # прослушиваем подключенного клиента
            # listen_client(user_socket) # потом удалим

            # addres[1] == ip address подключённого клиента + немного упростим, 
        

# не забываем про когнструкцию name == main
if __name__ == "__main__":
    start_server()
