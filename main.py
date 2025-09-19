"""
CMPS 6610  Problem Set 2
See problemset-02.pdf for details.
"""
import time
import tabulate

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))
    

## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.

# some useful utility functions to manipulate bit vectors
def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y
    
def quadratic_multiply(x, y):
    """
    Multiply two binary numbers x and y using the grade-school recursive algorithm.
    """
    # base cases
    if x.decimal_val == 0 or y.decimal_val == 0:
        return BinaryNumber(0)
    if len(x.binary_vec) == 1 and len(y.binary_vec) == 1:
        return BinaryNumber(x.decimal_val * y.decimal_val)

    # padding vectors to equal length
    x_vec, y_vec = pad(x.binary_vec, y.binary_vec)
    x0, x1 = split_number(x_vec)
    y0, y1 = split_number(y_vec)

    # recursive products
    z0 = quadratic_multiply(x0, y0)   # high * high
    z2 = quadratic_multiply(x1, y1)   # low * low
    z3 = quadratic_multiply(x0, y1)   # high * low
    z4 = quadratic_multiply(x1, y0)   # low * high

    n = len(x_vec)
    result_val = (bit_shift(z0, n).decimal_val +
                  bit_shift(z3, n//2).decimal_val +
                  bit_shift(z4, n//2).decimal_val +
                  z2.decimal_val)

    return BinaryNumber(result_val)


def subquadratic_multiply(x, y):
    """
    Multiply two binary numbers x and y using Karatsuba-Ofman algorithm.
    """

    # base cases
    if x.decimal_val == 0 or y.decimal_val == 0:
        return BinaryNumber(0)
    if len(x.binary_vec) == 1 and len(y.binary_vec) == 1:
        return BinaryNumber(x.decimal_val * y.decimal_val)

    # padding vectors to equal length
    x_vec, y_vec = pad(x.binary_vec, y.binary_vec)
    x0, x1 = split_number(x_vec)
    y0, y1 = split_number(y_vec)

    z0 = subquadratic_multiply(x0, y0)   # high * high
    z1 = subquadratic_multiply(x1, y1)   # low * low
    
    x0_x1_sum = BinaryNumber(x0.decimal_val + x1.decimal_val)
    y0_y1_sum = BinaryNumber(y0.decimal_val + y1.decimal_val)
    z2 = subquadratic_multiply(x0_x1_sum, y0_y1_sum)

    n = len(x_vec)
    result_val = (bit_shift(z0, n).decimal_val +
                    bit_shift(BinaryNumber(z2.decimal_val - z0.decimal_val - z1.decimal_val), n//2).decimal_val +
                    z1.decimal_val)

    return BinaryNumber(result_val)

print('testing multiplication')


print(quadratic_multiply(BinaryNumber(11), BinaryNumber(11)))
print(subquadratic_multiply(BinaryNumber(11), BinaryNumber(11)))

def test_multiply():
    assert quadratic_multiply(BinaryNumber(2), BinaryNumber(2)).decimal_val == 2*2
    assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(2)).decimal_val == 2*2
    assert quadratic_multiply(BinaryNumber(10), BinaryNumber(10)).decimal_val == 10*10
    assert subquadratic_multiply(BinaryNumber(10), BinaryNumber(10)).decimal_val == 10*10
    assert quadratic_multiply(BinaryNumber(5), BinaryNumber(4)).decimal_val == 5*4
    assert subquadratic_multiply(BinaryNumber(5), BinaryNumber(4)).decimal_val == 5*4

# some timing functions here that will make comparisons easy    
def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    f(x,y)
    return (time.time() - start)*1000
    
def compare_multiply():
    res = []
    for n in [10,100,1000,10000,100000,1000000,10000000,100000000,1000000000]:
        qtime = time_multiply(BinaryNumber(n), BinaryNumber(n), quadratic_multiply)
        subqtime = time_multiply(BinaryNumber(n), BinaryNumber(n), subquadratic_multiply)        
        res.append((n, qtime, subqtime))
    print_results(res)


def print_results(results):
    print("\n")
    print(
        tabulate.tabulate(
            results,
            headers=['n', 'quadratic', 'subquadratic'],
            floatfmt=".3f",
            tablefmt="github"))
    

if __name__ == "__main__":
    test_multiply()
    compare_multiply()  


