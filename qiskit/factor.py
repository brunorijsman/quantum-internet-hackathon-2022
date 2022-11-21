#!/usr/bin/env python

import argparse
import random
import sys


def main():
    args = parse_command_line_arguments()
    divisor_finder = DivisorFinder(args.number, args.allow_lucky_guess)
    divisor = divisor_finder.find_divisor()
    print(f'Divisor is {divisor}')


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Find a non-trivial divisor')
    parser.add_argument(
        'number',
        help='The number for which to find a divisor')
    parser.add_argument(
        '-l',
        '--allow-lucky-guess',
        action="store_true",
        help='Allow lucky guess of divisor')
    args = parser.parse_args()
    try:
        args.number = int(args.number)
    except ValueError:
        invalid_number_argument(args.number, 'Must be an integer')
    if args.number < 3:
        invalid_number_argument(args.number, 'Must be 3 or greater')
    return args


def invalid_number_argument(number_str, reason):
    print(f'Invalid number argument {number_str}: {reason}', file=sys.stderr)
    sys.exit(1)


class DivisorFinder:

    def __init__(self, number, allow_lucky_guess):
        self.number = number
        self.allow_lucky_guess = allow_lucky_guess

    def find_divisor(self):
        divisor = None
        while divisor is None:
            a = random.randint(2, self.number - 1)
            divisor = self.try_find_divisor_for_a(a)
        return divisor

    def try_find_divisor_for_a(self, a):
        k = self.greatest_common_divisor(a, self.number)
        if k != 1:
            if self.allow_lucky_guess:
                return k
            else:
                return None
        period = self.find_period(a)
        if period % 2 == 1:
            return None
        power = a ** (period // 2)
        if power % self.number == self.number - 1:
            return None
        return self.greatest_common_divisor(power + 1, self.number)

    def find_period(self, a):
        # Brute-force non-quantum algorithm for finding the period of: try every value r in
        # 1 < r < N until we find the first r such that a ** r == 1 (mod N)
        for r in range(1, self.number):
            if a ** r % self.number == 1:
                return r
        assert False

    @staticmethod
    def greatest_common_divisor(a, b):
        while b != 0:
            a, b = b, a % b
        return a


if __name__ == '__main__':
    main()
