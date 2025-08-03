from abc import ABC, abstractmethod
from ....domain.model.daily_quants import DailyQuants
from typing import List
from datetime import datetime


class DailyQuantsRepository(ABC):
    @abstractmethod
    def create_table_if_not_exists(self) -> None:
        pass

    @abstractmethod
    def insert_daily_quants(self, daily_quants: List[DailyQuants], target_date: datetime) -> None:
        pass
