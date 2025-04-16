
import code
from dataclasses import dataclass


@dataclass
class Stock:
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
