#!/usr/bin/env python3
# Tests (TD 1)
# Isabel Hojman & Hermes Martinez


def optimise_univariate(step_size=0.4, max_epochs=30):
    """
    Optimizes f(x) = (x-3)^2 (strictly convex)
    """
    x = 0
    for e in range(max_epochs):
        x -= step_size * 2 * (x - 3)  # f’(x) = 2(x-3)
        obj = (x - 3)**2
        print(x, obj)
    return x


def optimise_bivariate(step_size=0.4, max_epochs=30):
    """
    Optimizes f(x1,x2) = x1^2+x2^2+2x1+8x2 (strictly convex)
    """
    (x1, x2) = (0, 0)
    for e in range(max_epochs):
        obj = x1**2 + x2**2 + 2 * x1 + 8 * x2
        print((x1, x2), obj)
        x1, x2 = (x1 - step_size * (2 * x1 + 2), x2 - step_size * (2 * x2 + 8))
    obj = x1**2 + x2**2 + 2 * x1 + 8 * x2
    print((x1, x2), obj)
    return (x1, x2)
