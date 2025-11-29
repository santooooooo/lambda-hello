from ..domain.repository.dynamo_db.daliy_quants_repository import DailyQuantsRepository
from ..infra.dynamo_db.daily_quants_repository_impl import DailyQuantsRepositoryImpl
from ..domain.model.daily_quants import DailyQuants
from typing import List
from datetime import datetime, timedelta, timezone


class InsertDailyQuantsListService:
    dailyQuantsRepository: DailyQuantsRepository

    def __init__(self, isTest: str) -> None:
        self.dailyQuantsRepository = DailyQuantsRepositoryImpl(isTest=isTest)

    def insert(self, daily_quants: List[DailyQuants] | None) -> None:

        if daily_quants is None or len(daily_quants) == 0:
            print("株式四本値が存在しません")
            return

        # 株式四本値の日付を取得
        jst = timezone(timedelta(hours=9))
        target_date = datetime.fromtimestamp(daily_quants[0].date, tz=jst)
        self.dailyQuantsRepository.create_table_if_not_exists()
        self.dailyQuantsRepository.insert_daily_quants(
            daily_quants, target_date)
