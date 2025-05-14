from xmlrpc.client import Boolean
from ..domain.repository.dynamo_db.stock_info_repository import StockInfoRepository
from ..infra.dynamo_db.stock_info_repository_impl import StockInfoRepositoryImpl
from typing import List
from ..domain.model.stock import Stock

class InsertStockInfoListService:
    stockInfoRepository: StockInfoRepository  = None

    def __init__(self, isTest: str) -> None:
        self.stockInfoRepository = StockInfoRepositoryImpl(isTest=isTest)

    def insert(self, stock_list: List[Stock]) -> None:
        self.stockInfoRepository.create_table_if_not_exists()
        # self.stockInfoRepository.insert_stock_info(stock_list)
