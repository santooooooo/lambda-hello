from dataclasses import dataclass
from datetime import datetime, timezone, timedelta


@dataclass
class DailyQuants:
    """日次株価四本値

    Args:
        date (int): 日付（JSTの当日00:00を基準としたUnixエポック秒）
        code (str): 銘柄コード
        open (float): 始値
        high (float): 高値
        low (float): 安値
        close (float): 終値
        volume (float): 売買値
    """
    date: int
    code: str
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __init__(self, date: int, code: str, open: float, high: float, low: float, close: float, volume: float):
        self.date = date
        self.code = code
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    @staticmethod
    def to_jst_midnight_epoch_seconds(date_str: str) -> int:
        """YYYY-MM-DD を JST(UTC+9) 当日00:00のエポック秒に変換する"""
        d = datetime.strptime(date_str, "%Y-%m-%d")
        jst = timezone(timedelta(hours=9))
        jst_dt = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=jst)
        return int(jst_dt.timestamp())

    @classmethod
    def from_api(cls, date_str: str, code: str, open: float, high: float, low: float, close: float, volume: float) -> "DailyQuants":
        """APIのDate(YYYY-MM-DD)をJST 00:00のUnix秒に変換して生成する"""
        epoch_seconds = cls.to_jst_midnight_epoch_seconds(date_str)
        return cls(
            date=epoch_seconds,
            code=code,
            open=open,
            high=high,
            low=low,
            close=close,
            volume=volume
        )
