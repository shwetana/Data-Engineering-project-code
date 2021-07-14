from API_call_code import StockData
from kafka_producer import MyKafka
import logging
import time
import config
from logging.config import dictConfig
from kafka_consumer import MongoConnection

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
        # self.stocks2 = StockData()
        # self.stocks3 = StockData()
        # self.stocks4 = StockData()
        # self.stocks5 = StockData()
        # self.stocks6 = StockData()
        # self.stocks7 = StockData()        
        self.logger.info(f'StockData Starts Polling Initialized')

    def run(self):
        self.init_stock()
        start_time = time.time()
        #chunks = [config.list_cmp[i:i + 7] for i in range(0, len(config.list_cmp), 7)]
        for i in range(len(config.list_cmp)):
            data1 = self.stocks1.get_data(config.list_cmp[i], config.function[1])
            self.logger.info(f'Successfully polled Stock data for daily')
            self.mykafka.send_data(config.topic[1], data1, config.list_cmp[i],0)
            self.logger.info(f'Published stock data to Kafka for daily')
            time.sleep(15)

            # data2 = self.stocks2.get_data(chunks[i][1], config.function[1])
            # self.logger.info(f'Successfully polled Stock data for daily')
            # self.mykafka.send_data(config.topic[1], data2, chunks[i][1],1)
            # self.logger.info(f'Published stock data to Kafka for daily')

            # data3 = self.stocks3.get_data(chunks[i][2], config.function[1])
            # self.logger.info(f'Successfully polled Stock data for daily')
            # self.mykafka.send_data(config.topic[1], data3, chunks[i][2],2)
            # self.logger.info(f'Published stock data to Kafka for daily')

            # data4 = self.stocks4.get_data(chunks[i][3], config.function[1])
            # self.logger.info(f'Successfully polled Stock data for daily')
            # self.mykafka.send_data(config.topic[1], data4, chunks[i][3],3)
            # self.logger.info(f'Published stock data to Kafka for daily')

            # data5 = self.stocks5.get_data(chunks[i][4], config.function[1])
            # self.logger.info(f'Successfully polled Stock data for daily')
            # self.mykafka.send_data(config.topic[1], data5, chunks[i][4],4)
            # self.logger.info(f'Published stock data to Kafka for daily')

            # data6 = self.stocks6.get_data(chunks[i][5], config.function[1])
            # self.logger.info(f'Successfully polled Stock data for daily')
            # self.mykafka.send_data(config.topic[1], data6, chunks[i][5],5)
            # self.logger.info(f'Published stock data to Kafka for daily')

            # data7 = self.stocks7.get_data(chunks[i][6], config.function[1])
            # self.logger.info(f'Successfully polled Stock data for daily')
            # self.mykafka.send_data(config.topic[1], data7, chunks[i][6],6)
            # self.logger.info(f'Published stock data to Kafka for daily')

        self.logger.info("Data sent to broker successfully for all 49 assets")

        mongoCon = MongoConnection()
        self.logger.info(f'Starting MongoDB connection to push data into it')
        mongoCon.insert_many_records("StockMarket", "StocksDaily")
        self.logger.info(f'Data insertion in MongoDB complete')

if __name__ == "__main__":
    logging.info("Initializing stock Starts Polling")
    main = Main()
    main.run()