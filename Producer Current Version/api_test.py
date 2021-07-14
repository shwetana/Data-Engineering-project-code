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
        self.stocks1 = StockData()
        self.stocks2 = StockData()
        self.stocks3 = StockData()
        self.stocks4 = StockData()
        self.logger.info(f'StockData Starts Polling Initialized')
    def run(self):
        self.init_stock()
        start_time = time.time()
        while True:
            data0 = self.stocks1.get_data(config.symbol[0])
            self.logger.info(f'Successfully polled Stock data for {config.symbol[0]}')
            self.mykafka.send_data(key=config.symbol[0], partition_num=0, json_data=data0)
            self.logger.info(f'Published stock data to Kafka for {config.symbol[0]}')
            data1 = self.stocks2.get_data(config.symbol[1])
            self.logger.info(f'Successfully polled Stock data for {config.symbol[1]}')
            self.mykafka.send_data(key=config.symbol[1], partition_num=1, json_data=data1)
            self.logger.info(f'Published stock data to Kafka for {config.symbol[1]}')
            data2 = self.stocks3.get_data(config.symbol[2])
            self.logger.info(f'Successfully polled Stock data for {config.symbol[2]}')
            self.mykafka.send_data(key=config.symbol[2], partition_num=2, json_data=data2)
            self.logger.info(f'Published stock data to Kafka for {config.symbol[2]}')
            data3 = self.stocks4.get_data(config.symbol[3])
            self.logger.info(f'Successfully polled Stock data for {config.symbol[3]}')
            self.mykafka.send_data(key=config.symbol[3], partition_num=3, json_data=data3)
            self.logger.info(f'Published stock data to Kafka for {config.symbol[3]}')
            # push data to kafka topic in every 60 min
            time.sleep(60.0 - ((time.time() - start_time) % 60.0))

if __name__ == "__main__":
    logging.info("Initializing stock Starts Polling")
    main = Main()
    main.run()