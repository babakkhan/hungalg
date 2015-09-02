import hungalg

n = int(input())
mat = [list(map(int, input().split())) for _ in range(n)]

ans = hungalg.minimize(mat);
best = sum(mat[i][j] for i,j in ans)
print(best)

