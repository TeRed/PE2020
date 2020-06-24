# Wypożyczalnia artykułów

Projekt na zajęcia z Programowania Ekstremalnego 2020

### Przed uruchomieniem

Do aplikacji potrzebny jest Python w wersji >= 3.6

Do testów akceptacyjncyh potrzebny jest framework Lettuce:
```
pip install git+https://github.com/wixb50/lettuce.git
```

## Na początek

Sklonuj repozytorium:

```
git clone https://github.com/arturmen/PE2020.git
```

Następnie:

```
cd PE2020

cd app
```

## Zwykłe uruchomienie

Uruchom aplikację:

```
python main.py
```

aby korzystać z aplikacji wybieraj opcję wpisując numer i klikając enter
## Uruchomienie testów jednostkowych
Komendy należy wywoływać z poziomu katalogu app.

Uruchomienie wszystkich testów na raz:

```
python -m unittest
```

Uruchomienie jednego testu w jednym czasie:

```
python -m unittest tests/<nazwa pliku z testem>
```

np:
```
python -m unittest tests/test_article.py
```

## Uruchomienie testów akceptacyjnych
Komendy należy wywoływać z poziomu katalogu app.

Jeśli nie jest zainstalowany lettuce:

```
pip install git+https://github.com/wixb50/lettuce.git
```

Uruchomienie wszystkich testów na raz:

```
lettuce
```

Uruchomienie jednego testu w jednym czasie:

```
lettuce features/<nazwa pliku z testem>
```

np:
```
lettuce features/add_article.feature
```
