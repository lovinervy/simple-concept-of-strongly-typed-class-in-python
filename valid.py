import types

class Validator:
    __dict__ = {}
    __hint__ = {}

    def __init__(self) -> None:
        for name, value in self.__annotations__.items():
            try:
                self.__dict__[name] = self.__getattribute__(name)
            except AttributeError:
                self.__dict__[name] = None
            self.__hint__[name] = self.generic_parse_annotations(value)

    def __setattr__(self, __name: str, __value: __builtins__) -> None:
        if __name not in self.__dict__:
            raise AttributeError(f"Attribute {__name} not in class '{type(self).__name__}'")
        if self.is_valid(__name, __value):
            object.__setattr__(self, __name, __value)
            self.__dict__[__name] = __value
        else:
            raise ValueError(f"'{__name}' must be a '{', '.join([str(x) for x in self.__hint__[__name]])}'"\
                f", was {', '.join([str(x) for x in self.generic_parse_value(__value)])}")


    def generic_parse_value(self, __value: __builtins__) -> set[set[types.GenericAlias] | set[__builtins__]]:
        parsed = set()
        if not __value:
            parsed.add(type(__value))
        elif type(__value) in (list, tuple, set):
            for el in __value:
                if type(el) in (list, tuple, dict, set):
                    result = [types.GenericAlias(type(__value), x) for x in self.generic_parse_value(el)]
                    parsed = set.union(parsed, result)
                else:
                    parsed.add(types.GenericAlias(type(__value), type(el)))
        elif type(__value) is dict:
            for k, v in __value.items():
                result = [types.GenericAlias(type(__value), (type(k) ,x)) for x in self.generic_parse_value(v)]
                parsed = set.union(parsed, result)
        else:
            parsed.add(type(__value))
        return parsed

    def generic_parse_annotations(self, __type: types) -> set[set[types.GenericAlias] | set[__builtins__]]:
        parsed = set()
        if __type.__class__.__module__ == "builtins":
            parsed.add(__type)
        elif __type.__class__.__module__ == "types":
            if __type.__class__.__name__ == "GenericAlias":
                if __type.__name__ == "dict":
                    if len(__type.__args__) > 2:
                        raise Exception(f"Hint '{__type}' have much args, expected 2, actual {len(__type.__args__)}")
                    key = self.generic_parse_annotations(__type.__args__[0])
                    value = self.generic_parse_annotations(__type.__args__[1])
                    result = []
                    for k in key:
                        for v in value:
                            result.append(types.GenericAlias(__type.__origin__, (k, v)))
                    parsed = set.union(parsed, result)
                elif __type.__name__ in ("list", "tuple", "set"):
                    if len(__type.__args__) > 1:
                        raise Exception(f"To many args in {__type}, expected 1, gived {len(__type.__args__)}")
                    result = [types.GenericAlias(__type.__origin__, x) for x in self.generic_parse_annotations(__type.__args__[0])]
                    parsed = set.union(parsed, result)

            elif __type.__class__.__name__ == "UnionType":
                for el in __type.__args__:
                    result = self.generic_parse_annotations(el)
                    parsed = set.union(parsed, result)
        else:
            raise TypeError(f'Type "{__type}" is not supported')
        return parsed

    def is_generic(self, __type):
        if __type.__class__.__module__ == "types":
            return True
        return False
    
    def is_valid(self, __name: str, __value: __builtins__) -> bool:
        expected_hints = self.__hint__[__name]
        input_hints = self.generic_parse_value(__value)
        for input_hint in input_hints:
            if input_hint not in expected_hints:
                return False
        return True
