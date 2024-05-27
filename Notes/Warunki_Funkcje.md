
# Intro do Pythona

## Warunki (if else)

Warunki w Pythonie pozwalają na wykonywanie różnych bloków kodu w zależności od spełnienia określonych warunków. Najbardziej podstawowe użycie to `if`, `elif` oraz `else`.

### Przykład:

```python
x = 10

if x > 0:
    print("x jest dodatnie")
elif x == 0:
    print("x jest zerem")
else:
    print("x jest ujemne")
```

Wynik: `x jest dodatnie`

### Przykład z więcej niż jednym warunkiem:

```python
y = 7

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

while count < 5:
    print(count)
    count += 1
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

while n > 0:
    print(n)
    n -= 1
    if n == 5:
        break
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
    return f"Hello, {name}!"

# Korzystanie z funkcji
print(greet("Alice"))
```

Wynik: `Hello, Alice!`

### Funkcja z wieloma argumentami

#### Przykład:

```python
def add(a, b):
    return a + b

# Korzystanie z funkcji
result = add(3, 4)
print(result)
```

Wynik: `7`

### Funkcje z wartościami domyślnymi

#### Przykład:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

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
    return sum(args)

# Korzystanie z funkcji
print(summarize(1, 2, 3, 4))
```

Wynik: `10`

### Funkcja z argumentami kluczowymi

#### Przykład:

```python
def describe_person(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# Korzystanie z funkcji
describe_person(name="Alice", age=25, city="Warszawa")
```

Wynik:
```
name: Alice
age: 25
city: Warszawa
```

## Podsumowanie

W tej sekcji omówiliśmy podstawowe konstrukcje programistyczne w Pythonie, takie jak warunki, pętle oraz funkcje. Dzięki tym narzędziom możemy tworzyć złożone programy w sposób bardziej uporządkowany i efektywny.
