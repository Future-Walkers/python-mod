from typing import Iterable


def diff(iterable1: Iterable, iterable2: Iterable) -> list:
    """
    get iterable2's elements which is not in iterable1,elements of
    iterable1 and iterable2 must be hashable.So user defined class
    must supply override __hash__ and __eq__ function,or
    the class instance will use id() as its hash value.
    For example:
    iterable1=[1,2,3,4]
    iterable2=[2,3,5,7,9]
    call of diff(iterable1,iterable2) returns [5,7,9],
    call of diff(iterable2,iterable1) returns [1,4]
    :return: list of diff
    """
    res = list()
    if type(iterable1) != set:
        iterable1 = set(iterable1)
    for e in iterable2:
        if e not in iterable1:
            res.append(e)
    return res
