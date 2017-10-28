# Prompts the user for an integer N at least equal to 5,
# computes the largest number l >= 1 such that l consecutive prime numbers
# add up to a prime number at most equal to N,
# and outputs l and the larger such prime number.
#
# Written by Binaca and Eric Martin for COMP9021 quiz2


from math import sqrt
import sys


def solution(N):
    # Insert your code here
    return None, None
  
try:
    N = int(input('Enter an integer at least equal to 5: '))
    if N < 5:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

max_length, candidate = solution(N)
if max_length:
    print('The largest sequence of consecutive primes that add up\n  '
          'to a prime P equal to {} at most has a length of {}.\n'
          'The largest such P is {}.'.format(N, max_length, candidate))
            
