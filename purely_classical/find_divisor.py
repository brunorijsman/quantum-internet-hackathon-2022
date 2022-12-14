#!/usr/bin/env python
"""
A purely classical algorithm to find a factor of a number. It is exactly the same as Shor's
algorithm, except that it uses a brute-force classical search to find the period of a number a.
"""

import argparse
import random
import sys


def main():
    """
    Main entry point.
    """
    args = parse_command_line_arguments()
    divisor_finder = DivisorFinder(args.number, args.allow_lucky_guess)
    divisor = divisor_finder.find_divisor()
    print(f"Divisor is {divisor}")


def parse_command_line_arguments():
    """
    Parse the command line arguments.
    """
    parser = argparse.ArgumentParser(description="Find a non-trivial divisor")
    parser.add_argument("number", help="The number for which to find a divisor")
    parser.add_argument(
        "-l", "--allow-lucky-guess", action="store_true", help="Allow lucky guess of divisor"
    )
    args = parser.parse_args()
    try:
        args.number = int(args.number)
    except ValueError:
        invalid_number_argument(args.number, "Must be an integer")
    if args.number < 3:
        invalid_number_argument(args.number, "Must be 3 or greater")
    return args


def invalid_number_argument(number_str, reason):
    """
    Report an invalid number argument (fatal error).

    Parameters
    ----------
    number_str: The string that contains an invalid number.
    reason: The reason the string is not a valid number.
    """
    print(f"Invalid number argument {number_str}: {reason}", file=sys.stderr)
    sys.exit(1)


class DivisorFinder:
    """
    Class to find the divisor for a number.
    """

    def __init__(self, number, allow_lucky_guess):
        """
        Constructor.

        Parameters
        ----------
        number: The number for which we are looking for a factor.
        allow_lucky_guess: Allow the factor to be found using a lucky guess.
        """
        self.number = number
        self.allow_lucky_guess = allow_lucky_guess

    def find_divisor(self):
        """
        Find the divisor of the number passed to the constructor.

        Note: there is no primality test; this function will not return if number is a prime.
        """
        divisor = None
        while divisor is None:
            a_value = random.randint(2, self.number - 1)
            divisor = self.try_find_divisor_for_a(a_value)
        return divisor

    def try_find_divisor_for_a(self, a_value):
        """
        Try to find a divisor, using a randomly chosen value for a.

        Parameters
        ---------
        a_value: A randomly chosen value for a.

        Returns
        -------
        A factor of the number that was given to the constructor, or None if no factor could be
        found given the randomly chosen a_value.
        """
        common_divisor = self.greatest_common_divisor(a_value, self.number)
        if common_divisor != 1:
            if self.allow_lucky_guess:
                return common_divisor
            return None
        period = self.find_period(a_value)
        if period % 2 == 1:
            return None
        power = a_value ** (period // 2)
        if power % self.number == self.number - 1:
            return None
        return self.greatest_common_divisor(power + 1, self.number)

    def find_period(self, a_value):
        """
        Brute-force non-quantum algorithm for finding the period of a: try every value r in
        1 < r < N until we find the first r such that a ** r == 1 (mod N)
        """
        for r_value in range(1, self.number):
            if a_value**r_value % self.number == 1:
                return r_value
        assert False

    @staticmethod
    def greatest_common_divisor(number_a, number_b):
        """
        Find the greatest common divisor between two numbers.

        Parameters
        ----------
        number_a: The first number.
        number_b: The second number.

        Returns
        -------
        The greatest common divisor between the two numbers.
        """
        while number_b != 0:
            number_a, number_b = number_b, number_a % number_b
        return number_a


def find_divisor(number):
    """
    Find a divisor for a given number.

    Parameters
    ----------
    number: The number for which to find a factor. The number must not be a prime (the function
        will not return if number is a prime).

    Returns
    -------
    A factor of number.
    """
    divisor_finder = DivisorFinder(number, allow_lucky_guess=False)
    return divisor_finder.find_divisor()


if __name__ == "__main__":
    main()
