from ..domain.repository.jquants.jquants_repository import JquantsRepository
from ..infra.jquants.jquants_repository_impl import JquantsRepositoryImpl
from ..domain.model.daily_quants import DailyQuants
from datetime import datetime, timedelta, timezone
from typing import List, Optional


class GetDailyQuantsService:
    jquantsRepository: JquantsRepository

    def __init__(self):
        self.jquantsRepository = JquantsRepositoryImpl()

    def get(self, idToken: str, executeDateStr: Optional[str] = None) -> List[DailyQuants] | None:
        """
        株式四本値を取得する

        環境変数 EXECUTE_DATE が指定されている場合はその日付（JST）を対象日付とする。
        未指定の場合は既存のルール（現在から12週間前の平日）で対象日付を算出する。
        いずれの方法でも土日を指す場合は処理をスキップする（None を返す）。
        """
        targetDate = self._resolve_target_date(executeDateStr)
        if targetDate == None:
            return None

        print(targetDate)
        return self.jquantsRepository.get_daily_quants(idToken, targetDate)

    def _resolve_target_date(self, executeDateStr: Optional[str]) -> Optional[datetime]:
        """
        対象日付を解決する。優先順位:
        1) executeDateStr（JST, YYYY-MM-DD）
        2) 12週間前の平日（ローカル時刻基準）
        """
        if executeDateStr and executeDateStr.strip():
            parsed = self._parse_execute_date_jst(executeDateStr.strip())
            if parsed is None:
                print("EXECUTE_DATE が土日、または不正な形式のため処理をスキップします")
            return parsed
        return self.get_target_date()

    def _parse_execute_date_jst(self, date_str: str) -> Optional[datetime]:
        """
        EXECUTE_DATE（YYYY-MM-DD, JST）を datetime へ変換する。
        土日の場合は None を返す。
        """
        try:
            dt_naive = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None

        jst = timezone(timedelta(hours=9))
        jst_dt = datetime(dt_naive.year, dt_naive.month,
                          dt_naive.day, 0, 0, 0, tzinfo=jst)
        return self._weekday_or_none(jst_dt)

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
        return self._weekday_or_none(targetDate)

    def _weekday_or_none(self, date: datetime) -> datetime | None:
        """
        日付が平日であればその日付を返し、土日であればNoneを返す
        """
        if date.weekday() >= 5:
            return None
        return date
