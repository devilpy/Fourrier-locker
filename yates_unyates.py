# Fisher_yates shuffle
def yates(a,b):
    for ind in b:
        if ind >= len(a):
            x = ind%len(a)
            a.append(a[x])
        else:
            x = ind
            a.append(a[x])
        for i in range(x,len(a)-1):
            a[i] = a[i+1]
        a.pop()
        # print(a)
    return a


#decrypt yates (going backwards!)

def un_yates(a,b):
    b.reverse()
    for ind in b:
        c = a[-1]
        if ind >= len(a):
            x = ind%len(a)
        else:
            x = ind
        for i in range(len(a) - 2 , x-1, -1):
            a[i+1] = a[i]
        a[x] = c
    return a