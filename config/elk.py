from logging import Handler
import datetime
import time
import json

from elasticsearch import Elasticsearch


class LogSender:
    def __init__(self,elk) -> None:
        self.elk = elk

    def writelog(self, message, formatter) :
        index_name = f'log_{time.strftime("%Y_%m_%d")}'
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        log_data = json.loads(formatter(message))
        log_data['timestamp'] = timestamp
        log_data['level'] = message.levelname
        self.elk.index(index=index_name, document=log_data)


class ElkHandler(Handler) :
    def __init__(self, host, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.host = host
        self.formatter = kwargs.get('formatter')
        self.elk = Elasticsearch(hosts=self.host)
        self.sender = LogSender(elk=self.elk)

    def emit(self, record) :
        try:
            self.sender.writelog(record, self.formatter)
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

