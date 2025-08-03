from dataclasses import dataclass


@dataclass
class DailyQuants:
    """日次株価四本値

    Args:
        date (str): 日付
        code (str): 銘柄コード
        open (float): 始値
        high (float): 高値
        low (float): 安値
        close (float): 終値
        volume (float): 売買値
    """
    date: str
    code: str
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __init__(self, date: str, code: str, open: float, high: float, low: float, close: float, volume: float):
        self.date = date
        self.code = code
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
