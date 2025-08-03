import os
from dotenv import load_dotenv
from .usecase import get_jquants_temporary_token_service, get_stock_list_service, insert_stock_info_list_service, get_daily_quants_service, insert_daily_quants_list_service

print("Hello from Fargate!!")

# 環境変数の読み込み
load_dotenv()
email = os.environ.get("JQUANTS_EMAIL")
password = os.environ.get("JQUANTS_PASSWORD")
is_test = os.environ.get("IS_TEST")

if email is None or password is None or is_test is None:
    print("JQUANTS_EMAIL, JQUANTS_PASSWORD, または IS_TEST が設定されていません")
    exit(1)

# jquantsのAPIにPOSTリクエストを送信し、認証用トークンを取得
getJquantsTemporaryTokenService = get_jquants_temporary_token_service.GetJquantsTemporaryTokenService()
token = getJquantsTemporaryTokenService.get_token(email, password)

idToken = getJquantsTemporaryTokenService.get_id_token(token)

# 上場銘柄一覧を取得
getStockListService = get_stock_list_service.GetStockListService()
stockList = getStockListService.get(idToken)

# 上場銘柄一覧を保存
print("上場銘柄一覧を保存します")
insertStockInfoListService = insert_stock_info_list_service.InsertStockInfoListService(
    isTest=is_test)
insertStockInfoListService.insert(stockList)

# 株式四本値を取得
getDailyQuantsService = get_daily_quants_service.GetDailyQuantsService()
dailyQuantsList = getDailyQuantsService.get(idToken)
print(dailyQuantsList)

print("株式四本値を保存します")
insertDailyQuantsListService = insert_daily_quants_list_service.InsertDailyQuantsListService(
    isTest=is_test)
insertDailyQuantsListService.insert(dailyQuantsList)
