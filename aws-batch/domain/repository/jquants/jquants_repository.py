from abc import ABC, abstractmethod
from ....domain.model.stock import Stock
from typing import List

class JquantsRepository(ABC):
    @abstractmethod
    def get_refresh_token(self, email: str, password: str) -> str:
        pass

    @abstractmethod
    def get_id_token(self, refreshToken: str) -> str:
        pass

    @abstractmethod
    def get_stock_list(self, idToken: str) -> List[Stock]:
        pass
