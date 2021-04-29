import os
import json
import boto3
import decimalencoder
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')


def fetch_user_and_posts(event, context):
    # print(event)
    # print(event['pathParameters'])
    print("print this ")
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    posts_list = []
    userId = 'USER#{}'.format(event['pathParameters']['id'])
    metadata = 'METADATA#{}'.format(event['pathParameters']['id'])
    print(userId)
    print(metadata)
    result = table.query(
        KeyConditionExpression=
        Key('PK').eq(userId) & Key('SK').between(metadata, 'POST$'),
        ScanIndexForward=True
    )
    # create a response

    posts_list = result["Items"][1:]
    for post in posts_list:
        post.update((k, v.replace("POST#", "")) for k, v in post.items() if k == "SK")
        post.update((k, v.replace("USER#", "")) for k, v in post.items() if k == "PK")

    response = {
        "statusCode": 200,
        "body": json.dumps(result["Items"],
                           cls=decimalencoder.DecimalEncoder)

    }
    print(response)
    print("Query successful.")
    return response
