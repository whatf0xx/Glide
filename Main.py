# -*- coding: utf-8 -*-

class Glide:
    """
    Arithmetic on arbitrarily accurate denary floats. These are implemented as 
    lists of ints 0-9. Arithmetic is defined as operations over the arrays,
    but the glides should always be neatly represented as number strings.
    
    ...

    Attributes
    ----------
    number : str, int, float or glide-friendly array
        Representation of the number for the glide

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
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

# def gadd(a: glide, b: glide) -> glide:
#     carry = 0
#     c = []
#     for ai, bi in zip(reversed(a), reversed(b)):
