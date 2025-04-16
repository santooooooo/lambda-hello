from typing import List
import requests
import json
from ..http_status_exception.bad_request_exception import BadRequestException
from ...domain.repository.jquants import JquantsRepository
from ..http_status_exception.unauthorized_exception import UnauthorizedException
from ...domain.model.stock import Stock

class JquantsRepositoryImpl(JquantsRepository):
    api: str = ""
    def __init__(self):
        self.api = "https://api.jquants.com/v1/"

    def get_refresh_token(self, email: str, password: str) -> str:
        data={"mailaddress":email, "password":password}
        response = requests.post(self.api+"token/auth_user", data=json.dumps(data))
        if response.status_code == 200:
            return response.json().get("refreshToken")
        elif response.status_code == 403 or response.status_code == 401:
            raise UnauthorizedException(f"認証エラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        elif response.status_code >= 400:
            raise Exception(f"クライアント側のエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        elif response.status_code >= 500:
            raise Exception(f"サーバ側のエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        else:
            raise Exception(f"不明なエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")


    def get_id_token(self, refreshToken: str) -> str:
        response = requests.post(self.api + f"token/auth_refresh?refreshtoken={refreshToken}")
        if response.status_code == 200:
            return response.json().get("idToken")
        elif response.status_code == 403 or response.status_code == 401:
            raise UnauthorizedException(f"認証エラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        elif response.status_code >= 400:
            raise Exception(f"クライアント側のエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        elif response.status_code >= 500:
            raise Exception(f"サーバ側のエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        else:
            raise Exception(f"不明なエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")


    def get_stock_list(self, idToken: str) -> List[Stock]:
        headers = {'Authorization': 'Bearer {}'.format(idToken)}
        response = requests.get(self.api+"listed/info", headers=headers)
        if response.status_code == 200:
            jsonStockList = response.json().get("info")
            stockList = [
                Stock(
                date = stock["Date"], 
                code=stock["Code"], 
                companyName=stock["CompanyName"],
                companyNameEnglish=stock["CompanyNameEnglish"],
                sector17Code=stock["Sector17Code"],
                sector33Code=stock["Sector33Code"],
                scaleCategory=stock["ScaleCategory"],
                marketCode=stock["MarketCode"]
                ) for stock in jsonStockList]
            return stockList
        elif response.status_code == 403 or response.status_code == 401:
            raise UnauthorizedException(f"認証エラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        elif response.status_code >= 400:
            raise Exception(f"クライアント側のエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        elif response.status_code >= 500:
            raise Exception(f"サーバ側のエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
        else:
            raise Exception(f"不明なエラーです。エラー内容は以下の通りです\nステータスコード {response.status_code} \n エラー内容 {response.json().get('message')}")
