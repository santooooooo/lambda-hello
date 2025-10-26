from sqlite3 import Date
from typing import List
import requests
import json
from ..http_status_exception.bad_request_exception import BadRequestException
from ...domain.repository.jquants import JquantsRepository
from ..http_status_exception.unauthorized_exception import UnauthorizedException
from ...domain.model.stock import Stock
from ...domain.model.daily_quants import DailyQuants
from datetime import datetime


class JquantsRepositoryImpl(JquantsRepository):
    api: str = ""

    def __init__(self):
        self.api = "https://api.jquants.com/v1/"

    def get_refresh_token(self, email: str, password: str) -> str:
        data = {"mailaddress": email, "password": password}
        response = requests.post(
            self.api+"token/auth_user", data=json.dumps(data))
        if response.status_code == 200:
            return response.json().get("refreshToken")
        else:
            self.error_handler(response)

    def get_id_token(self, refreshToken: str) -> str:
        response = requests.post(
            self.api + f"token/auth_refresh?refreshtoken={refreshToken}")
        if response.status_code == 200:
            return response.json().get("idToken")
        else:
            self.error_handler(response)

    def get_stock_list(self, idToken: str) -> List[Stock]:
        headers = {'Authorization': 'Bearer {}'.format(idToken)}
        response = requests.get(self.api+"listed/info", headers=headers)
        if response.status_code == 200:
            jsonStockList = response.json().get("info")
            stockList = [
                Stock(
                    date=stock["Date"],
                    code=stock["Code"],
                    companyName=stock["CompanyName"],
                    companyNameEnglish=stock["CompanyNameEnglish"],
                    sector17Code=stock["Sector17Code"],
                    sector33Code=stock["Sector33Code"],
                    scaleCategory=stock["ScaleCategory"],
                    marketCode=stock["MarketCode"]
                ) for stock in jsonStockList]
            return stockList
        else:
            self.error_handler(response)

    def get_daily_quants(self, idToken: str, date: datetime) -> List[DailyQuants]:
        headers = {'Authorization': 'Bearer {}'.format(idToken)}
        request_url = self.api + \
            "prices/daily_quotes?date={}".format(date.strftime("%Y%m%d"))
        print(request_url)
        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            jsonDailyQuants = response.json().get("daily_quotes")
            dailyQuantsList = [
                DailyQuants(
                    date=dailyQuants["Date"],
                    code=dailyQuants["Code"],
                    open=dailyQuants["AdjustmentOpen"],
                    high=dailyQuants["AdjustmentHigh"],
                    low=dailyQuants["AdjustmentLow"],
                    close=dailyQuants["AdjustmentClose"],
                    volume=dailyQuants["AdjustmentVolume"]
                ) for dailyQuants in jsonDailyQuants]
            return dailyQuantsList
        else:
            self.error_handler(response)

    def error_handler(self, response: requests.Response) -> None:
        if response.status_code == 403 or response.status_code == 401:
            raise UnauthorizedException(
                f"認証エラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        elif response.status_code >= 400:
            raise Exception(
                f"クライアント側のエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        elif response.status_code >= 500:
            raise Exception(
                f"サーバ側のエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        else:
            raise Exception(
                f"不明なエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
