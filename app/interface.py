from abc import ABCMeta
from article import Article
from log import Log
from datetime import datetime
import os
import sys
sys.path.insert(0, 'lib')
from prettytable import PrettyTable
from pydoc import pager
import i18n


class Interface:

    def __init__(self, db_connector, logger_connector, config_manager):
        self.logger = logger_connector
        self.base = db_connector
        self.config_manager = config_manager
        self.app_info_logger = AppInfoLogger()

    def printInfo(self, text):
        print("INFO: " + text)

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu(self):
        self.app_info_logger.log_start()

        INVOKER = Invoker(self.base, self.logger, self.config_manager, self.app_info_logger)

        while True:
            self.cls()
            print(i18n.t('RENTAL_COMPANY_NAME'))
            print('')
            print(
                (f' 1: {i18n.t("LIST_ALL_ARTICLES")}\n'
                 f' 2: {i18n.t("LIST_RENTED_ARTICLES")}\n'
                 f' 3: {i18n.t("VIEW_FULL_RENTAL_HISTORY")}\n'
                 f' 4: {i18n.t("VIEW_RENTAL_HISTORY_OF_THE_ARTICLE")}\n'
                 f' 5: {i18n.t("ADD_ARTICLE")}\n'
                 f' 6: {i18n.t("DELETE_ARTICLE")}\n'
                 f' 7: {i18n.t("SEARCH_THE_ARTICLE_BY_NAME")}\n'
                 f' 8: {i18n.t("SEARCH_THE_ARTICLE_BY_ID")}\n'
                 f' 9: {i18n.t("CHANGE_THE_RENTAL_STATUS")}\n'
                 f'10: {i18n.t("VIEW_CURRENT_CONFIGURATION")}\n'
                 f'11: {i18n.t("CHANGE_THE_CONFIGURATION")}\n'
                 f'12: {i18n.t("SAVE_THE_CURRENT_CONFIGURATION")}\n'
                 f'13: {i18n.t("BORROW_ARTICLE")}\n'
                 f'14: {i18n.t("RETURN_ARTICLE")}\n'
                 f'15: {i18n.t("LIST_AVAILABLE_ARTICLES")}\n'
                 f' 0: {i18n.t("EXIT_APPLICATION")}\n'))

            choice = input(f'{i18n.t("DIAL_THE_NUMBER")}: ')
            self.cls()
            INVOKER.execute(choice)


class AppInfoLogger:
    info_title = ""
    info_divider = ""

    def __init__(self):
        self.info_title = "INFO"
        self.info_divider = ": "

    def log_start(self):
        print(self.info_title + self.info_divider + i18n.t('THE_APPLICATION_HAS_BEEN_LAUNCHED'))

    def log_end(self):
        print(self.info_title + self.info_divider + i18n.t('THE_APPLICATION_HAS_BEEN_STOPPED'))

    def log_error(self, text):
        print(self.info_title + self.info_divider + f'{i18n.t("AN_ERROR_OCCURRED")}{text}')

    def log_info(self, text):
        print(self.info_title + self.info_divider + text)


