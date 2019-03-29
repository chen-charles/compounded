import logging

import compounded


logger = logging.getLogger(__name__)


class base_setup(compounded.BaseCompounded):
    @compounded.compounded
    def method(self, out):
        self.out = out


class base(base_setup):
    @compounded.compounded
    def method(self, a, b, c):
        self.out['v'] += a + b + c


class basic(base):
    @compounded.compounded_ex([base])
    def method(self, d, e, f):
        self.out['v'] += d + e + f


def test_basic():
    count = dict(v=0)
    o = basic()

    vals_list = dict(a=1, b=2, c=3, d=4, e=5, f=6)
    o.method(count, *vals_list.values())
    assert count['v'] == sum(vals_list.values()), "failed"


def test_use_keywords():
    count = dict(v=0)
    o = basic()

    vals_list = dict(a=1, b=2, c=3, d=4, e=5, f=6)
    o.method(count, *vals_list.values())
    assert count['v'] == sum(vals_list.values()), "failed"


def test_with_default_values():
    count = dict(v=0)

    class with_default_values(base):
        @compounded.compounded_ex([base])
        def method(self, d, e, f=10):
            self.out['v'] += d + e + f

    o = with_default_values()

    vals_list = dict(a=1, b=2, c=3, d=4, e=5)
    o.method(count, *vals_list.values())
    assert count['v'] == sum(list(vals_list.values()) + [10]), "failed"


def test_with_default_values_overriding():
    count = dict(v=0)

    class override0(base_setup):
        @compounded.compounded
        def method(self, a=1, b=2, c=3):
            self.out['v'] += a + b + c

    class override1(override0):
        @compounded.compounded
        def method(self, a=4, c=6, d=10):
            self.out['v'] += a + c + d

    o = override1()
    o.method(count)
    assert count['v'] == 32, "failed"
