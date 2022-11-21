#!/usr/bin/env python

# TODO: Add --no-lucky-guess -n option

import argparse
import random
import sys


def main():
    args = parse_command_line_arguments()
    divisor_finder = DivisorFinder(args.number)
    divisor = divisor_finder.find_divisor()
    print(f'Divisor is {divisor}')


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Find a non-trivial divisor')
    parser.add_argument(
        'number',
        help='The number for which to find a divisor')
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

    def __init__(self, number):
        self.number = number

    def find_divisor(self):
        divisor = None
        while divisor is None:
            a = random.randint(2, self.number - 1)
            divisor = self.try_find_divisor_for_a(a)
        return divisor

    def try_find_divisor_for_a(self, a):
        print(f'try_find_divisor_for_a {a=}')
        k = self.greatest_common_divisor(a, self.number)
        print(f'{k=}')
        if k != 1:
            return k
        return None

    @staticmethod
    def greatest_common_divisor(a, b):
        while b != 0:
            a, b = b, a % b
        return a


if __name__ == '__main__':
    main()