class IOWrapper:

    @staticmethod
    def print_articles(articles, current_lang_val):
        pt = PrettyTable()
        pt.field_names = [i18n.t('ID'), i18n.t('NAME'), i18n.t('NAME_SECOND_LANG'), i18n.t('TOTAL_QUANTITY'),
                          i18n.t('QUANTITY'), i18n.t('AVAILABILITY')]
        if current_lang_val == "en":
            for article in articles:
                pt.add_row([int(article.id), article.name[1], article.name[0], article.total_quantity, article.quantity,
                            i18n.t('YES') if article.is_available else i18n.t('NO')])
        else:
            for article in articles:
                pt.add_row([int(article.id), article.name[0], article.name[1], article.total_quantity, article.quantity,
                            i18n.t('YES') if article.is_available else i18n.t('NO')])
        pt.sortby = i18n.t('ID')
        pager(str(pt))

    @staticmethod
    def print_articles_log(articles_logs):
        pt = PrettyTable()
        pt.field_names = [i18n.t('ID'), i18n.t('DATE'), i18n.t('TEXT')]
        for article_log in articles_logs:
            logs = [it for it in article_log.logs if 'Borrowed' in it.text or 'Returned' in it.text]
            for log in logs:
                state = log.text.split(" ")
                pt.add_row([int(article_log.id), log.data,
                            str(state[1]) + " " + i18n.t('RETURNED') if 'Returned' in log.text else str(
                                state[1]) + " " + i18n.t('BORROWED')])
        pt.sortby = i18n.t('ID')
        pager(str(pt))

    @staticmethod
    def continue_pause():
        input(i18n.t('PRESS_ENTER_TO_CONTINUE'))

    @staticmethod
    def print_article_log(logs):
        pt = PrettyTable()
        pt.field_names = [i18n.t('DATE'), i18n.t('TEXT')]
        for obj in logs:
            state = obj.text.split(" ")
            pt.add_row([obj.data, str(state[1]) + " " + i18n.t('RETURNED') if 'Returned' in obj.text else str(
                state[1]) + " " + i18n.t('BORROWED')])
        pt.sortby = i18n.t('DATE')
        pager(str(pt))


class ICommand(metaclass=ABCMeta):

    @staticmethod
    def execute():
        """The required execute method which all command obejcts will use"""


class DisplayAllArticlesCommand(ICommand):

    def __init__(self, base, config_manager):
        self.base = base
        self.config_manager = config_manager

    def execute(self):
        current_lang_val = self.config_manager.language
        IOWrapper.print_articles(self.base.get_all_articles(), current_lang_val)
        IOWrapper.continue_pause()


class DisplayHistoryCommand(ICommand):

    def __init__(self, logger):
        self.logger = logger

    def execute(self):
        article_id = input(i18n.t('ENTER_THE_ID_OF_THE_ARTICLE'))
        IOWrapper.print_article_log(self.logger.get_borrow_history(article_id))
        IOWrapper.continue_pause()


class AddArticleCommand(ICommand):

    def __init__(self, base, logger, config_manager, app_info_logger):
        self.base = base
        self.logger = logger
        self.config_manager = config_manager
        self.app_info_logger = app_info_logger

    def execute(self):
        current_lang_val = self.config_manager.language
        if current_lang_val == "en":
            new_name_en = input(i18n.t('ENTER_THE_NAME_OF_THE_ARTICLE_EN'))
            new_name_pl = input(i18n.t('ENTER_THE_NAME_OF_THE_ARTICLE_PL'))
        else:
            new_name_pl = input(i18n.t('ENTER_THE_NAME_OF_THE_ARTICLE_PL'))
            new_name_en = input(i18n.t('ENTER_THE_NAME_OF_THE_ARTICLE_EN'))
        new_quantity = int(input(i18n.t('ENTER_THE_QUANTITY_OF_THE_ARTICLE')))
        new_id = self.logger.get_available_id()
        new_obj = Article(new_id, [new_name_pl, new_name_en], new_quantity, new_quantity, True)

        self.base.add_article(new_obj)
        self.logger.add_log(new_id, Log(str(datetime.date(datetime.now())), "Added"))
        self.app_info_logger.log_info(i18n.t('ARTICLE_ADDED'))
        IOWrapper.continue_pause()


class DeleteArticleCommand(ICommand):

    def __init__(self, base, logger, app_info_logger):
        self.base = base
        self.logger = logger
        self.app_info_logger = app_info_logger

    def execute(self):
        rm_id = input(i18n.t('ENTER_THE_ID_OF_THE_ARTICLE'))

        if self.base.remove_article_by_id(rm_id):
            self.logger.add_log(rm_id, Log(str(datetime.date(datetime.now())), "Deleted"))
            self.app_info_logger.log_info(i18n.t('ARTICLE_DELETED'))
        else:
            self.app_info_logger.log_info(i18n.t('ARTICLE_OF_ID_LACKING'))

        IOWrapper.continue_pause()


