import math



def hex_dist(a0,b0,a1,b1):
    x0 = a0-(b0//2)
    y0 = b0
    x1 = a1-(b1//2)
    y1 = b1
    dx = x1 - x0
    dy = y1 - y0
    distance = max(abs(dx), abs(dy), abs(dx+dy))
    return distance

def euc_dist(a0,b0,a1,b1):
    h = 1
    w = math.sqrt(3)*h/2
    print(w)
    x0 = b0*w
    x1 = b1*w
    y0 = (a0+b0/2)*h
    y1 = (a1+b1/2)*h 
    dist = math.sqrt( (x1-x0)**2 + (y1-y0)**2 )
    return dist

print(euc_dist(0, 0, 1, 1))
print(hex_dist(0, 0, 1, 1))