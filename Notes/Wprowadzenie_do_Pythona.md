
# Wprowadzenie do Pythona

## Czym jest Python?

Python jest wszechstronnym, interpretowanym językiem programowania wysokiego poziomu, który jest znany ze swojej czytelności oraz prostoty składni. Jest używany do różnych zastosowań, takich jak web development, analiza danych, sztuczna inteligencja, automatyzacja, i wiele innych.

## Instalacja Pythona

Aby rozpocząć pracę z Pythonem, należy go najpierw zainstalować. Możesz pobrać najnowszą wersję z oficjalnej strony [python.org](https://www.python.org/).

### Instalacja na Windows

1. Pobierz instalator ze strony [python.org](https://www.python.org/downloads/).
2. Uruchom instalator i zaznacz opcję "Add Python to PATH".
3. Postępuj zgodnie z instrukcjami instalatora.

### Instalacja na macOS

1. Pobierz instalator ze strony [python.org](https://www.python.org/downloads/).
2. Uruchom instalator i postępuj zgodnie z instrukcjami.

### Instalacja na Linux

Na większości dystrybucji Linux, Python jest już zainstalowany. Możesz sprawdzić wersję Pythona za pomocą polecenia:

```sh
python3 --version
```

Jeśli nie masz Pythona zainstalowanego, możesz go zainstalować używając menedżera pakietów, np.:

```sh
sudo apt-get install python3
```

## Podstawowa składnia

### Hello, World!

Najbardziej podstawowy program w Pythonie to "Hello, World!".

```python
print("Hello, World!")
```

### Zmienne

Zmienne w Pythonie nie wymagają deklaracji typu. Typ jest przypisywany dynamicznie.

```python
x = 5
y = "Hello"
```

### Komentarze

Komentarze w Pythonie są oznaczane znakiem `#`. Można ich używać do dodawania notatek i wyjaśnień do kodu.

```python
# To jest komentarz
print("Hello, World!")  # To jest komentarz w linii kodu
```

### Wielolinijkowe komentarze

Wielolinijkowe komentarze można tworzyć za pomocą potrójnych cudzysłowów.

```python
'''
To jest
wielolinijkowy
komentarz
'''
```

### Indentacja

Indentacja w Pythonie jest bardzo ważna, ponieważ określa blok kodu. W przeciwieństwie do wielu innych języków programowania, Python nie używa nawiasów klamrowych do określenia bloków kodu, a zamiast tego używa wcięć (spacji lub tabulatorów).

#### Przykład:

```python
if x > 0:
    print("x jest dodatnie")
    if x > 10:
        print("x jest większe niż 10")
else:
    print("x jest ujemne lub zerowe")
```

### Podstawowe operatory

Python obsługuje różne operatory arytmetyczne, porównania, logiczne oraz przypisania.

#### Przykład operatorów arytmetycznych:

```python
a = 10
b = 3
sum = a + b
difference = a - b
product = a * b
quotient = a / b
modulus = a % b
```

#### Przykład operatorów porównania:

```python
is_equal = (a == b)
is_not_equal = (a != b)
is_greater = (a > b)
is_less = (a < b)
is_greater_equal = (a >= b)
is_less_equal = (a <= b)
```

#### Przykład operatorów logicznych:

```python
result_and = (a > b) and (b < 5)
result_or = (a > b) or (b > 5)
result_not = not (a > b)
```

### Struktury danych

Python ma różne wbudowane struktury danych, takie jak listy, krotki, słowniki i zbiory.

#### Lista:

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
first_fruit = fruits[0]
```

#### Krotka:

```python
coordinates = (10.0, 20.0)
x_coord = coordinates[0]
```

#### Słownik:

```python
person = {"name": "Alice", "age": 25}
person["city"] = "Warszawa"
name = person["name"]
```

#### Zbiór:

```python
colors = {"red", "green", "blue"}
colors.add("yellow")
```

## Podsumowanie

W tej sekcji omówiliśmy podstawy Pythona, w tym instalację, podstawową składnię, komentarze, indentację oraz struktury danych. Python jest potężnym językiem programowania, który jest łatwy do nauki i wszechstronny w zastosowaniach.
