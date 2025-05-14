from xmlrpc.client import Boolean
from ...domain.repository.dynamo_db.stock_info_repository import StockInfoRepository
from typing import List
from ...domain.model.stock import Stock
import boto3
from botocore.exceptions import ClientError
from ...domain.either import Either, Left, Right

class StockInfoRepositoryImpl(StockInfoRepository):
    dynamo_db = None
    table_name: str = ''

    def __init__(self, isTest: str) -> None:
        self.table_name = 'StockInfo'
        isLocal = isTest == 'True'
        print(f"Local DynamoDB: {isLocal}")
        if isLocal:
            self.dynamo_db = boto3.client('dynamodb', endpoint_url='http://host.docker.internal:8000/', region_name='ap-northeast-1', aws_access_key_id='dummy', aws_secret_access_key='dummy')
        else:
            self.dynamo_db = boto3.client('dynamodb')

    def create_table_if_not_exists(self) -> None:
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
            waiter.wait(TableName=self.table_name, WaiterConfig={'Delay': 5, 'MaxAttempts': 20})
            print(f"{self.table_name}テーブルが作成されました。")
        except ClientError as e:
            raise Exception(f"Unexpected error: {e}")

    def table_exists(self) -> Either[None, None]:
        try:
            response = self.dynamo_db.describe_table(TableName = self.table_name)
            print(f"{self.table_name} は存在するため、新規テーブルの作成は実行されません。")
            print(f"Table status: {response['Table']['TableStatus']}")
            return Right(None)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"{self.table_name}は存在しないため、新規テーブルの作成を実行します.")
                return Left(None)
            else:
                raise Exception(f"Unexpected error: {e}")

    def get_stock_info_list(self, code: List[str]) -> List[Stock]:
        pass

    def insert_stock_info(self, stock_list: List[Stock]) -> float:
        pass
