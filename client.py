import socket
import os

HOST = 'localhost'
PORT = 6666
sock = socket.socket()
sock.connect((HOST, PORT))
inp = "~$: "

try:
    os.mkdir("ftp_cl_downloads")
except:
    pass

# процесс регистрации и авторизации
while True:
    nickname_inp = input('Введите ник: ')
    pass_inp = input('Введите пароль: ')
    nickname = '<nick_check>=' + nickname_inp + ">=" + pass_inp
    sock.send(nickname.encode())
    data = sock.recv(1024)
    data = data.decode()
    if data == '<nick_check_true>':
        print(f'Ник успешно задан, добро пожаловать, {nickname_inp}')
        break
    elif data == '<nick_check_false>':
        print(f'Этот ник уже занят или Вы вводите неверный пароль для этой учётной записи')
        continue

while True:
    get_fl = False
    request = input(inp)
    # если мы хотм загрузить файл на сервер
    if "send_to_server" == request.split()[0]:
        try:
            with open(request.split()[1], 'rb') as f:
                file = f.read()
        except:
            print('Такого файла не существует!')
    else:
        file = b''
    # если хотим скачать с сервера
    if "get_from_server" == request.split()[0]:
        get_fl = True

    # отправляем сам запрос
    sock.send(request.encode())

    # отправляем размер файлы
    sock.send(str(len(file)).encode())

    # отправляем сам файл
    sock.send(file)

    # если хотим скачать с сервера
    if get_fl:
        # получаем размер файла
        size = sock.recv(1024).decode()
        # ошибка
        if size == "-1":
            print(sock.recv(1024).decode())
            continue
        # иначе получаем и сохраняем
        file = sock.recv(int(size))
        with open("ftp_cl_downloads\\"+request.split()[1].split("\\")[-1], "wb") as f:
            f.write(file)
        continue

    # печатаем ответ сервера
    response = sock.recv(1024).decode()
    if response != "ok":
        print(response)
    inp = sock.recv(1024).decode()

sock.close()