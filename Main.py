# -*- coding: utf-8 -*-

def int_to_list(number: int) -> list:
    print("Inputted as an 'int'")
    array = []
    n_skip = 0  # don't read the first element if negative
    if number < 0:
        array.append("-")
        n_skip = 1
    for c in str(number)[n_skip:]:
        array.append(int(c))

    return array


def float_to_list(number: float) -> list:
    print("Inputted as a 'float'")
    array = []
    n_skip = 0  # don't read the first element if negative
    if number < 0:
        array.append("-")
        n_skip = 1

    dot = str(number).index(".")
    for c in str(number)[n_skip:dot]:
        array.append(int(c))
    array.append(".")
    for c in str(number)[dot+1:]:
        array.append(int(c))
    return array


def str_to_list(number: str) -> list:
    print("Inputted as a 'str'")
    return


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

    def __init__(self, number):

        if type(number) == int:
            self._array = int_to_list(number)

        elif type(number) == float:
            self._array = float_to_list(number)

        elif type(number) == str:
            self._array = str_to_list(number)

        else:
            raise TypeError("Can't make sense of the input")
        # elif 
        #     for c in str(number):
        #         if c == "-":
        #             self._array.append(c)
        #         else:
        #             self._array.append(int(c))

        # good_chars = [str(c) for c in range(0, 10)] + ["-", ".", "/"]
        # elif type(number) == float:
        #     for c in str(number):
        #         if c == "." or "-":
        #             self._array.append(c)
        #         else:
        #             self._array.append(int(c))

        # elif type(number) == str:

        #     for c in number:
        #         if c not in good_chars:
        #             i = number.index(c)
        #             err = f"Bad character in number: '{c}' at pos: {i},"  
        #             err += " can't convert to glide."
        #             raise bad_input(err)

        #     if "/" in number:
        #         self._array = "Fraction type, still in progress..."

        #     else:
        #         for c in str(number):
        #             self._array.append(int(c))

        # elif isinstance(number, list):
        #     for c in number:
        #         if c not in good_chars:
        #             print(good_chars)
        #             i = good_chars.index(str(c))
        #             err = f"Bad character in number ({c} at pos {i}), \
        #             can't convert to glide."
        #             raise err
        #     self._array = number

        # else:
        #     raise "Input must be a valid number or glide-friendly array"

    def __repr__(self):
        return f"glide({self})"

    def __str__(self):
        s = ""
        for c in self._array:
            s += str(c)
        return s

# def gadd(a: glide, b: glide) -> glide:
#     carry = 0
#     c = []
#     for ai, bi in zip(reversed(a), reversed(b)):
