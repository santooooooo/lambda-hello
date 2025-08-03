from ..domain.repository.dynamo_db.daliy_quants_repository import DailyQuantsRepository
from ..infra.dynamo_db.daily_quants_repository_impl import DailyQuantsRepositoryImpl
from ..domain.model.daily_quants import DailyQuants
from typing import List
from datetime import datetime, timedelta


class InsertDailyQuantsListService:
    dailyQuantsRepository: DailyQuantsRepository

    def __init__(self, isTest: str) -> None:
        self.dailyQuantsRepository = DailyQuantsRepositoryImpl(isTest=isTest)

    def insert(self, daily_quants: List[DailyQuants]) -> None:
        target_date = datetime.now() - timedelta(weeks=12)
        self.dailyQuantsRepository.create_table_if_not_exists()
        self.dailyQuantsRepository.insert_daily_quants(
            daily_quants, target_date)
