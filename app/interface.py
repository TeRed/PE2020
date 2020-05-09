from db_connector import DBConnector
from logger_connector import LoggerConnector
from article import Article
from os import system


class Interface:

    def __init__(self):
        pass

    def printInfo(self, text):
        print("INFO: " + text)

    def menu(self):
        base = DBConnector("test_db.json")
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
           0: Wyjdz z aplikacji
           ''')

            if choice == '1':
                print("Lista wszystkich artykułów:")
                print("ID", '\t', "NAZWA", '\t', "DOSTĘPNOSC")
                for articles in base.get_all_articles():
                    print(articles.id, '\t', articles.name, '\t', articles.is_available)

            elif choice == '2':

                article_id = input("\t\t\t\tPodaj numer rzeczy by wyświetlić historię :> ")
                logger = LoggerConnector('test_logger.json')

                logs = logger.get_logs_by_id(str(article_id))
                for obj in logs:
                    for j in obj.logs:
                        print("id: " + j.id + "\t date: " + j.data + "\tmsg: " + j.text)
            
            elif choice == '3':
                new_id = input("Dodawanie nowego artykułu:\nID?: ")
                new_name = input("Name?: ")
                new_obj = Article(new_id, new_name, True)

                base.add_article(new_obj)
                print("Dodano nowy artykuł")
            
            elif choice == '4':
                rm_id = input("Podaj ID artykułu do usunięcia:\nID?: ")

                base.remove_article_by_id(rm_id)
                print("Usunięto artykuł o ID =", rm_id)

            elif choice == '5':
                src_name = input("Podaj nazwę artykułu :\nName?: ")

                for articles in base.get_articles_by_name(src_name):
                    print(articles.id, '\t', articles.name, '\t', articles.is_available)

            elif choice == '6':
                src_id = input("Podaj ID artykułu:\nID?: ")
                
                articles = base.get_article_by_id(src_id)
                if articles:
                    print(articles.id, '\t', articles.name, '\t', articles.is_available)
                else:
                    print("Brak artykułu o takim ID!")

            elif choice == '7':
                obj_id = input("Podaj ID elementu do zmiany statusu\ID?: ")
                status = input("Wybierz status do ustawienia:\n1: Wypożyczone\n2: Dostępne\n?:")
                
                if status == '1':
                    new_obj = base.change_article_availability(obj_id, False)
                    if new_obj:
                        base.remove_article_by_id(obj_id)
                        base.add_article(new_obj)
                elif status == '2':
                    new_obj = base.change_article_availability(obj_id, True)
                    if new_obj:
                        base.remove_article_by_id(obj_id)
                        base.add_article(new_obj)
                else:
                    print("Należało wybrać 1 lub 2!")

            elif choice == '0':
                print("Aplikacja została zamknieta.")
                run = False

            else:
                print("Podano nieprawidłowy numer!")

