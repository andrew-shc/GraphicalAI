""" Playing around with PyTest """


def incr(x):
    return x + 1

def test_answer():
    assert incr(4) == 5
