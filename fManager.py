import os
import shutil
import shlex


def check_direct(tm, dir):
    if tm in dir:
        return True
    else:
        print('Доступ только к рабочему каталогу!')
        return False


def send_to_server(name, b_file):
    with open(name.split("\\")[-1], "wb") as f:
        f.write(b_file)


def get_from_server(dir):
    with open(dir, 'rb') as f:
        b_file = f.read()
    return b_file


def crtdir(dir):
    os.mkdir(dir)


def lsdir(dir):
    dir_list = os.listdir(dir)
    res = ', '.join(dir_list)
    return res


def rmvdir(dir):
    shutil.rmtree(dir)


def swapdir(dir):
    os.chdir(dir)


def crtfile(dir):
    open(dir, 'a').close()


def readfile(dir):
    with open(dir, "r") as file:
        file_contents = file.read()
        return file_contents


def rmvfile(dir):
    os.remove(dir)


def cpyfile(dir1, dir2):
    shutil.copy2(dir1, dir2)


def movefile(dir1, dir2):
    shutil.move(dir1, dir2)


def renamefile(dir1, dir2):
    os.rename(dir1, dir2)


def inp_check():
    return os.getcwd()


def manage(tm, DIRECTORY, inp, file=b''):
    os.chdir(DIRECTORY)
    spl_inp = shlex.split(inp)

    if spl_inp[0] in ["crtdir", "rmvdir", "swapdir", "crtfile", "lsdir", "readfile", "rmvfile"]:
        abs_src_path = os.path.abspath(spl_inp[1])
        if check_direct(tm, abs_src_path):
            try:
                return functions[spl_inp[0]](abs_src_path)
            except FileNotFoundError:
                return 'Проверьте корректность введённого пути или названия файла :('
        else:
            return 'У Вас нет доступа к этому файлу или папке'

    elif spl_inp[0] == 'send_to_server':
        spl_inp = shlex.split(inp)
        abs_src_path = os.path.abspath(spl_inp[1])
        if check_direct(tm, abs_src_path):
            try:
                return functions[spl_inp[0]](spl_inp[1], file)
            except:
                return 'Ошибка! Проверьте правильность введённых данных'
        else:
            return 'У Вас нет доступа к этому файлу или папке'

    elif spl_inp[0] == 'get_from_server':
        spl_inp = shlex.split(inp)
        abs_src_path = os.path.abspath(spl_inp[1])
        if check_direct(tm, abs_src_path):
            try:
                return functions[spl_inp[0]](spl_inp[1])
            except:
                return 'Ошибка! Проверьте правильность введённых данных'
        else:
            return 'У Вас нет доступа к этому файлу или папке'

    elif spl_inp[0] in ["cpyfile", "movefile", "renamefile"]:
        abs_src_path = os.path.abspath(spl_inp[1])
        abs_dst_path = os.path.abspath(spl_inp[2])
        if check_direct(tm, abs_src_path) and check_direct(tm, abs_dst_path):
            try:
                functions[spl_inp[0]](abs_src_path, abs_dst_path)
            except FileNotFoundError:
                return 'Проверьте корректность введённого пути или названия файла :('
        else:
            return 'У Вас нет доступа к этому файлу или папке'

    else:
        return 'Такой команды не существует!'


functions = {"crtdir": crtdir, "rmvdir": rmvdir, "swapdir": swapdir, "crtfile": crtfile, "lsdir": lsdir,
             "readfile": readfile,
             "rmvfile": rmvfile, "cpyfile": cpyfile, "movefile": movefile, "renamefile": renamefile,
             "send_to_server": send_to_server,
             "get_from_server": get_from_server}
