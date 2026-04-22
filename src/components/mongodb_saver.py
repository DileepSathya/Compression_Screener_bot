import os
from typing import List, Dict

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

from src import logger


class MongoDBSaver:
    def __init__(self):
        load_dotenv()

        mongo_uri = os.getenv("MONGODB_URI")
        collection_name = os.getenv("MONGODB_COLLECTION", "hist_data_1m")

        if not mongo_uri:
            raise ValueError("MONGODB_URI is not set in .env file")

        self.client = MongoClient(mongo_uri)
        self.db = self.client["Markets_data"]
        self.collection = self.db[collection_name]

        # Ensure uniqueness for time-series candle records.
        self.collection.create_index(
            [("date", 1), ("time", 1), ("symbol", 1)],
            unique=True,
        )
        logger.info(
            "MongoDB connection initialized for database 'Markets_data', collection '%s'.",
            collection_name,
        )

    def save_records(self, records: List[Dict]):
        if not records:
            return

        unique_records = {
            (record["date"], record["time"], record["symbol"]): record
            for record in records
        }

        operations = [
            UpdateOne(
                {
                    "date": record["date"],
                    "time": record["time"],
                    "symbol": record["symbol"],
                },
                {"$set": record},
                upsert=True,
            )
            for record in unique_records.values()
        ]

        result = self.collection.bulk_write(operations, ordered=False)
        logger.info(
            "MongoDB save complete. Upserted: %s, Modified: %s",
            result.upserted_count,
            result.modified_count,
        )
