import json
from app.article import Article


class DBConnector:
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name

    def read_json_file(self):
        with open(self.db_file_name) as f:
            load = json.load(f)
        return load

    def get_all_articles(self):
        load = self.read_json_file()

        articles = list()
        for i in load:
            obj = Article(i['id'], i['name'], i['is_available'])
            articles.append(obj)

        return articles

    def get_articles_by_name(self, name):
        articles = self.get_all_articles()
        articles = [it for it in articles if name.lower() in it.name.lower()]

        return articles

    def get_article_by_id(self, id):
        articles = self.get_all_articles()
        for a in articles:
            if a.id == id:
                return a

        return False

    def add_article(self, obj):
        articles = self.get_all_articles()
        articles.append(obj)

        with open(self.db_file_name, 'w') as f:
            json.dump([obj.__dict__ for obj in articles], f)

    def change_article_availability(self, id, available):
        articles = self.get_all_articles()
        for article in articles:
            if article.id == id:
                article.is_available = available
                return article
