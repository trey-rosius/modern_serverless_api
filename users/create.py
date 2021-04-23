import json
import logging
import os
import time
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')


def create_user(event, context):
    data = json.loads(event['body'])
    if 'firstName' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the user ")

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['TABLE_NAME'])

    item = {
        'userId': str(uuid.uuid1()),
        'firstName': data['firstName'],
        "lastName": data['lastName'],
        'profilePicture': data['profilePicture'],
        'age': data['age'],
        'emailAddress': data['emailAddress'],
        'createdOn': timestamp,

    }

    # write the review to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,

        "body": json.dumps(item)
    }

    return response
