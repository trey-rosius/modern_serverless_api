import json
import logging
import os
import time
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')


def create_comment(event, context):
    data = json.loads(event['body'])
    if 'commentText' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create a comment")

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['TABLE_NAME'])

    item = {
        'PK': "POST#{}#{}".format(data['postId'],data['timestamp']),
        'SK': "COMMENT#{}#{}".format(str(uuid.uuid1()),timestamp),
        'commentId': str(uuid.uuid1()),
        'postId': data['postId'],
        'userId': data['userId'],
        'commentText': data['commentText'],
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
