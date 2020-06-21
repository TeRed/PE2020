from abc import ABCMeta

from article import Article
from log import Log
from datetime import datetime
import os
from prettytable import PrettyTable
from pydoc import pager


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
            print('Wypozyczalnia rzeczy\n')
            print(
                ('1: Wypisz liste wszystkich artykulow\n'
                 '2: Wypisz liste wypozyczonych artykulow\n'
                 '3: Wyswietl pelna historie wypozyczen\n'
                 '4: Wypisz historie wypozyczen artykulu\n'
                 '5: Dodaj artykul\n'
                 '6: Usun artykul\n'
                 '7: Wyszukaj artykul po nazwie\n'
                 '8: Wyszukaj artykul po id\n'
                 '9: Zmien status wypozyczenia\n'
                 '10: Aktualna konfiguracja\n'
                 '11: Zmiana konfiguracji\n'
                 '12: Zapisz aktualna konfiguracje aplikacji\n'
                 '0: Wyjdz z aplikacji\n'))

            choice = input('Prosze wybrac numer: ')
            self.cls()
            INVOKER.execute(choice)


class AppInfoLogger:
    info_title = ""
    info_divider = ""

    def __init__(self):
        self.info_title = "INFO"
        self.info_divider = ": "

    def log_start(self):
        print(self.info_title + self.info_divider + 'Aplikacja zostala uruchomiona.')

    def log_end(self):
        print(self.info_title + self.info_divider + 'Aplikacja zostala zatrzymana.')

    def log_error(self, text):
        print(self.info_title + self.info_divider + 'W aplikacji wystapil blad. ERROR: ' + text)

    def log_info(self, text):
        print(self.info_title + self.info_divider + text)


class IOWrapper:

    @staticmethod
    def print_articles(articles):
        pt = PrettyTable()
        pt.field_names = ['ID', 'NAZWA', 'NAME', 'DOSTEPNOSC']
        for article in articles:
            pt.add_row([article.id, article.name[0], article.name[1], 'tak' if article.is_available else 'nie'])

        pager(str(pt))

    @staticmethod
    def print_articles_log(articles_logs):
        pt = PrettyTable()
        pt.field_names = ['ID', 'DATA', 'TEKST']
        for article_log in articles_logs:
            logs = [it for it in article_log.logs if it.text == 'Borrowed' or it.text == 'Returned']
            for log in logs:
                pt.add_row([article_log.id, log.data, log.text])

        pager(str(pt))

    @staticmethod
    def continue_pause():
        input("Nacisnij Enter, aby kontynowac")

    @staticmethod
    def print_article_log(logs):
        pt = PrettyTable()
        pt.field_names = ['DATA', 'TEKST']
        for obj in logs:
            pt.add_row([obj.data, obj.text])

        pager(str(pt))


class ICommand(metaclass=ABCMeta):

    @staticmethod
    def execute():
        """The required execute method which all command obejcts will use"""


class DisplayAllArticlesCommand(ICommand):

    def __init__(self, base):
        self.base = base

    def execute(self):
        IOWrapper.print_articles(self.base.get_all_articles())


class DisplayHistoryCommand(ICommand):

    def __init__(self, logger):
        self.logger = logger

    def execute(self):
        article_id = input("Podaj numer rzeczy by wyswietlic historie :> ")
        IOWrapper.print_article_log(self.logger.get_borrow_history(article_id))


class AddArticleCommand(ICommand):

    def __init__(self, base, logger, app_info_logger):
        self.base = base
        self.logger = logger
        self.app_info_logger = app_info_logger

    def execute(self):
        new_name = input("Nazwa?: ")
        new_name2 = input("Name?: ")
        new_id = self.logger.get_available_id()
        new_obj = Article(new_id, [new_name, new_name2], True)

        self.base.add_article(new_obj)
        self.logger.add_log(new_id, Log(str(datetime.date(datetime.now())), "Added"))
        self.app_info_logger.log_info("Dodano nowy artykul")
        IOWrapper.continue_pause()


class DeleteArticleCommand(ICommand):

    def __init__(self, base, logger, app_info_logger):
        self.base = base
        self.logger = logger
        self.app_info_logger = app_info_logger

    def execute(self):
        rm_id = input("Podaj ID artykulu do usuniecia:\nID?: ")

        if self.base.remove_article_by_id(rm_id):
            self.logger.add_log(rm_id, Log(str(datetime.date(datetime.now())), "Deleted"))
            self.app_info_logger.log_info(f"Usunieto artykul o ID = {rm_id}")
        else:
            self.app_info_logger.log_info(f"Brak artykulu o ID = {rm_id}")

        IOWrapper.continue_pause()


class SearchForAnArticleByNameCommand(ICommand):

    def __init__(self, base):
        self.base = base

    def execute(self):
        src_name = input("Podaj nazwe artykulu :\nName?: ")
        IOWrapper.print_articles(self.base.get_articles_by_name(src_name))


