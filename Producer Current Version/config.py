""" API vars """
API_URL = "https://www.alphavantage.co/query"

function = ["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY"]
#symbol = ['HDFCBANK.BSE', 'RELIANCE.BSE', 'ICICIBANK.BSE', 'INFY.BSE']
#list_cmp = ["AAPL", "ADBE", "ADI", "ADP", "ALGN", "ALXN", "AMAT", "AMD", "AMGN", "AMZN", "ASML", "ATVI", "AVGO", "BIIB", "BMRN", "CDNS", "CERN", "CHKP", "CMCSA", "COST", "CSCO", "CSX", "CTAS", "CTSH", "CTXS", "EBAY", "EXPE", "FAST", "FB", "FISV", "FOX", "GILD", "GOOG", "GOOGL", "IDXX", "ILMN", "INCY", "INTC", "INTU", "ISRG", "JD", "LBTYA", "LBTYK", "LRCX", "MAR", "MCHP", "MELI", "MSFT", "MXIM"]
list_cmp = ["AAPL", "ADBE", "ADI"]
symbol = ['SAP', 'SIEGY', 'AAPL', 'AMZN']
output_size = "compact"
data_type = "json"
interval = "5min"
#api_key = "S6TX3KQ1W5OO2ZTK"
api_key = "T51VUT68CNVQY7XA"
#api_key = "MJLPMBB0U80SOFBK"

""" Kafka configs """
#kafka_broker = "35.224.85.53:9092"
kafka_broker = "127.0.0.1:9092"
topic = ["StockMarkets","StocksMongo"]
