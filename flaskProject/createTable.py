import boto3
client = boto3.client('dynamodb', region_name='us-east-1')

if( "Albums" not in client.list_tables()["TableNames"]):
    try:
        resp = client.create_table(
            TableName = "Albums",

            KeySchema =[
                {
                    "AttributeName": "Artist",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName": "Title",
                    "KeyType": "RANGE"
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "Artist",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "Title",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            }
        )
        print("Table Created Successfully!")
    except Exception as e:
        print("Error creating table: ")
        print(e)
else:
    print("Tables already created.")
