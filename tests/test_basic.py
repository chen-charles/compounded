import logging

import compounded


logger = logging.getLogger(__name__)


def test_basic():
    count = dict(v=0)

    class derived(compounded.BaseCompounded):
        @compounded.compounded
        def method(self):
            count['v'] += 1

        def method_not_compounded(self):
            assert False, "should not be called"

    class derived_derived(derived):
        @compounded.compounded_ex([derived])
        def method(self):
            count['v'] += 1

        def method_not_compounded(self):
            pass

    o = derived_derived()

    logger.info('ready to call .method')
    o.method()
    assert count['v'] == 2, "method not compounded"
    o.method_not_compounded()