class SearchForAnArticleByNameCommand(ICommand):

    def __init__(self, base, config_manager):
        self.base = base
        self.config_manager = config_manager

    def execute(self):
        current_lang_val = self.config_manager.language
        src_name = input(i18n.t('ENTER_THE_NAME_OF_THE_ARTICLE'))
        IOWrapper.print_articles(self.base.get_articles_by_name(src_name), current_lang_val)
        IOWrapper.continue_pause()


class SearchForAnArticleByIdCommand(ICommand):

    def __init__(self, base, config_manager, app_info_logger):
        self.base = base
        self.config_manager = config_manager
        self.app_info_logger = app_info_logger

    def execute(self):
        src_id = input(i18n.t('ENTER_THE_ID_OF_THE_ARTICLE'))
        current_lang_val = self.config_manager.language
        article = self.base.get_article_by_id(src_id)
        if article:
            IOWrapper.print_articles([article], current_lang_val)
            IOWrapper.continue_pause()
        else:
            self.app_info_logger.log_info(i18n.t('ARTICLE_OF_ID_LACKING'))
            IOWrapper.continue_pause()


class ChangeStatusCommand(ICommand):

    def __init__(self, base, logger, app_info_logger):
        self.base = base
        self.logger = logger
        self.app_info_logger = app_info_logger

    def execute(self):
        obj_id = input(i18n.t('ENTER_THE_ID_OF_THE_ARTICLE'))
        obj_article = self.base.get_article_by_id(obj_id)

        if obj_article:
            state = i18n.t('ARTICLE_AVAILABLE') if obj_article.is_available else i18n.t('ARTICLE_NOT_AVAILABLE')
            print(f'{state} {i18n.t("CHANGE_QUESTION")}')
            status = input(i18n.t('YES_OR_NO_QUESTION'))

            if status == '1':
                new_obj = self.base.change_article_availability(obj_id, not obj_article.is_available)
                if new_obj:
                    self.base.remove_article_by_id(obj_id)
                    self.base.add_article(new_obj)
                    if obj_article.is_available:
                        self.logger.add_log(obj_id, Log(str(datetime.date(datetime.now())), "Made article unavailable"))
                    else:
                        if obj_article.quantity == 0:
                            self.app_info_logger.log_info(i18n.t('CANT_BE_AVAILABLE_QUANTITY'))
                            IOWrapper.continue_pause()
                        else:
                            self.logger.add_log(obj_id,
                                                Log(str(datetime.date(datetime.now())), "Made article available"))
            elif status == '2':
                ""
            else:
                self.app_info_logger.log_info(i18n.t('ONLY_TWO_OPTIONS'))
                IOWrapper.continue_pause()
        else:
            self.app_info_logger.log_info(i18n.t('ARTICLE_OF_ID_LACKING'))
            IOWrapper.continue_pause()


class ReturnArticleCommand(ICommand):

    def __init__(self, base, logger, app_info_logger):
        self.base = base
        self.logger = logger
        self.app_info_logger = app_info_logger

    def execute(self):
        obj_id = input(i18n.t('ENTER_THE_ID_OF_THE_ARTICLE'))
        obj_article = self.base.get_article_by_id(obj_id)

        if obj_article:
            quantity = int(input(i18n.t('HOW_MANY_TO_RETURN')))
            if (quantity > 0 and quantity + obj_article.quantity < obj_article.total_quantity):
                new_obj = self.base.add_article_quantity(obj_id, quantity, True)
                if new_obj:
                    if obj_article.is_available == False:
                        self.logger.add_log(obj_id, Log(str(datetime.date(datetime.now())), "Made article available"))
                    self.base.remove_article_by_id(obj_id)
                    self.base.add_article(new_obj)
                    self.logger.add_log(obj_id, Log(str(datetime.date(datetime.now())), "Returned " + str(quantity)))
                self.app_info_logger.log_info(i18n.t('ARTICLES_RETURNED'))
                IOWrapper.continue_pause()
            else:
                self.app_info_logger.log_info(i18n.t('CANT_RETURN_ARTICLE'))
                IOWrapper.continue_pause()
        else:
            self.app_info_logger.log_info(i18n.t('ARTICLE_OF_ID_LACKING'))
            IOWrapper.continue_pause()


