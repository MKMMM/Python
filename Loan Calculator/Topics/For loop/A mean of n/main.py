my_numbers = []
total = 0
number_of_inputs = int(input())

for _ in range(number_of_inputs):
    my_input = int(input())
    my_numbers.append(my_input)
print(sum(my_numbers) / number_of_inputs)
