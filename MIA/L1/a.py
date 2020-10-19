n = int(input())
moves = input()
positions_array = list(map(int, input().split()))
winner = float('+inf')
collision_time = None

for i in range(1, n):
    if moves[i-1] == 'R' and moves[i] == 'L':
        collision_time = abs(positions_array[i-1] - positions_array[i]) / 2
        if collision_time < winner:
            winner = collision_time

if collision_time is None:
    print(-1)
else:
    print(int(winner))
