#!/usr/bin/env python

import argparse
import random
import sys


def main():
    args = parse_command_line_arguments()
    try:
        divisor = find_divisor(args)
    except Exception as exception:
        print(exception, file=sys.stderr)
        sys.exit(1)
    print(f'The divisor is {divisor}')


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Find a non-trivial divisor')
    parser.add_argument(
        'number',
        help='The number for which to find a divisor')
    args = parser.parse_args()
    return args


def find_divisor(args):
    number = get_number(args)
    divisor = None
    while divisor is None:
        a = random.randint(2, number-1)
        divisor = try_find_divisor_for_a(number, a)
    return number


def get_number(args):
    number_str = args.number
    try:
        number = int(number_str)
    except ValueError:
        invalid_number_argument(number_str, 'Must be an integer')
    if number < 3:
        invalid_number_argument(number_str, 'Must be 3 or greater')
    return number


def invalid_number_argument(number_str, reason):
    raise AttributeError(f'Invalid number argument {number_str}: {reason}')


def try_find_divisor_for_a(number, a):
    print(f'try_find_divisor_for_a {number=} {a=}')
    k = greatest_common_divisor(a, number)
    print(f'{k=}')
    return None


def greatest_common_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a


if __name__ == '__main__':
    main()
