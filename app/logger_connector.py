from Singleton import Singleton
from article_logs import ArticleLogs, NullArticleLogs
from log import Log


class LoggerConnector(metaclass=Singleton):
    def __init__(self, file_connector):
        self.file_connector = file_connector

    def get_all_logs(self):
        load = self.file_connector.read_json_file()

        article_logs = list()
        logs = list()
        for i in load:
            obj = ArticleLogs(i['id'], i['logs'])
            for j in obj.logs:
                log = Log(j['data'], j['text'])
                logs.append(log)
            article_logs.append(ArticleLogs(obj.id, logs))
            logs = []

        return article_logs

    def get_logs_by_id(self, id):
        load = self.file_connector.read_json_file()
        logs = list()
        article_logs = list()

        for i in load:
            obj = ArticleLogs(i['id'], i['logs'])
            if obj.id == id:
                for j in obj.logs:
                    log = Log(j['data'], j['text'])
                    logs.append(log)
                return ArticleLogs(obj.id, logs)

        return NullArticleLogs()

    def get_borrow_history(self, id):
        article_logs = self.get_logs_by_id(id)
        return [x for x in article_logs.logs if 'Returned' in x.text or 'Borrowed' in x.text]

    def add_log(self, id, log):
        article_logs = self.get_all_logs()

        def add_log_input(article_log):
            if article_log.id == id:
                article_log.logs.append(log)
                return article_log
            else:
                return article_log

        if any(x.id == id for x in article_logs):
            article_logs = list(map(add_log_input, article_logs))
        else:
            article_logs.append(ArticleLogs(id, [log]))

        self.file_connector.save_json_file(article_logs)

    def get_available_id(self):
        logs = self.get_all_logs()
        ids = [int(x.id) for x in logs]
        return str(sorted(ids)[-1] + 1)
