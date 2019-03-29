import logging

import compounded


logger = logging.getLogger(__name__)


class base_setup(compounded.BaseCompounded):
    @compounded.compounded
    def method(self, a, b, c):
        self.out['v'] += a + b + c


def test_basic():
    count = dict(v=0)

    class basic(base_setup):
        @compounded.compounded_ex([base_setup], compounded.ordering.backwards)
        def method(self, out):
            self.out = out

    o = basic()
    o.method(count, 1, 2, 3)
    assert count['v'] == 6, "failed"
