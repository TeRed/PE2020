from abc import ABCMeta

from article import Article
from log import Log
from datetime import datetime
import os


class Interface:
    global run

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
        global run
        run = True
        self.app_info_logger.log_start()

        INVOKER = Invoker(self.base, self.logger, self.config_manager, self.app_info_logger)

        while run:
            input("Naciśnij Enter, aby kontynować")
            self.cls()
            print("\tWypożyczalnia rzeczy\n\tProsze wybrać numer:")

            choice = input('''
           1: Wypisz liste wszystkich artykułów
           2: Wypisz listę wypożyczonych artykułów
           3: Wyświetl pełną historię wypożyczeń
           4: Wypisz historię wypożyczeń artykułu
           5: Dodaj artykuł
           6: Usuń artykuł
           7: Wyszukaj artykuł po nazwie
           8: Wyszukaj artykuł po id
           9: Zmień status wypożyczenia
           10: Aktualna konfiguracja
           11: Zmiana konfiguracji
           12: Zapisz aktualną konfigurację aplikacji
           0: Wyjdz z aplikacji
           ''')
            self.cls()
            INVOKER.execute(choice)


class AppInfoLogger:
    info_title = ""
    info_divider = ""

    def __init__(self):
        self.info_title = "INFO"
        self.info_divider = ": "

    def log_start(self):
        print(self.info_title + self.info_divider + 'Aplikacja została uruchomiona.')

    def log_end(self):
        print(self.info_title + self.info_divider + 'Aplikacja została zatrzymana.')

    def log_error(self, text):
        print(self.info_title + self.info_divider + 'W aplikacji wystąpił błąd. ERROR: ' + text)


class ICommand(metaclass=ABCMeta):

    @staticmethod
    def execute():
        """The required execute method which all command obejcts will use"""


class DisplayAllArticlesCommand(ICommand):

    def __init__(self, base):
        self.base = base

    def execute(self):
        print("Lista wszystkich artykułów:")
        print("ID", '\t', "NAZWA", '\t', "DOSTĘPNOSC")
        for articles in self.base.get_all_articles():
            print(articles.id, '\t', articles.name, '\t', articles.is_available)


class DisplayHistoryCommand(ICommand):

    def __init__(self, logger):
        self.logger = logger

    def execute(self):
        article_id = input("Podaj numer rzeczy by wyświetlić historię :> ")

        logs = self.logger.get_borrow_history(article_id)
        for obj in logs:
            print("date: " + obj.data + "\tmsg: " + obj.text)


class AddArticleCommand(ICommand):

    def __init__(self, base, logger):
        self.base = base
        self.logger = logger

    def execute(self):
        new_id = input("Dodawanie nowego artykułu:\nID?: ")
        new_name = input("Name?: ")
        new_obj = Article(new_id, new_name, True)

        self.base.add_article(new_obj)
        self.logger.add_log(new_id, Log(str(datetime.date(datetime.now())), "Added"))
        print("Dodano nowy artykuł")


class DeleteArticleCommand(ICommand):

    def __init__(self, base, logger):
        self.base = base
        self.logger = logger

    def execute(self):
        rm_id = input("Podaj ID artykułu do usunięcia:\nID?: ")

        self.base.remove_article_by_id(rm_id)
        self.logger.add_log(rm_id, Log(str(datetime.date(datetime.now())), "Deleted"))
        print("Usunięto artykuł o ID =", rm_id)


class SearchForAnArticleByNameCommand(ICommand):

    def __init__(self, base):
        self.base = base

    def execute(self):
        src_name = input("Podaj nazwę artykułu :\nName?: ")

        for articles in self.base.get_articles_by_name(src_name):
            print(articles.id, '\t', articles.name, '\t', articles.is_available)


class SearchForAnArticleByIdCommand(ICommand):

    def __init__(self, base):
        self.base = base

    def execute(self):
        src_id = input("Podaj ID artykułu:\nID?: ")

        articles = self.base.get_article_by_id(src_id)
        if articles:
            print(articles.id, '\t', articles.name, '\t', articles.is_available)
        else:
            print("Brak artykułu o takim ID!")


class ChangeStatusCommand(ICommand):

    def __init__(self, base, logger):
        self.base = base
        self.logger = logger

    def execute(self):
        obj_id = input("Podaj ID elementu do zmiany statusu\nID?: ")
        obj_article = self.base.get_article_by_id(obj_id)

        if obj_article:
            state = 'jest' if obj_article.is_available else 'nie jest'
            print(f'Atrykuł obecnie {state} dostępny. Czy chcesz zmienić jego status?')
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
                self.app_info_logger.log_error("Należało wybrać 1 lub 2!")
        else:
            self.app_info_logger.log_error("Nieprawidłowy id produktu")


class DisplayConfigCommand(ICommand):

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def execute(self):
        print("Aktualna konfiguracja:")
        config_attributes = self.config_manager.__dict__

        for key, val in config_attributes.items():
            print(f'{key}: "{val}"')


class ChangeConfigCommand(ICommand):

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def execute(self):
        config_attributes = list()

        for key, val in self.config_manager.__dict__.items():
            config_attributes.append(key)

        print("Zmiana konfiguracji")
        for index, val in enumerate(config_attributes):
            print(f'{index + 1}: "{val}"')

        index = input("Wybierz atrybut do zmiany: ")
        new_value = input("Podaj nową wartość: ")

        setattr(self.config_manager, config_attributes[int(index) - 1], new_value)

        print("Atrybut został zmieniony!")


class SaveConfigCommand(ICommand):

    def __init__(self, config_manager):
        self.config_manager = config_manager

    def execute(self):
        self.config_manager.save_configuration()


class DisplayAllNotAvailableArticlesCommand(ICommand):

    def __init__(self, base):
        self.base = base

    def execute(self):
        print("Lista wszystkich wypożyczonych artykułów:")
        print("ID", '\t', "NAZWA", '\t', "DOSTĘPNOSC")
        for articles in self.base.get_articles_by_availability(False):
            print(articles.id, '\t', articles.name, '\t', articles.is_available)


class DisplayFullHistoryCommand(ICommand):

    def __init__(self, logger):
        self.logger = logger

    def execute(self):
        print("Pełna historia wypożyczeń:")

        article_logs = self.logger.get_all_logs()

        print("ID", '\t', "DATA", '\t\t', "TEXT")
        for article_log in article_logs:
            logs = [it for it in article_log.logs if it.text == 'Borrowed' or it.text == 'Returned']
            for log in logs:
                print(article_log.id, '\t', log.data, '\t', log.text)


class StopApp(ICommand):

    def __init__(self, app_info_logger):
        self.app_info_logger = app_info_logger

    def execute(self):
        global run
        run = False
        self.app_info_logger.log_end()


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
                          '5': AddArticleCommand(self.base, self.logger),
                          '6': DeleteArticleCommand(self.base, self.logger),
                          '7': SearchForAnArticleByNameCommand(self.base),
                          '8': SearchForAnArticleByIdCommand(self.base),
                          '9': ChangeStatusCommand(self.base, self.logger),
                          '10': DisplayConfigCommand(self.config_manager),
                          '11': ChangeConfigCommand(self.config_manager),
                          '12': SaveConfigCommand(self.config_manager),
                          '0': StopApp(self.app_info_logger)}

    def execute(self, command_name):
        if command_name in self._commands.keys():
            self._commands[command_name].execute()
        else:
            self.app_info_logger.log_error("Podano nieprawidłowy numer!")
