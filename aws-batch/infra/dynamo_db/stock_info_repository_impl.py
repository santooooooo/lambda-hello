from xmlrpc.client import Boolean
from ...domain.repository.dynamo_db.stock_info_repository import StockInfoRepository
from typing import List
from ...domain.model.stock import Stock
import boto3
from botocore.exceptions import ClientError
from ...domain.either import Either, Left, Right


class StockInfoRepositoryImpl(StockInfoRepository):
    table_name: str = ''

    def __init__(self, isTest: str) -> None:
        self.table_name = 'StockInfo'
        isLocal = isTest == 'True'
        print(f"Local DynamoDB: {isLocal}")
        if isLocal:
            self.dynamo_db = boto3.client('dynamodb', endpoint_url='http://host.docker.internal:8000/',
                                          region_name='ap-northeast-1', aws_access_key_id='dummy', aws_secret_access_key='dummy')
        else:
            self.dynamo_db = boto3.client('dynamodb')

    def create_table_if_not_exists(self) -> None:
        """テーブルが存在しない場合にテーブルを作成する"""
        is_exists = self.table_exists()
        is_exists.fold(
            lambda _: self.create_table(),
            lambda _: None
        )

    def create_table(self) -> None:
        table_params = {
            'TableName': self.table_name,
            'KeySchema': [
                {
                    'AttributeName': 'code',
                    'KeyType': 'HASH'
                },
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'code',
                    'AttributeType': 'S'
                },
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
        }

        try:
            print(f"{self.table_name} テーブルを作成します。")
            self.dynamo_db.create_table(**table_params)
            waiter = self.dynamo_db.get_waiter('table_exists')
            waiter.wait(TableName=self.table_name, WaiterConfig={
                        'Delay': 5, 'MaxAttempts': 20})
            print(f"{self.table_name}テーブルが作成されました。")
        except ClientError as e:
            raise Exception(f"Unexpected error: {e}")

    def table_exists(self) -> Either[None, None]:
        try:
            response = self.dynamo_db.describe_table(TableName=self.table_name)
            print(f"{self.table_name} は存在するため、新規テーブルの作成は実行されません。")
            return Right(None)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"{self.table_name}は存在しないため、新規テーブルの作成を実行します.")
                return Left(None)
            else:
                raise Exception(f"Unexpected error: {e}")

    def get_stock_info_list(self) -> List[Stock]:
        """株式情報をDynamoDBから取得する

        Args:
            code (List[str], optional): 特定のコードの株式情報のみを取得する場合のコードリスト

        Returns:
            List[Stock]: 取得した株式情報のリスト
        """

        # 全株式情報を取得
        response = self.dynamo_db.scan(TableName=self.table_name)
        items = response.get('Items', [])

        # DynamoDBのアイテムをStockオブジェクトに変換
        stock_list = []
        for item in items:
            stock = Stock(
                code=item['code']['S'],
                companyName=item['companyName']['S'],
                companyNameEnglish=item['companyNameEnglish']['S'],
                date=item['date']['S'],
                marketCode=item['marketCode']['S'],
                sector17Code=item['sector17Code']['S'],
                sector33Code=item['sector33Code']['S'],
                scaleCategory=item['scaleCategory']['S']
            )
            stock_list.append(stock)

        return stock_list

    def insert_stock_info(self, stock_list: List[Stock]) -> None:
        """株式情報をDynamoDBに保存する
        Args:
            stock_list (List[Stock]): 保存する株式情報のリスト
        Returns:
            None: 保存が完了したことを示す
        """
        for stock in stock_list:
            self.dynamo_db.put_item(
                TableName=self.table_name,
                Item={
                    'code': {'S': stock.code},
                    'companyName': {'S': stock.companyName},
                    'companyNameEnglish': {'S': stock.companyNameEnglish},
                    'date': {'S': stock.date},
                    'marketCode': {'S': stock.marketCode},
                    'sector17Code': {'S': stock.sector17Code},
                    'sector33Code': {'S': stock.sector33Code},
                    'scaleCategory': {'S': stock.scaleCategory},
                }
            )