class BorrowArticleCommand(ICommand):

    def __init__(self, base, logger, app_info_logger):
        self.base = base
        self.logger = logger
        self.app_info_logger = app_info_logger

    def execute(self):
        obj_id = input(i18n.t('ENTER_THE_ID_OF_THE_ARTICLE'))
        obj_article = self.base.get_article_by_id(obj_id)

        if obj_article:
            state = i18n.t('ARTICLE_AVAILABLE') if obj_article.is_available else i18n.t('ARTICLE_NOT_AVAILABLE')
            if obj_article.is_available:
                quantity = int(input(i18n.t('HOW_MANY_TO_BORROW')))
                if obj_article.quantity > quantity:
                    new_obj = self.base.add_article_quantity(obj_id, (-1 * quantity), True)
                    if new_obj:
                        self.base.remove_article_by_id(obj_id)
                        self.base.add_article(new_obj)
                        self.logger.add_log(obj_id,
                                            Log(str(datetime.date(datetime.now())), "Borrowed " + str(quantity)))
                    self.app_info_logger.log_info(i18n.t('ARTICLES_BORROWED'))
                    IOWrapper.continue_pause()
                elif obj_article.quantity == quantity:
                    new_obj = self.base.add_article_quantity(obj_id, (-1 * quantity), False)
                    if new_obj:
                        self.base.remove_article_by_id(obj_id)
                        self.base.add_article(new_obj)
                        self.logger.add_log(obj_id,
                                            Log(str(datetime.date(datetime.now())), "Borrowed " + str(quantity)))
                        self.logger.add_log(obj_id, Log(str(datetime.date(datetime.now())), "Made article unavailable"))
                    self.app_info_logger.log_info(i18n.t('ARTICLES_BORROWED'))
                    IOWrapper.continue_pause()
                elif obj_article.quantity < quantity:
                    self.app_info_logger.log_info(i18n.t('NOT_ENOUGH_ARTICLE_AVAILABLE'))
                    IOWrapper.continue_pause()
            else:
                self.app_info_logger.log_info(i18n.t('ARTICLE_NOT_AVAILABLE'))
                IOWrapper.continue_pause()

        else:
            self.app_info_logger.log_info(i18n.t('ARTICLE_OF_ID_LACKING'))
            IOWrapper.continue_pause()


class DisplayConfigCommand(ICommand):

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def execute(self):
        print(i18n.t('CURRENT_CONFIGURATION'))
        config_attributes = self.config_manager.__dict__

        for key, val in config_attributes.items():
            print(f'{key}: "{val}"')

        IOWrapper.continue_pause()


class ChangeConfigCommand(ICommand):

    def __init__(self, config_manager, app_info_logger):
        self.config_manager = config_manager
        self.app_info_logger = app_info_logger
        self.language_attr_key = 0

    def execute(self):
        config_attributes = list()

        for key, val in self.config_manager.__dict__.items():
            config_attributes.append(key)

        print(i18n.t('CONFIGURATION_CHANGE'))
        for index, val in enumerate(config_attributes):
            if val == 'language':
                self.language_attr_key = index + 1
            print(f'{index + 1}: "{val}"')

        index = input(i18n.t('SELECT_AN_ATTRIBUTE_TO_CHANGE'))
        if int(index) == self.language_attr_key:
            current_lang_val = self.config_manager.language
            print(f"{i18n.t('CURRENT_LANGUAGE')}{current_lang_val}. {i18n.t('CHANGE_QUESTION')}")
            status = input(i18n.t('YES_OR_NO_QUESTION'))

            if status == '1':
                self.config_manager.set_language("pl" if current_lang_val == "en" else "en")
                self.app_info_logger.log_info(i18n.t('THE_ATTRIBUTE_HAS_BEEN_CHANGED'))
            elif status == '2':
                ""
            else:
                self.app_info_logger.log_info(i18n.t('ONLY_TWO_OPTIONS'))
        elif len(config_attributes) >= int(index) > 0:
            new_value = input(i18n.t('ENTER_A_NEW_VALUE'))
            setattr(self.config_manager, config_attributes[int(index) - 1], new_value)
            self.app_info_logger.log_info(i18n.t('THE_ATTRIBUTE_HAS_BEEN_CHANGED'))
        else:
            self.app_info_logger.log_info(i18n.t('NO_SUCH_ATTRIBUTE'))

        IOWrapper.continue_pause()


