# list functions


def intersection(ls1, ls2):
    """
    This function returns the intersection of two lists without
    repetition. This function uses built in Python function set()
    to get rid of repeated values so inputs must be cast to list
    first.

    Parameters:
    -----------
    ls1 : Python list
            The first list. Cannot be array.
    ls2 : Python list
            The second list. Cannot be array.

    Returns:
    ls3 : Python list
            The list of overlapping values between ls1 and ls2
    """

    temp = set(ls1)
    ls3 = [value for value in ls2 if value in temp]

    return ls3
