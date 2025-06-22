from abc import ABC, abstractmethod
from typing import List
from xmlrpc.client import Boolean
from ....domain.model.stock import Stock


class StockInfoRepository(ABC):
    @abstractmethod
    def create_table_if_not_exists(self) -> None:
        pass

    @abstractmethod
    def get_stock_info_list(self) -> List[Stock]:
        pass

    @abstractmethod
    def insert_stock_info(self, stock_list: List[Stock]) -> float:
        pass
