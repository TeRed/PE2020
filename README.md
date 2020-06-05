# Wypożyczalnia artykułów

Projekt na zajęcia z Programowania Ekstremalnego 2020

### Przed uruchomieniem

Do aplikacji potrzebny python w wersji 3

Do testów akceptacyjncyh potrzebny framework Lettuce:
```
pip install git+https://github.com/wixb50/lettuce.git
```

## Na początek

Sklonuj repozytorium:

```
git clone https://github.com/arturmen/PE2020.git
```

następnie:

```
cd PE2020

cd app
```

## Zwykłe uruchomienie

uruchom aplikację:

```
python main.py
```

aby korzystać z aplikacji wybieraj opcję wpisując numer i klikając enter
## Uruchomienie testow jednostkowych
uruchomienie wszystkich testów na raz:

```
python -m unittest
```

uruchomienie jednego testu w jednym czasie:

```
python <nazwa pliku z testem>
```

np:
```
python test_article.py
```

## Uruchomienie testow akceptacyjnych

Jeśli nie jest zainstalowany lettuce:

```
pip install git+https://github.com/wixb50/lettuce.git
```

w katalogu app należy uruchomić:

```
lettuce
```
