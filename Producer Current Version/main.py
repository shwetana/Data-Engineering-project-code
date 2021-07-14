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
        #self.stocks5 = StockData()
        self.logger.info(f'StockData Starts Polling Initialized')

    def run(self):
        self.init_stock()
        start_time = time.time()
        # for i in range(len(config.list_cmp)):
        #     data5 = self.stocks5.get_data(config.list_cmp[i], config.function[1])
        #     self.logger.info(f'Successfully polled Stock data for daily')
        #     self.mykafka.send_data(config.topic[1], data5, config.list_cmp[i],0)
        #     self.logger.info(f'Published stock data to Kafka for daily')
        #     time.sleep(30)

        while True:
            data1 = self.stocks1.get_data(config.symbol[0], config.function[0])
            self.logger.info(f'Successfully polled Stock data for {config.symbol[0]}')
            self.mykafka.send_data(config.topic[0], data1, config.symbol[0], 0)
            self.logger.info(f'Published stock data to Kafka for {config.symbol[0]}')
            
            data2 = self.stocks2.get_data(config.symbol[1], config.function[0])
            self.logger.info(f'Successfully polled Stock data for {config.symbol[1]}')
            self.mykafka.send_data(config.topic[0], data2, config.symbol[1], 1)
            self.logger.info(f'Published stock data to Kafka for {config.symbol[1]}')            
            
            data3 = self.stocks3.get_data(config.symbol[2], config.function[0])
            self.logger.info(f'Successfully polled Stock data for {config.symbol[2]}')
            self.mykafka.send_data(config.topic[0], data3, config.symbol[2], 2)
            self.logger.info(f'Published stock data to Kafka for {config.symbol[2]}')            

            data4 = self.stocks4.get_data(config.symbol[3], config.function[0])
            self.logger.info(f'Successfully polled Stock data for {config.symbol[3]}')
            self.mykafka.send_data(config.topic[0], data4, config.symbol[3], 3)
            self.logger.info(f'Published stock data to Kafka for {config.symbol[3]}')            

            #push data to kafka topic in every 5 min
            time.sleep(300.0 - ((time.time() - start_time) % 300.0))  

if __name__ == "__main__":
    logging.info("Initializing stock Starts Polling")
    main = Main()
    main.run()