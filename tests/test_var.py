import logging

import compounded


logger = logging.getLogger(__name__)


class base_setup(compounded.BaseCompounded):
    @compounded.compounded
    def method(self, out):
        self.out = out


class basic(base_setup):
    @compounded.compounded
    def method(self, a, b, c, *args, d=0, e=1, **kwargs):
        logger.info(str(locals()))
        self.out['v'] += a + b + c + sum(args) + d + e + sum(kwargs.values())


def test_basic():
    count = dict(v=0)
    o = basic()

    o.method(count, 1, 2, 3, 4, 5, 6, 7, 8, 9, d=10, e=11, f=12, g=13, h=14)
    assert count['v'] == sum(list(range(15))), "failed"


def test_different_varargs_name():
    count = dict(v=0)

    class basic2(basic):
        @compounded.compounded
        # a, b, c, *argv, d=0, e=1, **kwargs
        def method(self, *argv, **kwargv):
            logger.info(str(locals()))
            self.out['v'] += sum(argv) + sum(kwargv.values())

    o = basic2()
    o.method(count, 1, 2, 3, 4, 5, 6, 7, 8, 9, d=10, e=11, f=12, g=13, h=14)
    assert count['v'] == sum(
        list(range(15)) + list(range(4, 10)) + list(range(12, 15))), "failed"


def test_var_partial():
    count = dict(v=0)

    class basic3(basic):
        @compounded.compounded
        # a, b, c, *(xx, *rest_of_argv), d=0, e=1, **kwargs
        # 1, 2, 3, *(4, 5, 6, 7, 8, 9), d=10, e=11, **(f=12, g=13, h=14)
        # thus, at this stage, 4+5+6+7+8+9+12+13+14
        def method(self, xx, *argv, j=-1000, **kwargv):
            logger.info(str(locals()))
            self.out['v'] += xx + sum(argv) + sum(kwargv.values()) + j

    o = basic3()
    o.method(count, 1, 2, 3, 4, 5, 6, 7, 8, 9,
             d=10, e=11, f=12, g=13, h=14, j=0)
    assert count['v'] == sum(
        list(range(15)) + list(range(4, 10)) + list(range(12, 15))) - 4, \
        "failed"
