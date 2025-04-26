import os
from dotenv import load_dotenv
from .usecase import get_jquants_temporary_token_service
from .usecase import get_stock_list_service

print("Hello from Fargate!!")

# 環境変数の読み込み
load_dotenv()
email = os.environ.get("JQUANTS_EMAIL")
password = os.environ.get("JQUANTS_PASSWORD")

getJquantsTemporaryTokenService = get_jquants_temporary_token_service.GetJquantsTemporaryTokenService()
getStockListService = get_stock_list_service.GetStockListService()

# jquantsのAPIにPOSTリクエストを送信し、認証用トークンを取得
token = getJquantsTemporaryTokenService.get_token(email, password)
print(token)

idToken = getJquantsTemporaryTokenService.get_id_token(token)
print(idToken)

# 上場銘柄一覧を取得
stockList = getStockListService.get(idToken)
print(stockList)

# 上場銘柄一覧を保存
