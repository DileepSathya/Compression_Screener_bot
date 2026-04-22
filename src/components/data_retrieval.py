from src import logger
from fyers_apiv3 import fyersModel
from src.configurations.config import config_manager
from src.pipeline.hist_data_retrival_pipeline import hist_data_retrival_pipeline
from datetime import datetime, timedelta,date
from src.utils.common import extract_candles_with_symbol,clear_hist_data_json
from src.utils.common import format_symbol
from src.components.mongodb_saver import MongoDBSaver

class DataRetrieval:

    def __init__(self):
        logger.info("Accessing client_id and acesstoken")
        client_id, access_token = config_manager.authentication()
        logger.info("Accessing client_id and acesstoken successful")
        self.fyers = fyersModel.FyersModel(
            client_id=client_id,
            is_async=False,
            token=access_token,
            log_path=""
        )
        self.mongodb_saver = MongoDBSaver()

    def userdata(self):
        response = self.fyers.get_profile()
        print(response)
        return response

    def hist_data(self):

        symbols_list, start_date, end_date = hist_data_retrival_pipeline.hist_data()

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        max_days = 100
        delta = timedelta(days=max_days)

        for symbol in symbols_list:
            start = start_date_obj
            while start <= end_date_obj:
                range_from = start.strftime("%Y-%m-%d")
                range_to = min(start + delta, end_date_obj).strftime("%Y-%m-%d")

                data = {
                    "symbol": symbol,
                    "resolution": "1",
                    "date_format": "1",
                    "range_from": range_from,
                    "range_to": range_to,
                    "cont_flag": "1"
                }

                print(f"\n Fetching data for {symbol} from {range_from} to {range_to}...")
                response = self.fyers.history(data=data)
          
                data_with_symbols=extract_candles_with_symbol(response_json=response,symbol=symbol)
                self.mongodb_saver.save_records(data_with_symbols)
                start = datetime.strptime(range_to, "%Y-%m-%d") + timedelta(days=1)

        self.mongodb_saver.flush()
        