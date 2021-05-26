import os, re
import fManager as fm
import socket
import threading
from datetime import date
import json

# Пути для хранения логов и паролей. Пароли хранятся в открытом виде только для наглядности работы приложения
LOGS = "D:/study/2 курс/Практикум/4 семестр/ftp_server/logs.txt"
SECURE = "D:/study/2 курс/Практикум/4 семестр/ftp_server/sec.json"


class ThreadedServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.users = json.load(open(SECURE))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print(f"Подключился клиент {address}", file=open(LOGS, "a"))
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, conn, address):
        while True:
            data = conn.recv(1024).decode()
            if '<nick_check>' in data:
                user_nick = data.split('>=')[1]
                user_pass = data.split('>=')[2]

                # если нет такого логина - регистируем
                if user_nick not in self.users.keys():
                    self.users.setdefault(user_nick, user_pass)
                    json.dump(self.users, open("file_name.json", 'w'))
                    print(f"{date.today()} - Зарегистирован пользователь {user_nick}", file=open(LOGS, "a"))
                    conn.send('<nick_check_true>'.encode())
                    break

                # если зарегистрирован и пароль верный
                elif user_pass == self.users.get(user_nick):
                    print(f"{date.today()} - Пользователь {user_nick} вошёл в аккаунт", file=open(LOGS, "a"))
                    conn.send('<nick_check_true>'.encode())
                    break
                else:
                    print(f"{date.today()} - Неудачная попытка входа под пользователя {user_nick}",
                          file=open(LOGS, "a"))
                    conn.send('<nick_check_false>'.encode())
                    continue

        # получаем расположение папки, в которой будем создавать все папки пользователей
        with open('config.cfg', "r") as file:
            DIRECTORY = re.search(r'\"[^\"]*\"', file.read()).group().replace('"', '')
        os.chdir(DIRECTORY)

        try:
            # пытаемся создать папку с ником пользователя
            os.mkdir(user_nick)

        except:
            pass

        DIRECTORY = DIRECTORY + "\\" + user_nick

        # запоминаем домашнюю папку пользователя
        tm = DIRECTORY

        while True:
            # обработываем данные от клиента
            send_fl = False
            command = conn.recv(1024).decode()
            size = conn.recv(1024).decode()
            file = conn.recv(int(size))

            if command.split()[0] == "get_from_server":
                response = fm.manage(tm, DIRECTORY, command)
                # если получили ответ в байтах (файл) то отправляем клиенту
                if isinstance(response, (bytes, bytearray)):
                    conn.send(str(len(response)).encode())
                    conn.send(response)
                    continue
                else:
                    # иначе отправляем код ошибки
                    conn.send("-1".encode())
                    conn.send(response.encode())
                    continue

            print(f"{date.today()} - Запрос пользователя {user_nick} - {command}", file=open(LOGS, "a"))
            if file:
                response = fm.manage(tm, DIRECTORY, command, file)
            else:
                response = fm.manage(tm, DIRECTORY, command)

            if not response:
                response = "ok"

            conn.send(response.encode())
            DIRECTORY = fm.inp_check()
            
            # передаём текущуюю директорию пользователя
            conn.send(f"{DIRECTORY.replace(tm, '~$')}: ".encode())


if __name__ == "__main__":
    port_num = 6666
    ThreadedServer('', port_num).listen()
