def convert_scalar_to_list(scalar):



    # Scalar
    if type(scalar) != list:
        return [scalar]

    # Already list
    else:
        return scalar

def convert_to_tuple(a):
    # List
    if type(a) == list:
        return tuple(a)

    # Scalar
    elif type(a) != tuple:
        return (a, )

    # Already tuple
    else:
        return a
