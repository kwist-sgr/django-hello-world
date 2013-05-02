from types import FunctionType, MethodType


def error_trapping(result=None, on_exception=None):
    def inner(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception, e:
                try:
                    if callable(on_exception):
                        on_exception(e)
                except:
                    pass
                return result
        return wrapper
    # Allow decorator without arguments to be called without brackets
    if type(result) in [FunctionType, MethodType]:
        return inner(result)
    return inner
