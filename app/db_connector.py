from Singleton import Singleton
from article import Article


class DBConnector(metaclass=Singleton):
    def __init__(self, file_connector):
        self.file_connector = file_connector

    def get_all_articles(self):
        load = self.file_connector.read_json_file()

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
        self.file_connector.save_json_file(articles)

    def remove_article_by_id(self, id):
        articles = self.get_all_articles()
        articles = [it for it in articles if it.id != id]
        self.file_connector.save_json_file(articles)

    def change_article_availability(self, id, available):
        articles = self.get_all_articles()
        for article in articles:
            if article.id == id:
                article.is_available = available
                return article
