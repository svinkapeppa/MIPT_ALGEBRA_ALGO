from cmath import exp
from math import pi


def ifft(x):
    if len(x) == 1:
        return x

    even = ifft(x[0::2])
    odd = ifft(x[1::2])

    factor = [exp(2j * pi * k / len(x)) * odd[k] for k in range(len(x) // 2)]

    lhs = [even[k] + factor[k] for k in range(len(x) // 2)]
    rhs = [even[k] - factor[k] for k in range(len(x) // 2)]

    return lhs + rhs


if __name__ == '__main__':
    coefficients = list(map(float, input().split()))

    print(' '.join(f'{x.real},{x.imag}' for x in ifft(coefficients)))
