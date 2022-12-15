"""
Формат данных для общения --> JSON
"""

import socket
import sys
import json
import time
import logging
sys.path.append('common')
sys.path.append('log')
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
import log.client_log_config

logs = logging.getLogger('client')


def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


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
        logs.error('Сервер не найден')
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
