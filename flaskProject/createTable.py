import boto3
client = boto3.client('dynamodb', region_name='us-east-1')

if( "Albums" not in client.list_tables()["TableNames"]):
    try:
        resp = client.create_table(
            TableName = "Albums",

            KeySchema =[
                {
                    "AttributeName": "Album",
                    "KeyType": "HASH"
                },
                {
                    "AttributeName": "Artist",
                    "KeyType": "RANGE"
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "Album",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "Artist",
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
