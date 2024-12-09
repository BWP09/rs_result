import typing

T = typing.TypeVar("T", covariant = True)
E = typing.TypeVar("E", covariant = True)

class Ok[T1, E1]:
    def __init__(self, value: T1) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({repr(self._value)})"
    
    def is_ok(self) -> bool:
        return True
    
    def is_err(self) -> bool:
        return False
    
    def ok(self) -> T1:
        return self._value
    
    def err(self) -> None:
        return None
    
    def expect_ok(self, message: str) -> T1:
        return self._value
    
    def expect_err(self, message: str) -> typing.NoReturn:
        raise UnwrapError(self, message)
    
    def expect_ok_or[U](self, default: U) -> T1:
        return self._value
    
    def expect_err_or[U](self, default: U) -> U:
        return default
    
    def match[R](self, func_ok: typing.Callable[[T1], R], func_err: typing.Callable[[E1], R]) -> R:
        return func_ok(self._value)

class Err[E1, T1]:
    def __init__(self, value: E1) -> None:
        self._value = value
    
    def __repr__(self) -> str:
        return f"Err({repr(self._value)})"
    
    def is_ok(self) -> bool:
        return False
    
    def is_err(self) -> bool:
        return True
    
    def ok(self) -> None:
        return None
    
    def err(self) -> E1:
        return self._value
    
    def expect_ok(self, message: str) -> typing.NoReturn:
        raise UnwrapError(self, message)
    
    def expect_err(self, message: str) -> E1:
        return self._value
    
    def expect_ok_or[U](self, default: U) -> U:
        return default
    
    def expect_err_or[U](self, default: U) -> E1:
        return self._value
    
    def match[R](self, func_ok: typing.Callable[[T1], R], func_err: typing.Callable[[E1], R]) -> R:
        return func_err(self._value)
    
    def propagate[T2](self) -> "Err[E1, T2]":
        return Err[E1, T2](self.err())

Result: typing.TypeAlias = typing.Union[Ok[T, E], Err[E, T]]

class UnwrapError[T1, E1](Exception):
    def __init__(self, result: Result[T1, E1], message: str) -> None:
        self._result = result

        super().__init__(message)

    @property
    def result(self) -> Result[T1, E1]:
        return self._result
