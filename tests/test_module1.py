"""
Test for pymodule
"""

import pymodule as p1
import pytest


# Input data for test funcs
addData = [
    (2, 1, 3),
    (0, 1, 1),
    (0, 0, 0), ]


@pytest.mark.parametrize("a,b,ans", addData)
def test_add(a, b, ans):
    assert(p1.module1.aladd(a, b) == ans)
    assert(p1.module1.aladd(b, a) == ans)


# Input data for test funcs
mulData = [
    (2, 1, 2),
    (0, 1, 0),
    (0, 0, 0), ]


@pytest.mark.parametrize("a,b,ans", mulData)
def test_mul(a, b, ans):
    assert(p1.module1.almul(a, b) == ans)
    assert(p1.module1.almul(b, a) == ans)


def test_p2():
    p1.module2.alf2(1)
