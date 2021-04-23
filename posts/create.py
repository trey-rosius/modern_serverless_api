import json
import logging
import os
import time
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')


def create_post(event, context):
    data = json.loads(event['body'])
    if 'postText' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the post")

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['TABLE_NAME'])

    item = {
        'PK': "POST#{}".format(str(uuid.uuid1())),
        'SK': "USER#{}".format(data['userId']),
        'postText': data['postText'],
        'postImgUrl': data['postImgUrl'],
        'status': data['status'],
        'createdOn': timestamp

    }

    # write the post to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,

        "body": json.dumps(item)
    }

    return response
