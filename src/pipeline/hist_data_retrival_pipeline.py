from src import logger
from src.utils.common import format_symbol  # should handle both str and list if needed
from datetime import datetime
from src.configurations.config import config_manager

class hist_data_retrival_pipeline:
    @staticmethod
    def hist_data():
        in_symbol_list = config_manager.data_loading_config()

        symbols_list = [format_symbol(symbol) for symbol in in_symbol_list]
  
        start_date = input("Enter the start date (YYYY-MM-DD): ")

        while True:
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            try:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
                today = datetime.today()

                if end_date_obj >= today:
                    print("❌ End date should be **before** today's date. Please enter again.")
                else:
                    break
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD.")

        return symbols_list, start_date, end_date


if __name__ == "__main__":
    symbols, start_date, end_date = hist_data_retrival_pipeline.hist_data()
    print("Formatted symbols:", symbols)
    print("Start date:", start_date)
    print("End date:", end_date)