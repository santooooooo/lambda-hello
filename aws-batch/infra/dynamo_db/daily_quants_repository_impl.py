import datetime
from ...domain.repository.dynamo_db.daliy_quants_repository import DailyQuantsRepository
from typing import List
from ...domain.model.daily_quants import DailyQuants
import boto3
from botocore.exceptions import ClientError
from ...domain.either import Either, Left, Right
from datetime import datetime, timedelta
from decimal import Decimal


class DailyQuantsRepositoryImpl(DailyQuantsRepository):
    table_name: str = ''

    def __init__(self, isTest: str) -> None:
        self.table_name = 'DailyQuants'
        isLocal = isTest == 'True'
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
        """テーブルを作成する"""
        table_params = {
            'TableName': self.table_name,
            'KeySchema': [
                {
                    'AttributeName': 'date',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'code',
                    'KeyType': 'RANGE'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'date',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'code',
                    'AttributeType': 'S'
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 2
            },
        }

        try:
            print(f"{self.table_name} テーブルを作成します。")
            self.dynamo_db.create_table(**table_params)
            waiter = self.dynamo_db.get_waiter('table_exists')
            waiter.wait(TableName=self.table_name, WaiterConfig={
                        'Delay': 5, 'MaxAttempts': 20})
            print(f"{self.table_name} テーブルを作成しました。")
        except ClientError as e:
            raise Exception(f"Unexpected error: {e}")

    def table_exists(self) -> Either[None, None]:
        """テーブルが存在するかどうかを確認する
        Returns:
            Either[None, None]: テーブルが存在する場合はRight(None)、存在しない場合はLeft(None)
        """
        try:
            response = self.dynamo_db.describe_table(
                TableName=self.table_name)
            print(f"{self.table_name} は存在するため、新規テーブルの作成は実行されません。")
            return Right(None)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print(f"{self.table_name}は存在しないため、新規テーブルの作成を実行します.")
                return Left(None)
            else:
                raise Exception(f"Unexpected error: {e}")

    def insert_daily_quants(self, daily_quants: List[DailyQuants], target_date: datetime) -> None:
        """データを挿入する"""
        is_exists = self.check_if_today_date_exists(target_date)
        is_exists.fold(
            lambda _: self.insert_daily_quants_to_dynamo_db(daily_quants),
            lambda _: None
        )

    def check_if_today_date_exists(self, date: datetime) -> Either[None, None]:
        """今日のデータが存在するかどうかを確認する
        Returns:
            bool: 今日のデータが存在する場合はTrue、存在しない場合はFalse
        """
        try:
            response = self.dynamo_db.query(
                TableName=self.table_name,
                KeyConditionExpression='#date = :date',
                ExpressionAttributeNames={
                    '#date': 'date'
                },
                ExpressionAttributeValues={
                    ':date': {'S': date.strftime('%Y%m%d')}
                }
            )
            return Right(None) if response['Count'] > 0 else Left(None)
        except ClientError as e:
            raise Exception(f"Unexpected error: {e}")

    def insert_daily_quants_to_dynamo_db(self, daily_quants: List[DailyQuants]) -> None:
        """データをDynamoDBに挿入する"""
        for daily_quant in daily_quants:
            self.dynamo_db.put_item(
                TableName=self.table_name,
                Item={
                    'date': {'S': daily_quant.date},
                    'code': {'S': daily_quant.code},
                    'open': {'N': self.none_to_zero(daily_quant.open)},
                    'high': {'N': self.none_to_zero(daily_quant.high)},
                    'low': {'N': self.none_to_zero(daily_quant.low)},
                    'close': {'N': self.none_to_zero(daily_quant.close)},
                    'volume': {'N': self.none_to_zero(daily_quant.volume)},
                }
            )

    def none_to_zero(self, value: float) -> str:
        return '0.0' if value is None else str(round(value, 2))
