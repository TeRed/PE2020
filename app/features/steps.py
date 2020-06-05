from lettuce import *
import json

from article import Article
from config_manager import ConfigManager
from db_connector import DBConnector
from file_connector import DbFileConnector
from os import remove


@step('I have the following articles in my database:')
def articles_in_database(step):
    world.path_db = 'test_db.json'
    formated_articles = []

    for article_dict in step.hashes:
        if article_dict['is_available'] == 'no':
            article_dict['is_available'] = False
        else:
            article_dict['is_available'] = True
        formated_articles.append(article_dict)

    with open(world.path_db, 'w') as f:
        json.dump(formated_articles, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)


@step('I show articles')
def i_show_articles(step):
    config_manager = ConfigManager()
    config_manager.db_path = world.path_db
    db_file_connector = DbFileConnector(config_manager)
    db = DBConnector(db_file_connector)
    world.articles = db.get_all_articles()


@step('I add following article')
def i_add_article(step):
    article = None

    for article_dict in step.hashes:
        if article_dict['is_available'] == 'no':
            article_dict['is_available'] = False
        else:
            article_dict['is_available'] = True
        article = Article(article_dict['id'], article_dict['name'], article_dict['is_available'])

    config_manager = ConfigManager()
    config_manager.db_path = world.path_db
    db_file_connector = DbFileConnector(config_manager)
    db = DBConnector(db_file_connector)
    db.add_article(article)
    world.articles = db.get_all_articles()


@step('I remove article (\d+)')
def i_remove_article(step, number):
    config_manager = ConfigManager()
    config_manager.db_path = world.path_db
    db_file_connector = DbFileConnector(config_manager)
    db = DBConnector(db_file_connector)
    db.remove_article_by_id(number)
    world.articles = db.get_all_articles()


@step('I see those listed articles:')
def i_see_listed_articles(step):
    articles = list()
    for article in world.articles:
        obj = vars(article)
        if obj['is_available']:
            obj['is_available'] = 'yes'
        else:
            obj['is_available'] = 'no'
        articles.append(obj)

    list1 = set(tuple(sorted(d.items())) for d in articles)
    list2 = set(tuple(sorted(d.items())) for d in step.hashes)

    assert list1.symmetric_difference(list2) == set()


@after.each_scenario
def teardown_test_db(scenario):
    remove(world.path_db)
