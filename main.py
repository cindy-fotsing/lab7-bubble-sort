list = [4,1,3,10,5,16,2]
for i in range(len(list)):
    for j in range(len(list) - 1):
        if list[j] > list [j + 1] :
            list[j],list[j+1] = list[j+1], list[j]

print(list)