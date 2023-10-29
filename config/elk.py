from logging import Handler
import elasticsearch, elasticsearch_dsl
from elasticsearch import Elasticsearch


class ElkHandler(Handler) :
    def __init__(self, host, *args, **kwargs) :
        super().__init__(level=kwargs.get('level'))
        self.host = host
        self.formatter = kwargs.get('formatter')
        self.elk = Elasticsearch(hosts=self.host)

    def emit(self, record) :
        try:
            msg = self.format(record)
            index = self.elk.index(index='')
            index.write(msg + self.terminator)
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

