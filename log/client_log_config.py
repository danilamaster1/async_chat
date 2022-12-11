import logging

log = logging.getLogger('client')

logging.basicConfig(filename='client_log.log',
                    encoding='utf-8',
                    format="%(asctime)s %(levelname)s %(module)s %(message)s",
                    level=logging.INFO)





