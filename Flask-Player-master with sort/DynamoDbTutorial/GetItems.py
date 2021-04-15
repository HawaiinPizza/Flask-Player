import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Albums')

resp = table.get_item(Key={"Artist": "Saba", "Title": "CARE FOR ME"})
print(resp['Item'])

resp = table.get_item(Key={"Artist": "Saba", "Title": "Bucket List Project"})
print(resp['Item'])

resp = table.get_item(Key={"Artist": "Chance The Rapper", "Title": "Coloring Book"})
print(resp['Item'])

