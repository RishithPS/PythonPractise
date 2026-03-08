x=[1,2,3,4]

def square(x):
    lst=[]
    for i in x:
        lst.append(i*i)
    return lst
def cube(x):
    lst=[]
    for i in x:
        lst.append(i*i*i)
    return lst
print(square(x))
print(cube(x))