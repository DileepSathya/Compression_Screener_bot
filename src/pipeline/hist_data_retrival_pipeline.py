from src import logger
from src.utils.common import format_symbol  # should handle both str and list if needed
from datetime import datetime
from src.configurations.config import config_manager

class hist_data_retrival_pipeline:
    @staticmethod
    def hist_data():
        in_symbol_list = config_manager.data_loading_config()

        symbols_list = [format_symbol(symbol) for symbol in in_symbol_list]

        start_date = "2005-01-01"
        end_date = datetime.today().strftime("%Y-%m-%d")

        return symbols_list, start_date, end_date


if __name__ == "__main__":
    symbols, start_date, end_date = hist_data_retrival_pipeline.hist_data()
    print("Formatted symbols:", symbols)
    print("Start date:", start_date)
    print("End date:", end_date)