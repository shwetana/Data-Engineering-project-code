import json
import requests
import config as api_var


class StockData:

    def __init__(self):
        self.api = api_var.API_URL

    def get_data(self, symbol, function):
        data = {"function": function,
                "symbol": symbol,
                "outputsize": api_var.output_size,
                "datatype": api_var.data_type,
                "interval": api_var.interval,
                "apikey": api_var.api_key}

        response = requests.get(self.api, data)
        json_data = response.text
        return json.loads(json_data)

# sampletest = StockData()
# ps_list = []
# for cmp in api_var.symbol:
#     ps = sampletest.get_data(cmp, api_var.function[0])
#     ps_list.append(ps)
# print(ps_list[3])