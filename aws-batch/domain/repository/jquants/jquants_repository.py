from abc import ABC, abstractmethod
from ....domain.model.daily_quants import DailyQuants
from ....domain.model.stock import Stock
from typing import List
from datetime import datetime


class JquantsRepository(ABC):
    @abstractmethod
    def get_refresh_token(self, email: str, password: str) -> str:
        """
        リフレッシュトークンを取得する
        """
        pass

    @abstractmethod
    def get_id_token(self, refreshToken: str) -> str:
        """
        認証用IDトークンを取得する
        """
        pass

    @abstractmethod
    def get_stock_list(self, idToken: str) -> List[Stock]:
        """
        銘柄一覧を取得する
        """
        pass

    @abstractmethod
    def get_daily_quants(self, idToken: str, date: datetime) -> List[DailyQuants]:
        """
        日次株価四本値を取得する
        """
        pass
