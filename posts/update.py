import json
import logging
import os
import time
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')


def update_post(event, context):
    data = json.loads(event['body'])
    if 'status' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the post")

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['TABLE_NAME'])

    # write the post to the database
    item = table.update_item(
        Key={
            'PK': "USER#{}".format(data['userId']),
            'SK': "POST#{}#{}".format(event['pathParameters']['id'],data['timestamp'])


        },
        ExpressionAttributeNames={
            "#pt": 'postText',
            '#st': 'status',

        },
        ExpressionAttributeValues={
            ':postText': data['postText'],
            ':status': data['status'],
            ':updatedAt': timestamp,
        },
        UpdateExpression='SET #pt = :postText,#st=:status, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,

        "body": json.dumps(item["Attributes"])
    }

    return response
