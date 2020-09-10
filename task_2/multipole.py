def get_ith_bit(bit, number):
    for i in range(bit):
        number //= 2
    return number % 2


def get_initial_set(bit, max_bit, correct=1):
    initial_set = set()

    for k in range(2 ** max_bit):
        if get_ith_bit(bit, k) == correct:
            initial_set.add(k)

    return frozenset(initial_set)


if __name__ == '__main__':
    n = int(input())

    functions = {}
    for i in range(2 ** n + 1):
        functions[i] = {}

    for i in range(n):
        key = get_initial_set(i, n, correct=1)
        functions[2 ** (n - 1)][key] = i

    value = n

    for i in range(n):
        key = get_initial_set(i, n, correct=0)
        functions[2 ** (n - 1)][key] = value
        print('GATE {} NOT {}'.format(value, i))
        value += 1

    for i in range(2 ** (n - 1) - 1, -1, -1):
        left = 2 ** (n - 1)
        right = i + 1
        for key_left, value_left in functions[left].items():
            for key_right, value_right in functions[right].items():
                key = key_left.intersection(key_right)
                if key not in functions[len(key)]:
                    functions[len(key)][key] = value
                    print('GATE {} AND {} {}'.format(
                        value, value_left, value_right
                    ))
                    value += 1

    for i in range(2, 2 ** n + 1):
        left = 1
        right = left + i - 2
        for key_left, value_left in functions[left].items():
            for key_right, value_right in functions[right].items():
                key = key_left.union(key_right)
                if key not in functions[len(key)]:
                    functions[len(key)][key] = value
                    print('GATE {} OR {} {}'.format(
                        value, value_left, value_right
                    ))
                    value += 1

    for i in range(2 ** 2 ** n):
        print('OUTPUT {} {}'.format(i, i))
