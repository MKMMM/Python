my_input = int(input())
my_list = []
x = 0
factorial = 1

while x in range(my_input):
    my_list.append(x + 1)
    factorial = factorial * my_list[x]
    x += 1
print(factorial)
