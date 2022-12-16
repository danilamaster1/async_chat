"""
Формат данных для общения --> JSON
"""

import socket
import sys
import json
import time
import logging
import inspect
sys.path.append('common')
sys.path.append('log')
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
import log.client_log_config
from functools import wraps

logs = logging.getLogger('client')


def decor_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        outer_func = inspect.stack()[1][3]
        logs.info(f'Функция {func.__name__} вызвана из функции {outer_func}')
        r = func(*args, **kwargs)
        return r
    return wrapper


@decor_log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


@decor_log
def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port > 65535 or server_port < 1024:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        logs.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        transport.connect((server_address, server_port))
    except ConnectionRefusedError:
        logs.error('Сервер не найден.')
        sys.exit(1)

    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        logs.error('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
