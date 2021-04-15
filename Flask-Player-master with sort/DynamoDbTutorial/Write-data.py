import boto3


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Albums')


with table.batch_writer() as batch:
    batch.put_item(Item={"Artist": " ", "Title": " ", "Album_Cover" = " ", "Genre" = " ", "Year" = " "})
