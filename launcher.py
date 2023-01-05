"""Программа-лаунчер"""

import subprocess

PROCESSES = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESSES.append(subprocess.Popen('python server.py',
                                          shell=True))
        try:
            count = int(input('Сколько клиентов запустить?: '))
        except ValueError:
            print('Не число, запуск 1 клиента')
            PROCESSES.append(subprocess.Popen('python client.py -n test1', shell=True))
        else:
            for i in range(count):
                PROCESSES.append(subprocess.Popen(f'python client.py -n test{i+1}', shell=True))
    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
