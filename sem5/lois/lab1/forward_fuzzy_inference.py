from sympy import symbols, exp, log, limit, oo


def t_norm(x, y) -> float:
    if min(x, y) == 0:
        return 0
    
    z = symbols('z')
    f = x * exp(z * log(y)) + y * exp(z * log(x))
    value = limit(f, z, oo)
    return float(min(1.0, value.evalf()))


def weber_impl(x: float, y: float) -> float:
    if x < 0:
        return 1.0
    else:
        return y
    
    