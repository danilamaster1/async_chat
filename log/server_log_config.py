import logging

log = logging.getLogger('server')

logging.basicConfig(filename='server_log.log',
                    encoding='utf-8',
                    format="%(asctime)s %(levelname)s %(module)s %(message)s",
                    level=logging.INFO)


