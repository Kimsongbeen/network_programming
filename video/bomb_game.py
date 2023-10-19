arr = []

N = int(input("N:"))

for i in range(N):
    min_map = input(":")
    arr.append(list(map(int, min_map.split())))

for i in range(N):
    print(arr[i])

answer = [['*' if arr[i][j] == 1 else 0 for j in range(N)] for i in range(N)]

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

for i in range(N):
    for j in range(N):
        if arr[i][j] == 0:
            for dx, dy in directions:
                nx, ny = i + dx, j + dy
                if 0 <= nx < N and 0 <= ny < N and arr[nx][ny] == 1:
                    answer[i][j] += 1

for i in range(N):
    print(answer[i])