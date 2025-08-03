
import code
from dataclasses import dataclass


@dataclass
class Stock:
    """銘柄情報"""
    """
    Args:
        date (str): 日付
        code (str): 銘柄コード
        companyName (str): 会社名
        companyNameEnglish (str): 英語会社名
        sector17Code (str): 17業種コード
        sector33Code (str): 33業種コード
        scaleCategory (str): 規模コード
        marketCode (str): 市場コード
    """
    date: str
    code: str
    companyName: str
    companyNameEnglish: str
    sector17Code: str
    sector33Code: str
    scaleCategory: str
    marketCode: str

    def __init__(self, date: str, code: str, companyName: str, companyNameEnglish: str, sector17Code: str, sector33Code: str, scaleCategory: str, marketCode: str):
        self.date = date
        self.code = code
        self.companyName = companyName
        self.companyNameEnglish = companyNameEnglish
        self.sector17Code = sector17Code
        self.sector33Code = sector33Code
        self.scaleCategory = scaleCategory
        self.marketCode = marketCode
