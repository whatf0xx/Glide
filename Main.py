# -*- coding: utf-8 -*-
import copy
from math import factorial
from sympy import isprime


def remove_leading_zeros(s: list[int]) -> list[int]:
    if not s:
        return s

    if s == [0]:
        return s

    leading_zero = False
    new_s = [a for a in s if (leading_zero or a != 0) and (leading_zero := True)]

    return new_s

def remove_trailing_zeros(s: list[int]) -> list[int]:
    if not s:
        return s

    if s == [0]:
        return s

    decs = copy.copy(s)
    decs.reverse()
    leading_zero = False
    new_decs = [a for a in decs if (leading_zero or a != 0) and (leading_zero := True)]
    new_decs.reverse()
    return new_decs


class Glide:
    """
    Arithmetic on arbitrarily accurate denary floats. These are implemented as 
    lists of ints 0-9, sign stored as a string. Arithmetic is defined as operations over the
    arrays, but the glides are neatly represented as number strings.
    
    ...

    Attributes
    ----------
    number: float. The number to be converted into a Glide.

    Methods
    -------
    __repr__():
        Gets the representation of the Glide.
    """

    def __init__(self, number: float):

        """
        Decimal representation attributes
        """
        self._units = []
        self._decs = []

        """
        Scientific represenation attributes
        """
        self._mantissa = []
        self._pow = 0

        """
        Attributes for properties of the Glide
        """
        self._precision = None
        self._sign = "+ve"

        self.from_float(number)

    def __repr__(self):
        return f"Glide({self})"

    def __str__(self):
        s = ""

        if self._sign == "-ve":
            s += "-"

        for c in self._units:
            s += str(c)

        s += "."

        for d in self._decs:
            s += str(d)

        return s

    def get_units(self):
        return self._units

    def set_units(self, new_units):
        self._units = new_units

        return self

    def get_decs(self):
        return self._decs

    def set_decs(self, new_decs):
        self._decs = new_decs

        return self

    def get_pow(self):
        return self._pow

    def set_pow(self, new_pow: int):
        self._pow = new_pow
        return self

    def get_mantissa(self):
        return self._mantissa

    def set_mantissa(self, mant: list[int]):
        self._mantissa = mant

        return self

    def update_scientific(self):
        """
        Based on the currently stored decimal represenation, update the scientific representation.
        """
        self.trim()

        if self == Glide(0):
            self.set_pow(0)
            self.set_mantissa(0)
            return self

        if self.get_decs() == [0]:  # case that the number is an integer
            self.set_pow(len(self.get_units()) - 1)

            self.set_mantissa(remove_trailing_zeros(self.get_units()))

        if self.get_units() == [0]: #  case that the number is between 0 and 1
            trimmed_mant = remove_leading_zeros(self.get_decs())
            leading_zeros = len(self.get_decs()) - len(trimmed_mant)
            self.set_pow(- leading_zeros - 1)
            self.set_mantissa(trimmed_mant)

        else:
            self.set_pow(len(self.get_units()) - 1)
            self.set_mantissa(self.get_units() + self.get_decs())

        return self

    def update_decimal(self):
        """
        Update the decimal representation of the Glide based on the currently stored
        scientific representation.
        """
        if self.get_pow() == 0:
            self.set_units([self.get_mantissa()[0]])
            self.set_decs(self.get_mantissa()[1:])
        elif self.get_pow() > 0:
            self.set_units(self.get_mantissa()[:self.get_pow()+1])
            self.set_decs(self.get_mantissa()[self.get_pow()+1:])
        else:
            self.set_units([0])
            self.set_decs([0] * (abs(self.get_pow()) - 1) + self.get_mantissa())

        return self.trim()

    def get_sign(self):
        return self._sign

    def set_sign(self, new_sign):
        allowed_signs = ["+ve", "-ve"]
        if new_sign not in allowed_signs:
            raise ValueError("That's not an allowed sign! Use '+ve' or '-ve'")
        else:
            self._sign = new_sign

        return self

    def get_precision(self):
        return self._precision

    def set_precision(self, precision: int):
        self._precision = precision
        return self

    def to_float(self):
        f = 0
        for e, i in enumerate(self.get_decs()):
            f += 0.1 ** (e + 1) * i

        for u, j in enumerate(reversed(self.get_units())):
            f += 10 ** u * j

        s = {"+ve": 1, "-ve": -1}
        f *= s[self.get_sign()]

        return f

    def from_float(self, number: float):
        try:
            if number < 0:
                self.set_sign("-ve")

            skip_on_negative = {"+ve": 0, "-ve": 1}

            num_str = str(float(number))
            dot = num_str.index(".")

            units = []
            decs = []

            for c in num_str[skip_on_negative[self._sign]:dot]:
                units.append(int(c))

            for d in num_str[dot + 1:]:
                decs.append(int(d))

            self.set_units(units)
            self.set_decs(decs)

        except TypeError:
            print("Can't make sense of the input")
            raise

    def trim(self):
        """
        Get rid of leading/trailing zeros on the decimal represenation of the Glide.

        Returns
        -------
        self: the updated Glide.
        """
        if not self.get_units():
            self.set_units([0])
        else:
            self.set_units(remove_leading_zeros(self.get_units()))

        if not self.get_decs():
            self.set_decs([0])
        else:
            self.set_decs(remove_trailing_zeros(self.get_decs()))

        return self

    def __abs__(self):
        a = copy.copy(self)
        return a.set_sign("+ve")

    def __neg__(self):
        if self.get_sign() == "+ve":
            return self.set_sign("-ve")
        elif self.get_sign() == "-ve":
            return self.set_sign("+ve")
        else:
            raise AttributeError(f"Glide didn't have a valid sign. ({self.get_sign})")

    def __eq__(self, other):
        if self.get_decs() == other.get_decs() and \
                self.get_units() == other.get_units() and \
                self.get_sign() == other.get_sign():
            return True
        else:
            return False

    def __gt__(self, other):
        if self.get_sign() == "+ve" and other.get_sign() == "-ve":
            # print("Easy sign comparison (case 1)")
            return True
        elif self.get_sign() == "-ve" and other.get_sign() == "+ve":
            # print("Easy sign comparison (case 2)")
            return False

        # Then the signs must be the same, and we will always arrive here...
        fancy_truth = {"+ve": True, "-ve": False}

        a = copy.copy(self).trim()
        b = copy.copy(other).trim()
        #
        # if len(a.get_units()) > len(b.get_units()):
        #     return fancy_truth[self.get_sign()]  # returns True if +ve and False if -ve
        # elif len(a.get_units()) < len(b.get_units()):
        #     return not fancy_truth[self.get_sign()]

        len_diff = len(a.get_units()) - len(b.get_units())
        zeros = [0] * abs(len_diff)

        if len_diff > 0:
            b.set_units(zeros + b.get_units())
        elif len_diff < 0:
            a.set_units(zeros + a.get_units())

        # print(f"List 1: {a.get_units()}")
        # print(f"List 2: {b.get_units()}")

        # Compare digit by digit:
        for i, j in zip(a.get_units(), b.get_units()):
            if i > j:
                # print(f"{i} > {j} !")
                return fancy_truth[self.get_sign()]
            elif j > i:
                # print(f"{i} actually < {j} !")
                return not fancy_truth[self.get_sign()]
            # print(f"{i} not > {j}")

        # equal units! Try the decimals...

        len_diff = len(a.get_decs()) - len(b.get_decs())
        zeros = [0] * abs(len_diff)

        if len_diff > 0:
            b.set_decs(b.get_decs() + zeros)
        elif len_diff < 0:
            a.set_decs(a.get_decs() + zeros)

        # print(f"List 1: {a.get_decs()}")
        # print(f"List 2: {b.get_decs()}")

        for k, l in zip(a.get_decs(), b.get_decs()):
            if k > l:
                # print(f"{k} > {l} !")
                return fancy_truth[self.get_sign()]
            elif l > k:
                # print(f"{k} actually < {l} !")
                return not fancy_truth[self.get_sign()]
            # print(f"{k} not > {l}")

        # if we got here they must be equal.
        # print("Got to the end so returning False")
        return False

    def __lt__(self, other):
        if self.get_sign() == "+ve" and other.get_sign() == "-ve":
            # print("Easy sign comparison (case 1)")
            return False
        elif self.get_sign() == "-ve" and other.get_sign() == "+ve":
            # print("Easy sign comparison (case 2)")
            return True

        # Then the signs must be the same, and we will always arrive here...
        fancy_truth = {"+ve": False, "-ve": True}

        a = copy.copy(self).trim()
        b = copy.copy(other).trim()
        #
        # if len(a.get_units()) > len(b.get_units()):
        #     return fancy_truth[self.get_sign()]  # returns True if +ve and False if -ve
        # elif len(a.get_units()) < len(b.get_units()):
        #     return not fancy_truth[self.get_sign()]

        len_diff = len(a.get_units()) - len(b.get_units())
        zeros = [0] * abs(len_diff)

        if len_diff > 0:
            b.set_units(zeros + b.get_units())
        elif len_diff < 0:
            a.set_units(zeros + a.get_units())

        # print(f"List 1: {a.get_units()}")
        # print(f"List 2: {b.get_units()}")

        # Compare digit by digit:
        for i, j in zip(a.get_units(), b.get_units()):
            if i > j:
                # print(f"{i} > {j} !")
                return fancy_truth[self.get_sign()]
            elif j > i:
                # print(f"{i} actually < {j} !")
                return not fancy_truth[self.get_sign()]
            # print(f"{i} not > {j}")

        # equal units! Try the decimals...

        len_diff = len(a.get_decs()) - len(b.get_decs())
        zeros = [0] * abs(len_diff)

        if len_diff > 0:
            b.set_decs(b.get_decs() + zeros)
        elif len_diff < 0:
            a.set_decs(a.get_decs() + zeros)

        # print(f"List 1: {a.get_decs()}")
        # print(f"List 2: {b.get_decs()}")

        for k, l in zip(a.get_decs(), b.get_decs()):
            if k > l:
                # print(f"{k} > {l} !")
                return fancy_truth[self.get_sign()]
            elif l > k:
                # print(f"{k} actually < {l} !")
                return not fancy_truth[self.get_sign()]
            # print(f"{k} not > {l}")

        # if we got here they must be equal.
        # print("Got to the end so returning False")
        return False

    def __ge__(self, other):
        if self > other or self == other:
            return True
        else:
            return False

    def __le__(self, other):
        if self < other or self == other:
            return True
        else:
            return False

    def __add__(self, other):
        a = copy.copy(self)
        b = copy.copy(other)

        if a.get_sign() == "-ve" and b.get_sign() == "-ve":
            c = abs(a) + abs(b)
            return -c

        elif a.get_sign() == "-ve" and b.get_sign() == "+ve":
            return abs(b) - abs(a)

        elif a.get_sign() == "+ve" and b.get_sign() == "-ve":
            return abs(a) - abs(b)

        len_diff = len(a.get_decs()) - len(b.get_decs())
        zeros = [0] * abs(len_diff)

        if len_diff > 0:
            b.set_decs(b.get_decs() + zeros)
        elif len_diff < 0:
            a.set_decs(a.get_decs() + zeros)

        carry = 0
        output_decs = []

        for ai, bi in zip(reversed(a.get_decs()), reversed(b.get_decs())):
            s = ai + bi + carry
            output_decs.append(s % 10)
            if s > 9:
                carry = 1
            else:
                carry = 0

        output_decs.reverse()

        len_diff = len(a.get_units()) - len(b.get_units())
        zeros = [0] * abs(len_diff)

        if len_diff > 0:
            b.set_units(zeros + b.get_units())
        elif len_diff < 0:
            a.set_units(zeros + a.get_units())

        output_units = []

        for ci, di in zip(reversed(a.get_units()), reversed(b.get_units())):
            s = ci + di + carry
            output_units.append(s % 10)
            if s > 9:
                carry = 1
            else:
                carry = 0

        if carry == 1:
            output_units.append(1)

        output_units.reverse()

        x = Glide(1)
        x.set_decs(output_decs)
        x.set_units(output_units)

        return x

    def __sub__(self, other):
        a = copy.copy(self)
        b = copy.copy(other)

        if a == b:
            return Glide(0)

        if a.get_sign() == "-ve" and b.get_sign() == "-ve":
            return abs(b) - abs(a)

        elif a.get_sign() == "+ve" and b.get_sign() == "-ve":
            return abs(a) + abs(b)

        elif a.get_sign() == "-ve" and b.get_sign() == "+ve":
            c = abs(a) + abs(b)
            return -c

        if a < b:
            c = b - a
            return -c

        # actually do the subtraction. First need to do the subtraction over the decs...

        len_diff = len(a.get_decs()) - len(b.get_decs())
        zeros = [0] * abs(len_diff)

        if len_diff > 0:
            b.set_decs(b.get_decs() + zeros)
        elif len_diff < 0:
            a.set_decs(a.get_decs() + zeros)

        carry = 0
        output_decs = []

        for ai, bi in zip(reversed(a.get_decs()), reversed(b.get_decs())):
            s = ai - bi - carry
            output_decs.append(s % 10)
            if s < 0:
                carry = 1
            else:
                carry = 0

        output_decs.reverse()

        len_diff = len(a.get_units()) - len(b.get_units())
        zeros = [0] * abs(len_diff)

        if len_diff > 0:
            b.set_units(zeros + b.get_units())
        elif len_diff < 0:
            a.set_units(zeros + a.get_units())

        output_units = []

        for ci, di in zip(reversed(a.get_units()), reversed(b.get_units())):
            s = ci - di - carry
            output_units.append(s % 10)
            if s < 0:
                carry = 1
            else:
                carry = 0

        output_units.reverse()

        x = Glide(1)
        x.set_decs(output_decs)
        x.set_units(output_units)
        if carry == 1:
            x.set_sign("-ve")

        return x

    def __mul__(self, other):
        a = copy.copy(self).trim().update_scientific()
        b = copy.copy(other).trim().update_scientific()

        if len(a.get_mantissa()) < len(b.get_mantissa()):
            return b * a

        # print(f"{a_list} \t with shift {a_shift}")
        # print(f"{b_list} \t with shift {b_shift}")
        # print("--------------")

        table = []

        for e, bi in enumerate(reversed(b.get_mantissa())):
            carry = 0
            table.append([])

            if e != 0:
                table[e] += ([0] * e)

            for ai in reversed(a.get_mantissa()):
                p = (ai * bi + carry)
                table[e].append(p % 10)

                if p > 9:
                    # print(f"Calculating carry... (p = {p})")
                    carry = p // 10
                else:
                    carry = 0

            shift = a.get_pow() + b.get_pow()  # work out the power of the result

            if carry != 0:
                table[e].append(carry)
                shift += 1

            table[e].reverse()
            # print(table[e])

        # print("--------------")

        # Now add the rows as Glides!
        s = Glide(0)

        for i in table:
            q = Glide(1)
            q.set_units(i)
            s += q

        s.set_mantissa(s.get_units())
        s.set_pow(shift)

        if a.get_sign() == b.get_sign():
            return s.update_decimal()
        else:
            return -s.update_decimal()

    def __divmod__(self, other):
        a = copy.copy(self)
        b = copy.copy(other)

        if b == Glide(0):
            raise ZeroDivisionError("can't divide by Glide(0.0).")

        if a == b:
            return Glide(1), Glide(0)

        quot = Glide(0)
        cum = Glide(0)

        if a.get_sign() == b.get_sign():

            while abs(cum) <= abs(a):
                    quot += Glide(1)
                    cum += b

            return (quot-Glide(1)).trim(), (a+b-cum).trim()

        while abs(cum) < abs(a):
            quot -= Glide(1)
            cum -= b

        return quot.trim(), (a-cum).trim()

    def __floordiv__(self, other):
        return divmod(self, other)[0]

    def __mod__(self, other):
        return divmod(self, other)[1]

    def __truediv__(self, other):
        if self == other:
            return Glide(1)

        a = copy.copy(self)
        b = copy.copy(other)

        quot, rem = divmod(a, b)
        if rem == Glide(0):
            return quot  # if we're lucky we're done here!

        """
        Otherwise we have to divide the remainder, until the precision limit is reached or the 
        division terminates.
        """

        if self.get_precision() is None:
            a_len = len(a.get_units()) + len(a.get_decs())
            b_len = len(b.get_units()) + len(b.get_decs())
            precision_limit = max([a_len, b_len]) + 1
        else:
            precision_limit = self.get_precision()

        while len(quot.get_units()) + len(quot.get_decs()) < precision_limit and remainder != Glide(0):

            zeros = 0
            while remainder < b:
                remainder *= Glide(10)
                zeros += 1




            if remainder % divisor == 0:
                remainder = 0
            else:
                remainder = 10 * (remainder % divisor)

        if shift == 0:
            return Glide(1).set_units(quotient_list).trim()

        t = Glide(1)
        t.set_units(quotient_list[:-shift])
        t.set_decs(quotient_list[-shift:])

        return t.trim()


