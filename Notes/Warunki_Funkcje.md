
# Intro do Pythona

## Warunki (if else)

Warunki w Pythonie pozwalają na wykonywanie różnych bloków kodu w zależności od spełnienia określonych warunków. Najbardziej podstawowe użycie to `if`, `elif` oraz `else`.

### Przykład:

```python
x = 10

# Sprawdzamy, czy x jest większe od 0
if x > 0:
    print("x jest dodatnie")
# Sprawdzamy, czy x jest równe 0
elif x == 0:
    print("x jest zerem")
# Jeśli powyższe warunki nie są spełnione, to x jest ujemne
else:
    print("x jest ujemne")
```

Wynik: `x jest dodatnie`

### Przykład z więcej niż jednym warunkiem:

```python
y = 7

# Sprawdzamy, czy y jest parzyste
if y % 2 == 0:
    print("y jest parzyste")
else:
    print("y jest nieparzyste")
```

Wynik: `y jest nieparzyste`

## Pętle

### Pętla `while`

Pętla `while` wykonuje blok kodu tak długo, jak warunek jest spełniony.

#### Przykład:

```python
count = 0

# Pętla wykonuje się, dopóki count jest mniejsze od 5
while count < 5:
    print(count)
    count += 1  # Zwiększamy wartość count o 1
```

Wynik:
```
0
1
2
3
4
```

### Przykład z warunkiem przerwania:

```python
n = 10

# Pętla wykonuje się, dopóki n jest większe od 0
while n > 0:
    print(n)
    n -= 1  # Zmniejszamy wartość n o 1
    if n == 5:
        break  # Przerywamy pętlę, gdy n jest równe 5
```

Wynik:
```
10
9
8
7
6
```

### Pętla `for`

Pętla `for` w Pythonie służy do iteracji po elementach sekwencji (np. lista, krotka, string) lub innych iterowalnych obiektach.

#### Przykład:

```python
# Iterujemy od 0 do 4
for i in range(5):
    print(i)
```

Wynik:
```
0
1
2
3
4
```

#### Przykład iteracji po liście:

```python
fruits = ["jabłko", "banan", "wiśnia"]

# Iterujemy po elementach listy
for fruit in fruits:
    print(fruit)
```

Wynik:
```
jabłko
banan
wiśnia
```

### Przykład iteracji po słowniku:

```python
person = {"name": "Alice", "age": 25, "city": "Warszawa"}

# Iterujemy po kluczach i wartościach słownika
for key, value in person.items():
    print(f"{key}: {value}")
```

Wynik:
```
name: Alice
age: 25
city: Warszawa
```

## Funkcje

Funkcje w Pythonie pozwalają na grupowanie kodu w moduły, które mogą być wielokrotnie używane. Definicja funkcji zaczyna się od słowa kluczowego `def`.

### Definicja i korzystanie z funkcji

#### Przykład:

```python
def greet(name):
    return f"Hello, {name}!"  # Zwracamy sformatowany napis

# Korzystanie z funkcji
print(greet("Alice"))
```

Wynik: `Hello, Alice!`

### Funkcja z wieloma argumentami

#### Przykład:

```python
def add(a, b):
    return a + b  # Zwracamy sumę dwóch argumentów

# Korzystanie z funkcji
result = add(3, 4)
print(result)
```

Wynik: `7`

### Funkcje z wartościami domyślnymi

#### Przykład:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"  # Zwracamy sformatowany napis z domyślnym przywitaniem

# Korzystanie z funkcji z wartością domyślną
print(greet("Alice"))
print(greet("Bob", "Hi"))
```

Wynik:
```
Hello, Alice!
Hi, Bob!
```

### Funkcja z listą argumentów

#### Przykład:

```python
def summarize(*args):
    return sum(args)  # Zwracamy sumę wszystkich argumentów

