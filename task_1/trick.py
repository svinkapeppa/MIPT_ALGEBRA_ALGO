n = int(input())

for k in range(0, n):
    level = 3 * n + 12 * k
    print('GATE {} NOT {}'.format(level, k))
    print('GATE {} OR {} {}'.format(level + 1, n + k, 2 * n + k))
    print('GATE {} AND {} {}'.format(level + 2, n + k, 2 * n + k))
    print('GATE {} NOT {}'.format(level + 3, level + 1))
    print('GATE {} AND {} {}'.format(level + 4, k, level + 1))
    print('GATE {} NOT {}'.format(level + 5, level + 2))
    print('GATE {} OR {} {}'.format(level + 6, level + 3, level + 2))
    print('GATE {} OR {} {}'.format(level + 7, level + 4, level + 2))
    print('GATE {} AND {} {}'.format(level + 8, level + 1, level + 5))
    print('GATE {} OR {} {}'.format(level + 9, level, level + 6))
    print('GATE {} OR {} {}'.format(level + 10, k, level + 8))
    print('GATE {} AND {} {}'.format(level + 11, level + 9, level + 10))

print('GATE {} AND {} {}'.format(15 * n, 0, 3 * n))

for k in range(0, n):
    level = 3 * n + 12 * k
    print('OUTPUT {} {}'.format(k, level + 11))

print('OUTPUT {} {}'.format(n, 15 * n))
print('OUTPUT {} {}'.format(n + 1, 15 * n))

for k in range(0, n):
    level = 3 * n + 12 * k
    print('OUTPUT {} {}'.format(n + k + 2, level + 7))
