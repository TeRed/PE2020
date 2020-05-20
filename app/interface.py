from article import Article
from datetime import date
from log import Log
from datetime import datetime

class Interface:

    def __init__(self, db_connector, logger_connector, config_manager):
        self.logger = logger_connector
        self.base = db_connector
        self.config_manager = config_manager

    def printInfo(self, text):
        print("INFO: " + text)

    def menu(self):
        run = True
        self.printInfo("app started")

        while (run):
            print("\n\n\t\t\t\tWypożyczalnia rzeczy\n\t\t\t\tProsze wybrać numer:")

            choice = input('''
           1: Wypisz liste wszystkich artykułów
           2: Wypisz historię wypożyczeń
           3: Dodaj artykuł
           4: Usuń artykuł
           5: Wyszukaj artykuł po nazwie
           6: Wyszukaj artykuł po id
           7: Zmień status wypożyczenia
           8: Aktualna konfiguracja
           9: Zmiana konfiguracji
           0: Wyjdz z aplikacji
           ''')

            if choice == '1':
                print("Lista wszystkich artykułów:")
                print("ID", '\t', "NAZWA", '\t', "DOSTĘPNOSC")
                for articles in self.base.get_all_articles():
                    print(articles.id, '\t', articles.name, '\t', articles.is_available)

            elif choice == '2':

                article_id = input("Podaj numer rzeczy by wyświetlić historię :> ")

                logs = self.logger.get_borrow_history(article_id)
                for obj in logs:
                    print("date: " + obj.data + "\tmsg: " + obj.text)
            
            elif choice == '3':
                new_id = input("Dodawanie nowego artykułu:\nID?: ")
                new_name = input("Name?: ")
                new_obj = Article(new_id, new_name, True)

                self.base.add_article(new_obj)
                self.logger.add_log(new_id, Log(str(datetime.date(datetime.now())), "Added"))
                print("Dodano nowy artykuł")
            
            elif choice == '4':
                rm_id = input("Podaj ID artykułu do usunięcia:\nID?: ")

                self.base.remove_article_by_id(rm_id)
                self.logger.add_log(rm_id, Log(str(datetime.date(datetime.now())), "Deleted"))
                print("Usunięto artykuł o ID =", rm_id)

            elif choice == '5':
                src_name = input("Podaj nazwę artykułu :\nName?: ")

                for articles in self.base.get_articles_by_name(src_name):
                    print(articles.id, '\t', articles.name, '\t', articles.is_available)

            elif choice == '6':
                src_id = input("Podaj ID artykułu:\nID?: ")
                
                articles = self.base.get_article_by_id(src_id)
                if articles:
                    print(articles.id, '\t', articles.name, '\t', articles.is_available)
                else:
                    print("Brak artykułu o takim ID!")

            elif choice == '7':
                obj_id = input("Podaj ID elementu do zmiany statusu\ID?: ")
                obj_article = self.base.get_article_by_id(obj_id)

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
                    continue
                else:
                    print("Należało wybrać 1 lub 2!")

            elif choice == '8':
                print("Aktualna konfiguracja:")
                config_attributes = self.config_manager.__dict__

                for key, val in config_attributes.items():
                    print(f'{key}: "{val}"')

            elif choice == '9':
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

            elif choice == '0':
                print("Aplikacja została zamknieta.")
                run = False

            else:
                print("Podano nieprawidłowy numer!")

