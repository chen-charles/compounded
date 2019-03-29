import logging

import compounded


logger = logging.getLogger(__name__)


class base_setup(compounded.BaseCompounded):
    @compounded.compounded
    def method(self, a, b, c):
        logger.info(str(locals()))
        self.out['v'] += a + b + c


class not_so_obvious_setup(compounded.BaseCompounded):
    @compounded.compounded
    def method(self, d, e=0, f=0):
        logger.info(str(locals()))
        self.out['v'] -= d + e + f


def test_basic():
    count = dict(v=0)

    class basic(base_setup):
        @compounded.compounded_ex([base_setup], compounded.ordering.backwards)
        def method(self, out):
            self.out = out

    o = basic()
    o.method(count, 1, 2, 3)
    assert count['v'] == 6, "failed"


def test_multi_path_base():
    count = dict(v=0)

    class path_base(base_setup, not_so_obvious_setup):
        @compounded.compounded_ex([base_setup], compounded.ordering.backwards)
        def method(self, out):
            self.out = out

    o = path_base()
    o.method(count, 1, 2, 3)
    assert count['v'] == 6, "failed"


def test_multi_path_not_so_obvious():
    class path_not_so_obvious(base_setup, not_so_obvious_setup):
        @compounded.compounded_ex([not_so_obvious_setup],
                                  compounded.ordering.backwards)
        def method(self, out):
            self.out = out

    count = dict(v=0)
    o = path_not_so_obvious()
    o.method(count, 1, 2, 3)
    assert count['v'] == -6, "failed"


def test_multi_path_both():
    class path_both(base_setup, not_so_obvious_setup):
        @compounded.compounded_ex([base_setup, not_so_obvious_setup],
                                  compounded.ordering.backwards)
        def method(self, out):
            self.out = out

    count = dict(v=0)
    o = path_both()
    o.method(count, 1, 2, 3, 6)
    assert count['v'] == 0, "failed"
    o.method(count, 1, 2, 3, 6, f=5)
    assert count['v'] == -5, "failed"