class SaveConfigCommand(ICommand):

    def __init__(self, config_manager, app_info_logger):
        self.config_manager = config_manager
        self.app_info_logger = app_info_logger

    def execute(self):
        self.config_manager.save_configuration()
        self.app_info_logger.log_info(i18n.t('CONFIGURATION_SAVED'))
        IOWrapper.continue_pause()


class DisplayAllNotAvailableArticlesCommand(ICommand):

    def __init__(self, base, config_manager):
        self.base = base
        self.config_manager = config_manager

    def execute(self):
        current_lang_val = self.config_manager.language
        IOWrapper.print_articles(self.base.get_articles_by_availability(False), current_lang_val)
        IOWrapper.continue_pause()


class DisplayAllAvailableArticlesCommand(ICommand):

    def __init__(self, base, config_manager):
        self.base = base
        self.config_manager = config_manager

    def execute(self):
        current_lang_val = self.config_manager.language
        IOWrapper.print_articles(self.base.get_articles_by_availability(True), current_lang_val)
        IOWrapper.continue_pause()


class DisplayAllBorrowedArticlesCommand(ICommand):
    def __init__(self, base, config_manager):
        self.base = base
        self.config_manager = config_manager

    def execute(self):
        current_lang_val = self.config_manager.language
        IOWrapper.print_articles(self.base.get_articles_by_borrowed(), current_lang_val)
        IOWrapper.continue_pause()


class DisplayFullHistoryCommand(ICommand):

    def __init__(self, logger):
        self.logger = logger

    def execute(self):
        IOWrapper.print_articles_log(self.logger.get_all_logs())
        IOWrapper.continue_pause()


class StopApp(ICommand):

    def __init__(self, app_info_logger):
        self.app_info_logger = app_info_logger

    def execute(self):
        self.app_info_logger.log_end()
        raise SystemExit


class Invoker:

    def __init__(self, base, logger, config_manager, app_info_logger):
        self.base = base
        self.logger = logger
        self.config_manager = config_manager
        self.app_info_logger = app_info_logger
        self._commands = {'1': DisplayAllArticlesCommand(self.base, self.config_manager),
                          '2': DisplayAllBorrowedArticlesCommand(self.base, self.config_manager),
                          '3': DisplayFullHistoryCommand(self.logger),
                          '4': DisplayHistoryCommand(self.logger),
                          '5': AddArticleCommand(self.base, self.logger, self.config_manager, self.app_info_logger),
                          '6': DeleteArticleCommand(self.base, self.logger, self.app_info_logger),
                          '7': SearchForAnArticleByNameCommand(self.base, self.config_manager),
                          '8': SearchForAnArticleByIdCommand(self.base, self.config_manager, self.app_info_logger),
                          '9': ChangeStatusCommand(self.base, self.logger, self.app_info_logger),
                          '10': DisplayConfigCommand(self.config_manager),
                          '11': ChangeConfigCommand(self.config_manager, self.app_info_logger),
                          '12': SaveConfigCommand(self.config_manager, self.app_info_logger),
                          '13': BorrowArticleCommand(self.base, self.logger, self.app_info_logger),
                          '14': ReturnArticleCommand(self.base, self.logger, self.app_info_logger),
                          '15': DisplayAllAvailableArticlesCommand(self.base, self.config_manager),
                          '0': StopApp(self.app_info_logger)}

    def execute(self, command_name):
        if command_name in self._commands.keys():
            self._commands[command_name].execute()
        else:
            self.app_info_logger.log_error(i18n.t('WRONG_NUMBER_GIVEN'))
            IOWrapper.continue_pause()
