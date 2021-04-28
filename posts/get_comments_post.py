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
    comments_list = []
    postId = 'POST#{}'.format(event['pathParameters']['id'])

    print(postId)

    result = table.query(
        KeyConditionExpression=
        Key('PK').eq(postId) & Key('SK').between(postId, 'COMMENT$'),
        ScanIndexForward=True
    )
    # create a response

    posts_list = result["Items"][1:]
    print(posts_list)
    for post in posts_list:
        post.update((k, v.replace("POST#", "")) for k, v in post.items() if k == "PK")
        post.update((k, v.replace("COMMENT#", "")) for k, v in post.items() if k == "SK")

    response = {
        "statusCode": 200,
        "body": json.dumps(result["Items"],
                           cls=decimalencoder.DecimalEncoder)

    }
    print(response)
    print("Query successful.")
    return response
