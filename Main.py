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

    def absolute(self):
        a = copy.copy(self)
        return a.set_sign("+ve")

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
        self.set_units([a for a in self.get_units() if (leading_zero or a != 0) and (leading_zero := True)])

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

        output_units.reverse()

        x = Glide(1)
        x.set_decs(output_decs)
        x.set_units(output_units)

        return x

    def __sub__(self, other):
        a = copy.copy(self)
        b = copy.copy(other)



        return a, b
