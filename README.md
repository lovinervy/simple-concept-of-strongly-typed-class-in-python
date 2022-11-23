# simple-concept-of-strongly-typed-class-in-python
Простой концепт на строгую типизацию Python в классах

```python
import types
from valid import Validator


class Foo(Validator):
    def __init__(self) -> None:
        super().__init__()
    
    name: str
    id: int = 0
    address: dict[str, str] = {}
    func: types.FunctionType

def examples():
    print('hello')


if __name__ == "__main__":
    f = Foo()
    f.name = "Max"            # print(f.name) -> Max
    f.code = "123"            # -> ValueError: 'id' must be a '<class 'int'>', was <class 'str'>
    f.address['city'] = 123   # print(f.address) -> {'city': 123}   <-- its works because input in "dict" avoiding Validator.__setattr__
    f.func = example          # print(f.func()) -> 'hello'
    
```
