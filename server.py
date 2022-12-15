import socket
import json
import sys
import logging
sys.path.append('common')
sys.path.append('log')
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP_ADDRESS
from common.utils import get_message, send_message
import log.server_log_config

logs = logging.getLogger('server')


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE : 200}
    return {
        RESPONSE : 400,
        ERROR : 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port > 65535 or listen_port < 1024:
            raise ValueError
    except ValueError:
        logs.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = DEFAULT_IP_ADDRESS
    except IndexError:
        logs.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        transport.bind((listen_address, listen_port))
    except socket.gaierror:
        logs.error('Неправильный ip-address')
        sys.exit(1)

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            logs.error('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
