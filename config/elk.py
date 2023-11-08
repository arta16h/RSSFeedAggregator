from logging import Handler
from datetime import datetime
import time
import json

from elasticsearch import Elasticsearch


class LogSender:
    def __init__(self, elk) -> None:
        self.elk = elk

    def writelog(self, message, formatter, db_name=None, daily_index=False) :
        suffix = "_" + str(time.strftime("%Y_%m_%d")) if daily_index else ""
        index_name = db_name + suffix or f'log_{time.strftime("%Y_%m_%d")}'
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        log_data = {'message' : formatter(message)}
        log_data['timestamp'] = timestamp
        log_data['level'] = message.levelname
        self.elk.index(index=index_name.lower(), document=log_data)
        

class ElkHandler(Handler) :
    def __init__(self, host,*args, **kwargs) :
        self.db_name = kwargs.pop('db_name', None)
        self.daily_index = kwargs.pop('daily_index', False)
        super().__init__(*args, **kwargs)
        self.host = host
        self.elk = Elasticsearch(self.host)
        self.sender = LogSender(elk=self.elk)

    def emit(self, record) :
        try:
            self.sender.writelog(message=record, formatter=self.format, db_name=self.db_name, daily_index=self.daily_index)
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

