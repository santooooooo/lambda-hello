from typing import Callable, TypeVar, Generic

L = TypeVar("L")
R = TypeVar("R")
U = TypeVar("U")

class Either(Generic[L, R]):
    def is_left(self) -> bool:
        raise NotImplementedError("is_left method not implemented")

    def is_right(self) -> bool:
        raise NotImplementedError("is_right method not implemented")

    @property
    def get_left_value(self):
        if self.is_left():
            return self.value
        raise ValueError("Value is not a Left")

    @property
    def get_right_value(self):
        if self.is_right():
            return self.value
        raise ValueError("Value is not a Right")

    def fold(self, left_func: Callable[[L], U], right_func: Callable[[R], U]) -> U:
        raise NotImplementedError("fold method not implemented")

class Left(Either[L, R]):
    def __init__(self, value: L):
        self.value = value

    def is_left(self) -> bool:
        return True

    def is_right(self) -> bool:
        return False

    def fold(self, left_func: Callable[[L], U], right_func: Callable[[R], U]) -> U:
        return left_func(self.value)

class Right(Either[L, R]):
    def __init__(self, value: R):
        self.value = value

    def is_left(self) -> bool:
        return False

    def is_right(self) -> bool:
        return True

    def fold(self, left_func: Callable[[L], U], right_func: Callable[[R], U]) -> U:
        return right_func(self.value)
