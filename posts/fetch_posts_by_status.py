import os
import json
import boto3
import decimalencoder
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')


def fetch_post(event, context):
    # print(event)
    # print(event['pathParameters'])
    print("print this ")
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    result = table.query(
        IndexName="GSI1",
        KeyConditionExpression=
        Key('status').eq(event['pathParameters']['status']),
        ScanIndexForward=True
    )
    # create a response

    response = {
        "statusCode": 200,
        "body": json.dumps(result["Items"],
                           cls=decimalencoder.DecimalEncoder)

    }
    print(response)
    print("Query successful.")
    return response
