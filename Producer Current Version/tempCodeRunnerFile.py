        # for i in range(len(config.list_cmp)):
        #     data5 = self.stocks5.get_data(config.list_cmp[i], config.function[1])
        #     self.logger.info(f'Successfully polled Stock data for daily')
        #     self.mykafka.send_data(config.topic[1], data5, config.list_cmp[i], 0)
        #     self.logger.info(f'Published stock data to Kafka for daily')