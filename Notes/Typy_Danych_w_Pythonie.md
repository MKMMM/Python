
# Typy Danych w Pythonie

## Zmienne

Zmienne w Pythonie służą do przechowywania danych. Można je deklarować i przypisywać im wartości za pomocą operatora `=`.

### Przykład:

```python
x = 5
y = "Hello"
z = True
```

## Typy danych

### Numbers (Liczby)

Python obsługuje różne typy liczbowe, takie jak `int` (całkowite), `float` (zmiennoprzecinkowe), oraz `complex` (zespolone).

#### Przykład:

```python
a = 10       # int
b = 3.14     # float
c = 1 + 2j   # complex
```

### Strings (Napisy)

Napisy w Pythonie to sekwencje znaków ujęte w cudzysłowy pojedyncze lub podwójne.

#### Przykład:

```python
text = "Hello, World!"
```

Możemy wykonywać różne operacje na napisach, takie jak konkatenacja, indeksowanie, czy slicing.

```python
first_char = text[0]
substring = text[0:5]
```

### Boolean (Wartości logiczne)

Typ `bool` w Pythonie może przyjmować dwie wartości: `True` lub `False`.

#### Przykład:

```python
is_active = True
is_deleted = False
```

### Operators (Operatory)

Operatory służą do wykonywania różnych operacji na zmiennych i wartościach.

#### Przykład:

```python
# Operator arytmetyczny
sum = 5 + 3

# Operator porównania
is_equal = (5 == 3)

# Operator logiczny
result = True and False
```

### Lists (Listy)

Listy to uporządkowane sekwencje elementów, które mogą być różnych typów. Listy są modyfikowalne (mutable).

#### Przykład:

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
```

### Sets (Zbiory)

Zbiory to nieuporządkowane kolekcje unikalnych elementów.

#### Przykład:

```python
colors = {"red", "green", "blue"}
colors.add("yellow")
```

### Tuples (Krotki)

Krotki są podobne do list, ale są niemodyfikowalne (immutable).

#### Przykład:

```python
coordinates = (10.0, 20.0)
```

### Dictionaries (Słowniki)

Słowniki przechowują pary klucz-wartość. Klucze muszą być unikalne i niemodyfikowalne.

#### Przykład:

```python
person = {"name": "Alice", "age": 25}
person["city"] = "Warszawa"
```

## Data Casting (Rzutowanie danych)

Rzutowanie danych to proces konwersji jednego typu danych na inny. Python umożliwia rzutowanie między różnymi typami za pomocą funkcji wbudowanych.

### Przykład:

```python
# Konwersja int na float
a = 5
b = float(a)

# Konwersja float na int
c = 3.14
d = int(c)

# Konwersja string na int
e = "123"
f = int(e)

# Konwersja int na string
g = 456
h = str(g)
```

## Podsumowanie

W tej sekcji omówiliśmy różne typy danych w Pythonie oraz sposób ich rzutowania. Zrozumienie tych podstawowych typów danych jest kluczowe do efektywnego programowania w Pythonie.
