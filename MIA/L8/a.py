n, X = list(map(int, input().split()))
 
prices = list(map(int, input().split()))
prices.sort()
 
results = []
N = 0

if prices[0] >= X:
    print(1)
    exit(0)
else:
    results.append(prices[0])

i = 1
while i < n:
    if prices[i] + prices[N] <= X:
        results.append(prices[i])
        N += 1
    else:
        print(N + 1)
        exit(0)
    i += 1
 
print(N + 1)