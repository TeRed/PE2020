class Main:
    def __init__(self):
        self.contributors = ["Przemysław Filipek", "Jan Kowalski"]

    def __str__(self):
        return "Contributors list:\n{}".format("\n".join(self.contributors))


obj = Main()
print(obj)
