# Simple Hooks

The purpose of this package is to provide a simple way to add hooks to functions
and methods that trigger before or after the function/method call.

Only downside is that it breaks original type analysis and related tools.

## Installation

```
pip install simple-hooks
```

## Usage

There are several ways to use this library. There are four functions available:
- `enable_hooks`
- `enable_hooks_on_callable`
- `enable_hooks_on_method`
- `enable_hooks_on_class`

The simplest way to use this is to use `enable_hooks` as a decorator as it will
automatically call either `enable_hooks_on_class` or `enable_hooks_on_callable`;
`enable_hooks_on_class` will call `enable_hooks_on_method` instead of
`enable_hooks_on_callable` for class methods.

```python
from simple_hooks import enable_hooks
make_log = lambda label: lambda *args, **kwargs: print(f"{label}: {args=} {kwargs=}")


@enable_hooks
def does_something(arg: str):
    print(arg)

does_something.add_before_hook(make_log('before'))
does_something.add_after_hook(make_log('after'))

does_something('hello')
# before: args=('hello',) kwargs={}
# hello
# after: args=('hello',) kwargs={}
```

The `enable_hooks` decorator can also be used with class methods:

```python
from simple_hooks import enable_hooks
make_log = lambda label: lambda *args, **kwargs: print(f"{label}: {args=} {kwargs=}")

class Thing:
    @enable_hooks
    def do_something(self, arg: str):
        print(arg)
    def __repr__(self) -> str:
        return "Thing instance"

Thing.do_something.add_before_hook(make_log('before original'))
Thing.do_something.add_after_hook(make_log('after original'))
t = Thing()

t.do_something('test')
# before original: args=(Thing instance, 'test') kwargs={}
# test
# after original: args=(Thing instance, 'test') kwargs={}

t.do_something.add_before_hook(make_log('before instance'))
t.do_something.add_after_hook(make_log('after instance'))

t.do_something('test')
# prints the following:
# before original: args=(Thing instance, 'test') kwargs={}
# before instance: args=(Thing instance, 'test') kwargs={}
# test
# after original: args=(Thing instance, 'test') kwargs={}
# after instance: args=(Thing instance, 'test') kwargs={}
```

The `enable_hooks` decorator can also be used with a class itself.

```python
from simple_hooks import enable_hooks
make_log = lambda label: lambda *args, **kwargs: print(f"{label}: {args=} {kwargs=}")


@enable_hooks
class Thing:
    def do_something(self, arg: str):
        print(arg)
    def __repr__(self) -> str:
        return "Thing instance"

Thing.do_something.add_before_hook(make_log('before original'))
Thing.do_something.add_after_hook(make_log('after original'))
t = Thing()

t.do_something('test')
# before original: args=(Thing instance, 'test') kwargs={}
# test
# after original: args=(Thing instance, 'test') kwargs={}

t.do_something.add_before_hook(make_log('before instance'))
t.do_something.add_after_hook(make_log('after instance'))

t.do_something('test')
# prints the following:
# before instance: args=(Thing instance, 'test') kwargs={}
# before original: args=(Thing instance, 'test') kwargs={}
# test
# after original: args=(Thing instance, 'test') kwargs={}
# after instance: args=(Thing instance, 'test') kwargs={}
```


## Testing

To test, clone the repo and run the following:

```
python tests/test_functions.py
```

There are currently only 5 tests as this is a simple library.

# License

ISC License

Copyleft (c) 2023 k98kurz

Permission to use, copy, modify, and/or distribute this software
for any purpose with or without fee is hereby granted, provided
that the above copyleft notice and this permission notice appear in
all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
