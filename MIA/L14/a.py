import math

highest_num = max(list(map(int, input().split())))
a = len(range(highest_num, 7))

gcd_num = math.gcd(a, 6)
print(int(a/gcd_num), int(6/gcd_num), sep='/')