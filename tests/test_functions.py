from context import functions
import unittest


class TestFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.log_entries = []
        return super().setUp()

    def log(self, *args, **kwargs):
        self.log_entries.append(f'Log: {args=} {kwargs=}')

    def make_log(self, anything):
        def log(*args, **kwargs):
            self.log(anything, *args, **kwargs)
        return log

    def test_enable_hooks_on_function(self):
        @functions.enable_hooks
        def thing(name: str):
            self.log_entries.append(name)

        thing.add_before_hook(self.make_log('before'))
        thing.add_after_hook(self.make_log('after'))

        thing('test')

        assert len(self.log_entries) == 3
        assert 'before' in self.log_entries[0]
        assert 'test' in self.log_entries[1]
        assert 'after' in self.log_entries[2]

    def test_hooks_on_class_instance(self):
        this = self
        @functions.enable_hooks
        class Thing:
            def __init__(self, name: str = 'Bob') -> None:
                self.name = name
            def say_hello(self, name: str = 'Alice'):
                this.log_entries.append(f"{self.name} says hello to {name}")

        t = Thing()
        t.say_hello.add_before_hook(self.make_log('before instance'))
        t.say_hello.add_after_hook(self.make_log('after instance'))

        assert len(self.log_entries) == 0
        t.say_hello('Alice')
        assert len(self.log_entries) == 3
        assert 'before' in self.log_entries[0]
        assert 'Alice' in self.log_entries[0]
        assert 'Bob' in self.log_entries[1]
        assert 'Alice' in self.log_entries[1]
        assert 'after' in self.log_entries[2]
        assert 'Alice' in self.log_entries[2]

    def test_hooks_on_class_itself(self):
        this = self
        @functions.enable_hooks
        class Thing:
            def __init__(self, name: str = 'Bob') -> None:
                self.name = name
            def say_hello(self, name: str = 'Alice'):
                this.log_entries.append(f"{self.name} says hello to {name}")

        Thing.say_hello.add_before_hook(self.make_log('before static'))
        Thing.say_hello.add_after_hook(self.make_log('after static'))

        t = Thing()
        assert len(self.log_entries) == 0
        t.say_hello('Alice')
        assert len(self.log_entries) == 3, f"expected 3, encountered {len(self.log_entries)}"
        assert 'before static' in self.log_entries[0]
        assert 'Alice' in self.log_entries[0]
        assert 'Bob' in self.log_entries[1]
        assert 'Alice' in self.log_entries[1]
        assert 'after static' in self.log_entries[2]
        assert 'Alice' in self.log_entries[2]

    def test_hooks_on_class_itself_and_on_instance_simultaneously(self):
        this = self
        @functions.enable_hooks
        class Thing:
            def __init__(self, name: str = 'Bob') -> None:
                self.name = name
            def say_hello(self, name: str = 'Alice'):
                this.log_entries.append(f"{self.name} says hello to {name}")

        Thing.say_hello.add_before_hook(self.make_log('before static'))
        Thing.say_hello.add_after_hook(self.make_log('after static'))

        t = Thing()
        t.say_hello.add_before_hook(self.make_log('before instance'))
        t.say_hello.add_after_hook(self.make_log('after instance'))
        assert len(self.log_entries) == 0
        t.say_hello('Alice')
        assert len(self.log_entries) == 5, f"expected 5, encountered {len(self.log_entries)}"
        assert 'before instance' in self.log_entries[0]
        assert 'Alice' in self.log_entries[0]
        assert 'before static' in self.log_entries[1]
        assert 'Alice' in self.log_entries[1]
        assert 'Bob' in self.log_entries[2]
        assert 'Alice' in self.log_entries[2]
        assert 'after static' in self.log_entries[3]
        assert 'Alice' in self.log_entries[3]
        assert 'after instance' in self.log_entries[4]
        assert 'Alice' in self.log_entries[4]

    def test_hooks_on_class_method_definitions(self):
        this = self
        class Thing:
            def __init__(self, name: str = 'Bob') -> None:
                self.name = name
            @functions.enable_hooks_on_method
            def say_hello(self, name: str = 'Alice'):
                this.log_entries.append(f"{self.name} says hello to {name}")

        Thing.say_hello.add_before_hook(self.make_log('before static'))
        Thing.say_hello.add_after_hook(self.make_log('after static'))

        t = Thing()
        t.say_hello.add_before_hook(self.make_log('before instance'))
        t.say_hello.add_after_hook(self.make_log('after instance'))
        assert len(self.log_entries) == 0
        t.say_hello('Alice')
        assert len(self.log_entries) == 5, f"expected 5, encountered {len(self.log_entries)}"
        assert 'before static' in self.log_entries[0], self.log_entries[0]
        assert 'Alice' in self.log_entries[0]
        assert 'before instance' in self.log_entries[1]
        assert 'Alice' in self.log_entries[1]
        assert 'Bob' in self.log_entries[2]
        assert 'Alice' in self.log_entries[2]
        assert 'after static' in self.log_entries[3]
        assert 'Alice' in self.log_entries[3]
        assert 'after instance' in self.log_entries[4]
        assert 'Alice' in self.log_entries[4]


if __name__ == '__main__':
    unittest.main()
