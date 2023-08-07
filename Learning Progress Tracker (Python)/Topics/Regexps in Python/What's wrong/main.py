import re

w1 = input()
w2 = input()
if not re.match(w1, w2):
    print('no matching')
else:
    print(len(w1) * 2)

