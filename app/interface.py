from app.db_connector import DBConnector
from app.logger_connector import LoggerConnector


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
           3: Wyjdz z aplikacji
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
                print("Aplikacja została zamknieta.")
                run = False

            else:
                print("Podano nieprawidłowy numer!")
