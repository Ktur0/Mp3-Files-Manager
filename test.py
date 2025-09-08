n = 4102
for i in range(1,n):
    numStr = str(n - i)
    print(numStr)
    if not('0' in numStr) and not('0' in str(i)):
        print( [i, n - i] )
        break