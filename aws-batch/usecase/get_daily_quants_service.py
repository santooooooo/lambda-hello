from sqlite3 import Date
from ..domain.repository.jquants.jquants_repository import JquantsRepository
from ..infra.jquants.jquants_repository_impl import JquantsRepositoryImpl
from ..domain.model.daily_quants import DailyQuants
from datetime import datetime, timedelta
from typing import List


class GetDailyQuantsService:
    jquantsRepository: JquantsRepository

    def __init__(self):
        self.jquantsRepository = JquantsRepositoryImpl()

    def get(self, idToken: str) -> List[DailyQuants] | None:
        targetDate = self.get_target_date()
        if targetDate == None:
            return None

        print(targetDate)
        return self.jquantsRepository.get_daily_quants(idToken, targetDate)

    def get_target_date(self) -> datetime | None:
        """
        対象日付を取得する

        対象日時は以下を満たす必要がある
        - 月曜日から金曜日の日にち
        - 現在から12週間前の日にち

        Args:
            targetDate (str): 対象日付

        Returns:
            Date: 対象日付
            None: 対象日付が見つからない場合
        """
        today = datetime.now()
        targetDate = today - timedelta(weeks=12)
        if targetDate.weekday() <= 4:
            return targetDate
        else:
            return None
