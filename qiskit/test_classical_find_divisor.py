from classical_find_divisor import find_divisor


def test_two_divisors():
    assert find_divisor(47 * 59) in [47, 59]
    assert find_divisor(31 * 97) in [31, 97]


def test_multiple_divisors():
    number = 5 * 13 * 19 * 59
    divisor = find_divisor(number)
    assert number % divisor == 0


def test_repeated_divisors():
    number = 13 * 13 * 19
    divisor = find_divisor(number)
    assert number % divisor == 0
