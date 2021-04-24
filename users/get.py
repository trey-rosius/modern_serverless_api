import os
import json
import boto3
import decimalencoder
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')


def get_user(event, context):
    # print(event)
    print(event['pathParameters'])
    print("print this ")
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    userId = "USER#{}".format(event['pathParameters']['id'])
    metaId = "METADATA#{}".format(event['pathParameters']['id'])
    print(userId)
    print(metaId)

    # fetch user from the database
    result = table.get_item(
        Key={
            'PK': userId,
            'SK': metaId
        }
    )

    print(result)
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)

    }
    return response