def glide_from_int(num: int) -> Glide:
    num_list = [int(a) for a in str(num)]

    output = Glide(1)
    output.set_units(num_list)

    return output


def glide_to_string(g: Glide, raw: bool = True) -> str:
    """
    Take a Glide input and return a string representation.
    Parameters
    ----------
    g : The input Glide
    raw : bool, whether we want the glide as a proper string, or just the numbers associated. So if True only
          the associated numbers of the glide, not -ve sign, decimal point etc.

    Returns the string of numbers and symbols associated with the Glide's value.
    -------

    """
    if raw:
        return "".join([str(a) for a in g.get_units() + g.get_decs()])
    else:
        if g.get_sign() == "-ve":
            return "-".join([str(a) for a in g.get_units()]) + ".".join([str(a) for a in g.get_decs()])


def main() -> None:
    precision = 10000
    e = Glide(0)

    for i in range(500):
        f = glide_from_int(factorial(i))
        f.set_precision(precision)
        e += Glide(1).set_precision(precision) / f

    accurate_e = glide_to_string(e)

    for i in range(precision-9):
        n_to_check = accurate_e[i:i+10]
        if isprime(n_to_check):
            print(f"{n_to_check} is the first prime we're interested in!")
            break


if __name__ == "__main__":
    pass
    #  main()
