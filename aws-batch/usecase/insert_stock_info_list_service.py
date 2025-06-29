from xmlrpc.client import Boolean
from ..domain.repository.dynamo_db.stock_info_repository import StockInfoRepository
from ..infra.dynamo_db.stock_info_repository_impl import StockInfoRepositoryImpl
from typing import List
from ..domain.model.stock import Stock


class InsertStockInfoListService:
    """上場銘柄一覧をDynamoDBに保存するサービス"""
    stockInfoRepository: StockInfoRepository
    isTest: str

    def __init__(self, isTest: str) -> None:
        self.stockInfoRepository = StockInfoRepositoryImpl(isTest=isTest)
        self.isTest = isTest

    def insert(self, stock_list: List[Stock]) -> None:
        """上場銘柄一覧をDynamoDBに保存する
        Args:
            stock_list (List[Stock]): 保存する上場銘柄一覧
        """
        # テーブルが存在しない場合は作成する
        self.stockInfoRepository.create_table_if_not_exists()

        # 既に保存されている銘柄コードの取得
        try:
            exists_stock_list = self.stockInfoRepository.get_stock_info_list()
            exists_stock_list_code = [
                stock.code for stock in exists_stock_list]
            print("現在保存されている銘柄コード件数: ", len(exists_stock_list_code))
        except Exception as e:
            print("現在保存されている銘柄コードの取得に失敗しました: ", e)
            return

        # まだ保存されていないstock_listのみ保存する
        try:
            new_stock_list = [
                stock for stock in stock_list if stock.code not in exists_stock_list_code]
            self.stockInfoRepository.insert_stock_info(new_stock_list)
        except Exception as e:
            print("新しい銘柄の保存に失敗しました: ", e)
            return