class SearchForAnArticleByIdCommand(ICommand):

    def __init__(self, base, app_info_logger):
        self.base = base
        self.app_info_logger = app_info_logger

    def execute(self):
        src_id = input("Podaj ID artykulu:\nID?: ")

        article = self.base.get_article_by_id(src_id)
        if article:
            IOWrapper.print_articles([article])
        else:
            self.app_info_logger.log_info("Brak artykulu o takim ID!")
            IOWrapper.continue_pause()


class ChangeStatusCommand(ICommand):

    def __init__(self, base, logger, app_info_logger):
        self.base = base
        self.logger = logger
        self.app_info_logger = app_info_logger

    def execute(self):
        obj_id = input("Podaj ID elementu do zmiany statusu\nID?: ")
        obj_article = self.base.get_article_by_id(obj_id)

        if obj_article:
            state = 'jest' if obj_article.is_available else 'nie jest'
            print(f'Atrykul obecnie {state} dostepny. Czy chcesz zmienic jego status?')
            status = input("1: Tak\n2: Nie\n Wybierz cyfre: ")

            if status == '1':
                new_obj = self.base.change_article_availability(obj_id, not obj_article.is_available)
                if new_obj:
                    self.base.remove_article_by_id(obj_id)
                    self.base.add_article(new_obj)
                    if obj_article.is_available:
                        self.logger.add_log(obj_id, Log(str(datetime.date(datetime.now())), "Borrowed"))
                    else:
                        self.logger.add_log(obj_id, Log(str(datetime.date(datetime.now())), "Returned"))
            elif status == '2':
                ""
            else:
                self.app_info_logger.log_info("Nalezalo wybrac 1 lub 2!")
                IOWrapper.continue_pause()
        else:
            self.app_info_logger.log_info("Nieprawidlowy id produktu")
            IOWrapper.continue_pause()


class DisplayConfigCommand(ICommand):

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def execute(self):
        print("Aktualna konfiguracja:")
        config_attributes = self.config_manager.__dict__

        for key, val in config_attributes.items():
            print(f'{key}: "{val}"')

        IOWrapper.continue_pause()


class ChangeConfigCommand(ICommand):

    def __init__(self, config_manager, app_info_logger):
        self.config_manager = config_manager
        self.app_info_logger = app_info_logger

    def execute(self):
        config_attributes = list()

        for key, val in self.config_manager.__dict__.items():
            config_attributes.append(key)

        print("Zmiana konfiguracji")
        for index, val in enumerate(config_attributes):
            print(f'{index + 1}: "{val}"')

        index = input("Wybierz atrybut do zmiany: ")
        if len(config_attributes) >= int(index) > 0:
            new_value = input("Podaj nowa wartosc: ")
            setattr(self.config_manager, config_attributes[int(index) - 1], new_value)
            self.app_info_logger.log_info("Atrybut zostal zmieniony!")
        else:
            self.app_info_logger.log_info("Brak takiego atrybutu!")

        IOWrapper.continue_pause()


class SaveConfigCommand(ICommand):

    def __init__(self, config_manager, app_info_logger):
        self.config_manager = config_manager
        self.app_info_logger = app_info_logger

    def execute(self):
        self.config_manager.save_configuration()
        self.app_info_logger.log_info("Zapisano konfiguracje!")
        IOWrapper.continue_pause()


class DisplayAllNotAvailableArticlesCommand(ICommand):

    def __init__(self, base):
        self.base = base

    def execute(self):
        IOWrapper.print_articles(self.base.get_articles_by_availability(False))


class DisplayFullHistoryCommand(ICommand):

    def __init__(self, logger):
        self.logger = logger

    def execute(self):
        IOWrapper.print_articles_log(self.logger.get_all_logs())


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
        self._commands = {'1': DisplayAllArticlesCommand(self.base),
                          '2': DisplayAllNotAvailableArticlesCommand(self.base),
                          '3': DisplayFullHistoryCommand(self.logger),
                          '4': DisplayHistoryCommand(self.logger),
                          '5': AddArticleCommand(self.base, self.logger, self.app_info_logger),
                          '6': DeleteArticleCommand(self.base, self.logger, self.app_info_logger),
                          '7': SearchForAnArticleByNameCommand(self.base),
                          '8': SearchForAnArticleByIdCommand(self.base, self.app_info_logger),
                          '9': ChangeStatusCommand(self.base, self.logger, self.app_info_logger),
                          '10': DisplayConfigCommand(self.config_manager),
                          '11': ChangeConfigCommand(self.config_manager, self.app_info_logger),
                          '12': SaveConfigCommand(self.config_manager, self.app_info_logger),
                          '0': StopApp(self.app_info_logger)}

    def execute(self, command_name):
        if command_name in self._commands.keys():
            self._commands[command_name].execute()
        else:
            self.app_info_logger.log_error("Podano nieprawidlowy numer!")
            IOWrapper.continue_pause()
