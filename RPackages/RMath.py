def is_prime(n):   
    if n==1:
        return False
    elif n==2:
        return True
    elif n!=2:
        for i in range(2,n):
            if n%i==0:
                return False
        if i==(n-1):
            return True
    
def is_even(n):
    if n%2==0:
        return True
    else:
        return False

def cube_cuboid_volume_surface_area_finder(l,b,h,un):
    volume=l*b*h
    surface_area=h*l*2+h*b*2+l*b*2
    print(f'volume is {volume}{un} to the power of 3')
    print(f'surface area is {surface_area}{un} to the power of 2')