import inspect


def foo(a: int, b) -> None:
    pass


for i in inspect.signature(foo).parameters.values():
    print(i.annotation)

print(inspect._empty)
