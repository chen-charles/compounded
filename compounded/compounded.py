import inspect
import logging

from .ordering import ordering


logger = logging.getLogger('compounded')
logger.propagate = False
logger.setLevel(logging.DEBUG)


class meta_compounded(type):
    """
    At each layer, we only know the details about one layer above.

    > Shall we support newly binded methods with compounding support?
    < No. It is rather easy to design an intermediate class
        to support dynamically binded methods.

    """
    def __new__(cls, original_name, bases, dct):
        for field in dct:
            if inspect.isfunction(dct[field]):
                if hasattr(dct[field], '_compounded'):
                    if field.startswith('__') and field.endswith('__'):
                        raise AttributeError(
                            "Should not compound internal methods: %s" % field)

                    to_be_compounded = list()
                    parents, call_ordering = dct[field]._compounded
                    if parents is None:
                        parents = bases
                    elif not all(p in bases for p in parents):
                        raise ValueError(
                            "Specified parents must be direct parents "
                            "of the class, "
                            "parents=%s, bases=%s" % (parents, bases))
                    logger.debug('compounding with parents %s' %
                                 parents)

                    for base in parents:
                        logger.debug('base %s has __dict__=%s' %
                                     (base, base.__dict__))
                        if field in base.__dict__ and \
                                inspect.isfunction(base.__dict__[field]):
                            to_be_compounded.append(base.__dict__[field])

                    # apply ordering
                    if call_ordering == ordering.backwards:
                        to_be_compounded.insert(0, dct[field])
                    elif call_ordering == ordering.forwards:
                        to_be_compounded.append(dct[field])
                    else:
                        raise ValueError(
                            "%s is not a valid ordering" % call_ordering)

                    logger.debug('compounding %s' % to_be_compounded)
                    final_args = list()
                    final_varargs = None
                    final_kw_varargs = None
                    final_kwonly = list()
                    final_defaults = dict()
                    final_calls = list()

                    for func in to_be_compounded:
                        sig = inspect.signature(func, follow_wrapped=True)
                        call_param = list()
                        for name in sig.parameters:
                            param = sig.parameters[name]
                            if param.kind == param.POSITIONAL_ONLY:
                                if name not in final_args:
                                    final_args.append(param.name)
                                call_param.append(name)
                            elif param.kind == param.POSITIONAL_OR_KEYWORD:
                                if name not in final_args:
                                    final_args.append(param.name)
                                call_param.append(name)
                            elif param.kind == param.VAR_POSITIONAL:
                                if final_varargs is None:
                                    call_param.append('*' + name)
                                    final_varargs = param.name
                                else:
                                    call_param.append('*' + final_varargs)
                            elif param.kind == param.KEYWORD_ONLY:
                                if name not in final_kwonly:
                                    final_kwonly.append(param.name)
                                call_param.append('%s=%s' % (name, name))
                            elif param.kind == param.VAR_KEYWORD:
                                if final_kw_varargs is None:
                                    final_kw_varargs = param.name
                                    call_param.append('**' + name)
                                else:
                                    call_param.append('**' + final_kw_varargs)
                            else:
                                assert False, \
                                    "param.kind=%s could not be handled" \
                                    % param.kind

                            if param.default != param.empty:
                                # lower layer always overrides defaults
                                final_defaults[param.name] = param.default
                        final_calls.append((func, call_param))

                    # now, construct actual function parameters
                    final_parameters = list()
                    for a in final_args:
                        if a in final_defaults:
                            final_parameters.append(
                                '%s=%s' % (a, final_defaults[a]))
                        else:
                            final_parameters.append(a)
                    if final_varargs is not None:
                        final_parameters.append('*' + final_varargs)
                    for kw_only in final_kwonly:
                        if kw_only in final_defaults:
                            final_parameters.append(
                                '%s=%s' % (kw_only, final_defaults[kw_only]))
                        # kw-only's must have a default value
                    if final_kw_varargs is not None:
                        final_parameters.append('**' + final_kw_varargs)

                    d = dict()
                    f_str = """
def _wrapped(%s):
    %s
    return to_be_compounded[-1](%s)
d[0] = _wrapped
""" % (', '.join(final_parameters),
                        ";".join(['to_be_compounded[%d](%s)' %
                                  (i, ', '.join(final_calls[i][1]))
                                  for i in range(len(to_be_compounded) - 1)]),
                        ', '.join(final_calls[-1][1]))
                    logger.debug('final_args=%s' % final_args)
                    exec(f_str, dict(
                        d=d, f=dct[field], to_be_compounded=to_be_compounded))
                    dct[field] = d[0]

        return super(meta_compounded, cls).__new__(
            cls, original_name, bases, dct)


class BaseCompounded(metaclass=meta_compounded):
    """Base class for enabling compounding
    """
    pass


def compounded(method):
    """Default decorator to enable a decorated method for compounding
    :param method: function
        actual function before becoming a bounded/unbounded method
    :return: function for method bounding, ready to be compounded
    """
    logger.debug('decorator called %s' % method)
    method._compounded = None, ordering.forwards
    return method


def compounded_ex(parents, call_ordering=ordering.forwards):
    """Extended decorator to enable a decorated method for compounding
    :param parents: iterable
        iterable for specifying which (direct) bases to be be compounded
    :param call_ordering: ordering
        the specific order for compounded methods to be called
    :return: function for method bounding, ready to be compounded
    """
    def _compounded(method):
        logger.debug('decorator_ex called %s' % method)
        method._compounded = parents, call_ordering
        return method

    return _compounded
