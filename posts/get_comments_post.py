import os
import json
import boto3
import decimalencoder
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')


def get_post_comments(event, context):
    # print(event)
    # print(event['pathParameters'])
    print("print this ")
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    postId = 'POST#{}#{}'.format(event['pathParameters']['id'],event['pathParameters']['timestamp'])

    print(postId)

    result = table.query(
        KeyConditionExpression=
        Key('PK').eq(postId),
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
