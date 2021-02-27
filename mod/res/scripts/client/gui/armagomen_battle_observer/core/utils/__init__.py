from .keys_parser import HotKeysParser
from .loader import Loader


def overrideMethod(wg_class, method_name="__init__"):
    """
    :type wg_class: class object
    :type method_name: unicode default __init__
    """
    class_name = wg_class.__name__
    if not hasattr(wg_class, method_name):
        if method_name.startswith("__"):
            full_name = "_{0}{1}".format(class_name, method_name)
            if hasattr(wg_class, full_name):
                method_name = full_name
            elif hasattr(wg_class, method_name[1:]):
                method_name = method_name[1:]

    def outer(new_method):
        old_method = getattr(wg_class, method_name, None)
        if old_method is not None and callable(old_method):
            def override(*args, **kwargs):
                return new_method(old_method, *args, **kwargs)

            setattr(wg_class, method_name, override)
        else:
            from .bw_utils import logError
            logError("{0} in {1} is not callable or undefined".format(method_name, class_name))
        return new_method

    return outer
