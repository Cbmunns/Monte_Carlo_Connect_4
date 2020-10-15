import random
arr = []

for i in range(45):
    x = random.randrange(0,7)
    arr.append(x)
    
for i in range(len(arr)):
    print(arr[i])