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

            for d in num_str[dot+1:]:
                self._decs.append(int(d))

        except TypeError:
            print("Can't make sense of the input")
            raise

    def __repr__(self):
        return f"glide({self})"

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
        self._units = []
        for c in str(new_units):
            self._units.append(c)

        return self

    def get_decs(self):
        return self._decs

    def set_decs(self, new_decs):
        self._decs = []
        for c in str(new_decs):
            self._decs.append(c)

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
        other = copy.copy(self)
        return other.set_sign("+ve")
