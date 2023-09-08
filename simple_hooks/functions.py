from typing import Callable
import functools


def enable_hooks(cls_or_fn: type|Callable) -> type|Callable:
    """Adds an event hook system for before and after a function/method
        is called. Can wrap functions and entire classes.
    """
    if type(cls_or_fn) is type:
        return enable_hooks_class(cls_or_fn)
    elif callable(cls_or_fn):
        return enable_hooks_callable(cls_or_fn)


def enable_hooks_callable(fn: Callable) -> Callable:
    """Enables hooks for a function or method."""
    # @functools.wraps(fn)
    def wrapped_fn(*args, **kwargs):
        if hasattr(wrapped_fn, 'before_hooks'):
            for hook in wrapped_fn.before_hooks:
                hook(*args, **kwargs)
        result = fn(*args, **kwargs)
        if hasattr(wrapped_fn, 'after_hooks'):
            for hook in wrapped_fn.after_hooks:
                hook(*args, **kwargs)
        return result

    def add_before_hook(hook: Callable) -> None:
        if not hasattr(wrapped_fn, 'before_hooks'):
            setattr(wrapped_fn, 'before_hooks', [])
        wrapped_fn.before_hooks.append(hook)

    def remove_before_hook(hook: Callable) -> None:
        if hasattr(wrapped_fn, 'before_hooks'):
            if hook in wrapped_fn.before_hooks:
                wrapped_fn.before_hooks.remove(hook)

    def add_after_hook(hook: Callable) -> None:
        if not hasattr(wrapped_fn, 'after_hooks'):
            setattr(wrapped_fn, 'after_hooks', [])
        wrapped_fn.after_hooks.append(hook)

    def remove_after_hook(hook: Callable) -> None:
        if hasattr(wrapped_fn, 'after_hooks'):
            if hook in wrapped_fn.after_hooks:
                wrapped_fn.after_hooks.remove(hook)

    wrapped_fn.add_before_hook = add_before_hook
    wrapped_fn.remove_before_hook = remove_before_hook
    wrapped_fn.add_after_hook = add_after_hook
    wrapped_fn.remove_after_hook = remove_after_hook

    wrapped_fn.__name__ = fn.__name__
    wrapped_fn.__annotations__ = fn.__annotations__
    wrapped_fn.__defaults__ = fn.__defaults__
    wrapped_fn.__kwdefaults__ = fn.__kwdefaults__

    return wrapped_fn


def enable_hooks_class(cls: type) -> type:
    """Enables hooks for all methods of the given class. Hooks can be
        added or removed from both the class itself and individual
        instances.
    """
    class WrappedCls(cls):
        def __init__(self, *args, **kwargs) -> None:
            for name in dir(self):
                if name[:2] == '__':
                    continue
                if type(getattr(self, name)) is type:
                    continue
                if callable(getattr(self, name)):
                    setattr(self, name, enable_hooks_callable(getattr(self, name)))
            super().__init__(*args, **kwargs)

    for name in dir(cls):
        if name[:2] == '__':
            continue
        if type(getattr(cls, name)) is type:
            continue
        if callable(getattr(cls, name)):
            setattr(WrappedCls, name, enable_hooks_callable(getattr(cls, name)))

    WrappedCls.__name__ = cls.__name__
    WrappedCls.__annotations__ = cls.__annotations__
    WrappedCls.__doc__ = cls.__doc__
    WrappedCls.__module__ = cls.__module__

    return WrappedCls
