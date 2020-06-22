from lettuce import *
import json

from article import Article
from config_manager import ConfigManager
from db_connector import DBConnector
from logger_connector import LoggerConnector
from file_connector import DbFileConnector, LoggerFileConnector
from os import remove
from copy import deepcopy


@step('I have the following articles in my database:')
def articles_in_database(step):
    world.path_db = 'test_db.json'
    formatted_articles = []
    given_list = deepcopy(step.hashes)
    for article_dict in given_list:
        if article_dict['is_available'] == 'no':
            article_dict['is_available'] = False
        else:
            article_dict['is_available'] = True

        article_dict['name'] = [article_dict['name_pl'], article_dict['name_en']]
        article_dict.pop('name_pl', None)
        article_dict.pop('name_en', None)
        article_dict['total_quantity'] = int(article_dict['total_quantity'])
        article_dict['quantity'] = int(article_dict['quantity'])
        formatted_articles.append(article_dict)

    with open(world.path_db, 'w') as f:
        json.dump(formatted_articles, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)


@step('I have the following logs in logger:')
def i_have_the_following_logs_in_logger(step):
    world.path_logger = 'test_logger.json'
    formatted_logs = deepcopy(step.hashes)

    logs_dict = {}
    for formatted_log in formatted_logs:
        logs_dict[formatted_log['id']] = {'id': formatted_log['id'], 'logs': []}

    for formatted_log in formatted_logs:
        log = {'data': formatted_log['data'], 'text': formatted_log['text']}
        logs_dict[formatted_log['id']]['logs'].append(log)

    with open(world.path_logger, 'w') as f:
        json.dump(list(logs_dict.values()), f, default=lambda o: o.__dict__, sort_keys=True, indent=4)


@step('I show articles')
def i_show_articles(step):
    config_manager = ConfigManager()
    config_manager.db_path = world.path_db
    db_file_connector = DbFileConnector(config_manager)
    db = DBConnector(db_file_connector)
    world.articles = db.get_all_articles()


@step('I show full history of rentals')
def i_show_full_history_of_rentals(step):
    config_manager = ConfigManager()
    config_manager.logger_path = world.path_logger
    logger_file_connector = LoggerFileConnector(config_manager)
    logger = LoggerConnector(logger_file_connector)

    all_logs = list()

    for article_log in logger.get_all_logs():
        logs = [it for it in article_log.logs if it.text == 'Borrowed' or it.text == 'Returned']
        logs = [vars(it) for it in logs]
        for log in logs:
            log['id'] = article_log.id

        all_logs = all_logs + logs

    world.logs = all_logs


@step('I show history of rentals of article (\d+)')
def i_show_history_of_rentals_of_article(step, number):
    config_manager = ConfigManager()
    config_manager.logger_path = world.path_logger
    logger_file_connector = LoggerFileConnector(config_manager)
    logger = LoggerConnector(logger_file_connector)

    logs = [vars(it) for it in logger.get_borrow_history(number)]
    for log in logs:
        log['id'] = number

    world.logs = logs


@step('I show article by name "(.*?)"')
def i_show_one_article(step, name):
    config_manager = ConfigManager()
    config_manager.db_path = world.path_db
    db_file_connector = DbFileConnector(config_manager)
    db = DBConnector(db_file_connector)
    world.articles = db.get_articles_by_name(name)


@step('I add following article')
def i_add_article(step):
    article = None

    for article_dict in deepcopy(step.hashes):
        if article_dict['is_available'] == 'no':
            article_dict['is_available'] = False
        else:
            article_dict['is_available'] = True

        name = [article_dict['name_pl'], article_dict['name_en']]
        article = Article('3', name, int(article_dict['total_quantity']),
                          int(article_dict['quantity']), article_dict['is_available'])

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


@step('I change to available article (\d+)')
def i_change_to_available_article(step, number):
    config_manager = ConfigManager()
    config_manager.db_path = world.path_db
    db_file_connector = DbFileConnector(config_manager)
    db = DBConnector(db_file_connector)

    new_obj = db.change_article_availability(number, True)
    if new_obj:
        db.remove_article_by_id(number)
        db.add_article(new_obj)
    world.articles = db.get_all_articles()


@step('I change to not available article (\d+)')
def i_change_to_not_available_article(step, number):
    config_manager = ConfigManager()
    config_manager.db_path = world.path_db
    db_file_connector = DbFileConnector(config_manager)
    db = DBConnector(db_file_connector)

    new_obj = db.change_article_availability(number, False)
    if new_obj:
        db.remove_article_by_id(number)
        db.add_article(new_obj)
    world.articles = db.get_all_articles()


@step('I see those listed articles:')
def i_see_listed_articles(step):
    actual_articles = list()
    for article in world.articles:
        obj = vars(article)
        obj['name_pl'] = obj['name'][0]
        obj['name_en'] = obj['name'][1]
        obj.pop('name', None)
        actual_articles.append(obj)

    expected_articles = list()
    for article_dict in deepcopy(step.hashes):
        if article_dict['is_available'] == 'no':
            article_dict['is_available'] = False
        else:
            article_dict['is_available'] = True

        article_dict['total_quantity'] = int(article_dict['total_quantity'])
        article_dict['quantity'] = int(article_dict['quantity'])
        expected_articles.append(article_dict)

    actual = set(tuple(sorted(d.items())) for d in actual_articles)
    expected = set(tuple(sorted(d.items())) for d in expected_articles)

    assert actual.symmetric_difference(expected) == set()

@step('I see those listed logs:')
def i_see_listed_logs(step):
    list1 = set(tuple(sorted(d.items())) for d in world.logs)
    list2 = set(tuple(sorted(d.items())) for d in step.hashes)

    assert list1.symmetric_difference(list2) == set()


@step('I show borrowed articles')
def i_show_borrowed_articles(step):
    config_manager = ConfigManager()
    config_manager.db_path = world.path_db
    db_file_connector = DbFileConnector(config_manager)
    db = DBConnector(db_file_connector)
    world.articles = db.get_articles_by_borrowed()


@after.each_scenario
def teardown_test_db(scenario):
    try:
        remove(world.path_db)
    except:
        pass

    try:
        remove(world.path_logger)
    except:
        pass