# Korzystanie z funkcji
print(summarize(1, 2, 3, 4))
```

Wynik: `10`

### Funkcja z argumentami kluczowymi

#### Przykład:

```python
def describe_person(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")  # Wypisujemy każdą parę klucz-wartość

# Korzystanie z funkcji
describe_person(name="Alice", age=25, city="Warszawa")
```

Wynik:
```
name: Alice
age: 25
city: Warszawa
```

### Funkcje geometryczne

#### Przykład funkcji liczącej pole kwadratu:

```python
def pole_kwadratu(bok):
    return bok ** 2  # Zwracamy pole kwadratu (bok do kwadratu)

# Korzystanie z funkcji
print(pole_kwadratu(4))
```

Wynik: `16`

#### Przykład funkcji liczącej pole prostokąta:

```python
def pole_prostokata(dlugosc, szerokosc):
    return dlugosc * szerokosc  # Zwracamy pole prostokąta (długość razy szerokość)

# Korzystanie z funkcji
print(pole_prostokata(5, 3))
```

Wynik: `15`

#### Przykład funkcji liczącej pole trójkąta:

```python
def pole_trojkata(podstawa, wysokosc):
    return 0.5 * podstawa * wysokosc  # Zwracamy pole trójkąta (0.5 razy podstawa razy wysokość)

# Korzystanie z funkcji
print(pole_trojkata(6, 4))
```

Wynik: `12.0`

### Funkcje związane z finansami

#### Przykład funkcji liczącej prostą stopę procentową:

```python
def prosta_stopa_procentowa(kapital, stopa, czas):
    return kapital * (1 + stopa * czas)  # Zwracamy wartość końcową kapitału z prostą stopą procentową

# Korzystanie z funkcji
print(prosta_stopa_procentowa(1000, 0.05, 3))
```

Wynik: `1150.0`

#### Przykład funkcji liczącej złożoną stopę procentową:

```python
def zlozona_stopa_procentowa(kapital, stopa, czas, czestotliwosc):
    return kapital * (1 + stopa / czestotliwosc) ** (czestotliwosc * czas)  # Zwracamy wartość końcową kapitału z złożoną stopą procentową

# Korzystanie z funkcji
print(zlozona_stopa_procentowa(1000, 0.05, 3, 4))
```

Wynik: `1161.181`
 

# Choinka w Pythonie

Ta funkcja drukuje prostą choinkę z znakami "*" i jednym znakiem "#" jako pień. Funkcja przyjmuje parametr `height`, który oznacza wysokość choinki.

```python
def drukuj_choinke(height):
    # Funkcja do drukowania prostej choinki z znakami "*"
    # i jednym znakiem "#" na dole jako pień.
    
    # Parametry:
    # height (int): Wysokość choinki (liczba poziomów).
    
    # Przechodzimy przez każdy poziom choinki
    for index in range(height):
        # Drukuj wycentrowane spacje
        # Numer spacji do wydrukowania to (height - indeks - 1)
        print(' ' * (height - index - 1), end='')
        
        # Drukuj liczbe "*" dla danego poziomu (indeks)
        # Liczba "*" do wydrukowania to (2 * indeks + 1)
        print('*' * (2 * index + 1))
    
    # Drukuj pieniek na dole
    # Pieniek jest na środku, wiec wydrukuj (height - 1) spacji oraz symbol "#"
    print(' ' * (height - 1) + '#')

# Korzystanie z Funkcji:
drukuj_choinke(5)

# Przykład wyniku:

    *
   ***
  *****
 *******
*********
    #

# Analiza wyniku:

    *       (4 spacje + 1 gwiazdka)
   ***      (3 spacje + 3 gwiazdki)
  *****     (2 spacje + 5 gwiazdek)
 *******    (1 spacja + 7 gwiazdek)
*********   (0 spacji + 9 gwiazdek)
    #       (4 spacje + 1 hash)


## Podsumowanie

W tej sekcji omówiliśmy podstawowe konstrukcje programistyczne w Pythonie, takie jak warunki, pętle oraz funkcje. Dzięki tym narzędziom możemy tworzyć złożone programy w sposób bardziej uporządkowany i efektywny.
