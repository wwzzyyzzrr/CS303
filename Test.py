import copy

list1 = [1,2,3,4,5]
list2 = copy.deepcopy(list1)
list1.clear()
print(list2)

a = 1
b = -a
print(b)