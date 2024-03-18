var = 10 
for i in range(10):
    for j in range(2, 10, 1):
        if var % 2 != 0:
            print(var)
            continue 
            var += 2 
    print(var)
    var += 2 

else:
    var+= 1

print("Result:", var)