import math

def gauss_bell(mu, sigma, min=0, max=1):
    return lambda x: math.exp(-((x - mu) ** 2 / (2 * sigma ** 2))) * (max - min) + min

def plateaued_gauss_bell(min_mu, max_mu, sigma, min=0, max=1):
    left_gauss = gauss_bell(min_mu, sigma, min, max)
    right_gauss = gauss_bell(max_mu, sigma, min, max)

    return lambda x: (
        1 if min_mu <= x <= max_mu
        else left_gauss(x) if x < min_mu
        else right_gauss(x)
    )

def characteristic_function(predicate, off=0, on=1):
    return lambda x: on if predicate(x) else off

def integer_partition(n, weights):
    if len(weights) == 0:
        return []

    s = sum(weights)
    if s == 0:
        return [0 for _ in weights]

    max_index = weights.index(max(weights))
    fraction = weights[max_index] / s
    part = min(max(round(fraction * n), 1), n)
    residue = n - part

    del weights[max_index]
    result = integer_partition(residue, weights)
    result.insert(max_index, part)

    return result
