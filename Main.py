# -*- coding: utf-8 -*-
import copy


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
        self._units = []
        self._decs = []
        try:
            if number >= 0:
                self._sign = "+ve"
            else:
                self._sign = "-ve"

            skip_on_negative = {"+ve": 0, "-ve": 1}

            num_str = str(float(number))
            dot = num_str.index(".")

            for c in num_str[skip_on_negative[self._sign]:dot]:
                self._units.append(int(c))

            for d in num_str[dot + 1:]:
                self._decs.append(int(d))

        except TypeError:
            print("Can't make sense of the input")
            raise

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

    def get_sign(self):
        return self._sign

    def set_sign(self, new_sign):
        allowed_signs = ["+ve", "-ve"]
        if new_sign not in allowed_signs:
            raise ValueError("That's not an allowed sign! Use '+ve' or '-ve'")
        else:
            self._sign = new_sign

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

    def trim(self):
        """
        Get rid of leading/trailing zeros.

        Returns
        -------
        self: the updated Glide.
        """
        leading_zero = False
        new_units = [a for a in self.get_units() if (leading_zero or a != 0) and (leading_zero := True)]
        if not new_units:
            self.set_units([0])
        else:
            self.set_units(new_units)

        decs = copy.copy(self.get_decs())
        decs.reverse()
        leading_zero = False
        new_decs = [a for a in decs if (leading_zero or a != 0) and (leading_zero := True)]
        new_decs.reverse()
        if not new_decs:
            self.set_decs([0])
        else:
            self.set_decs(new_decs)
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
        a = copy.copy(self).trim()
        b = copy.copy(other).trim()

        if len(a.get_decs()) + len(a.get_units()) < len(b.get_decs()) + len(b.get_units()):
            return b * a

        if a.get_decs() == [0]:  # no need to shift if we have an integer
            a_list = a.get_units()
            a_shift = 0
        else:
            a_list = a.get_units() + a.get_decs()
            a_shift = len(a.get_decs())

        if b.get_decs() == [0]:  # no need to shift if we have an integer
            b_list = b.get_units()
            b_shift = 0
        else:
            b_list = b.get_units() + b.get_decs()
            b_shift = len(b.get_decs())

        # print(f"{a_list} \t with shift {a_shift}")
        # print(f"{b_list} \t with shift {b_shift}")
        # print("--------------")

        table = []

        for e, bi in enumerate(reversed(b_list)):
            carry = 0
            table.append([])

            if e != 0:
                table[e] += ([0] * e)

            for ai in reversed(a_list):
                p = (ai * bi + carry)
                table[e].append(p % 10)

                if p > 9:
                    # print(f"Calculating carry... (p = {p})")
                    carry = p // 10
                else:
                    carry = 0

            if carry != 0:
                table[e].append(carry)

            table[e].reverse()
            # print(table[e])

        # print("--------------")

        # Now add the rows as Glides!
        s = Glide(0)

        for i in table:
            q = Glide(1)
            q.set_units(i)
            s += q

        shift = a_shift + b_shift

        if shift == 0:
            if a.get_sign() == b.get_sign():
                return s
            else:
                return -s

        t = Glide(1)
        t.set_units(s.get_units()[:-shift])
        t.set_decs(s.get_units()[-shift:])

        if a.get_sign() == b.get_sign():
            return t
        else:
            return -t

    def __floordiv__(self, other):
        a = copy.copy(self)
        b = copy.copy(other)

        if a == b:
            return Glide(1)

        if a.get_sign() == "-ve" and b.get_sign() == "-ve":
            return -a // -b
        elif a.get_sign() == "-ve" and b.get_sign() == "+ve":
            return - (-a // b)
        elif a.get_sign() == "+ve" and b.get_sign() == "-ve":
            return - (a // -b)

        if b > a:
            return Glide(0)

        else:
            i = 0
            ans = Glide(0)
            while ans <= a:
                i += 1
                ans += b

            return i-1

    def __truediv__(self, other):
        if self == other:
            return Glide(1)

        a = copy.copy(self)
        b = copy.copy(other)

        if a.get_decs() == [0]:  # no need to shift if we have an integer
            a_list = a.get_units()
            a_shift = 0
        else:
            a_list = a.get_units() + a.get_decs()
            a_shift = len(a.get_decs())

        if b.get_decs() == [0]:  # no need to shift if we have an integer
            b_list = b.get_units()
            b_shift = 0
        else:
            b_list = b.get_units() + b.get_decs()
            b_shift = len(b.get_decs())

        divisor = Glide(1).set_units(b_list).to_float() * 10**b_shift

        shift = a_shift - b_shift

        quotient_list = []
        remainder = 0

        for i in a_list:

            dividend = remainder + i
            quotient_list.append(int(dividend // divisor))

            if dividend % divisor == 0:
                remainder = 0
            else:
                remainder = 10 * (dividend % divisor)

        if remainder == 0:
            if shift == 0:
                return Glide(1).set_units(quotient_list).trim()

            t = Glide(1)
            t.set_units(quotient_list[:-shift])
            t.set_decs(quotient_list[-shift:])

            return t

        precision_limit = 20
        while len(quotient_list) < precision_limit and remainder != 0:
            a_list.append(remainder)
            shift += 1

            quotient_list.append(int(remainder // divisor))

            if remainder % divisor == 0:
                remainder = 0
            else:
                remainder = 10 * (dividend % divisor)

        if shift == 0:
            return Glide(1).set_units(quotient_list).trim()

        t = Glide(1)
        t.set_units(quotient_list[:-shift])
        t.set_decs(quotient_list[-shift:])

        return t.trim()