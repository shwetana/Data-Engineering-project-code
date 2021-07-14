from API_call_code import StockData
from kafka_producer import MyKafka
import logging
import time
import config
from logging.config import dictConfig

class Main:

    def __init__(self):
        logging_config = dict(
            version=1,
            formatters={
                'f': {'format':
                          '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
            },
            handlers={
                'h': {'class': 'logging.StreamHandler',
                      'formatter': 'f',
                      'level': logging.DEBUG}
            },
            root={
                'handlers': ['h'],
                'level': logging.DEBUG,
            },
        )

        self.logger = logging.getLogger()
        dictConfig(logging_config)
        self.logger.info("Initializing Kafka Producer")
        self.logger.info("KAFKA_BROKERS={0}".format(config.kafka_broker))
        self.mykafka = MyKafka(config.kafka_broker)

    def init_stock(self):
        self.stocks5 = StockData()
        self.logger.info(f'StockData Starts Polling Initialized')

    def run(self):
        self.init_stock()
        start_time = time.time()
        for i in range(len(config.list_cmp)):
            data = self.stocks.get_data(config.list_cmp[i], config.function[1])
            self.logger.info(f'Successfully polled Stock data for daily')
            self.mykafka.send_data(config.topic[1], data, config.list_cmp[i],0)
            self.logger.info(f'Published stock data to Kafka for daily')
            time.sleep(15)

if __name__ == "__main__":
    logging.info("Initializing stock Starts Polling")
    main = Main()
    main.run()