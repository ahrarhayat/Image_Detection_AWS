import json
import boto3

TABLE_NAME = 'IMAGE_URL'

def add_tag(event, context):
    db_resource = boto3.resource('dynamodb')
    table = db_resource.Table(TABLE_NAME) 
    data = json.loads(event['body'])

    if data['url'] is not None:
        tags = data['tags']
        url = data['url']

        try:
            response = table.update_item(
                Key={
                    'url_list': url
                },
                UpdateExpression='ADD tags :t',
                ExpressionAttributeValues={
                    ':t': set(tags)
                },
                ReturnValues='UPDATED_NEW'
            )
            
            print(response)
            return{
                'statusCode': 200,
                "headers": {
                    'Access-Control-Allow-Origin': '*'
                }
            }
        except Exception as e:
            print(e)
        return{
            'statusCode': 500,
            "headers": {
                'Access-Control-Allow-Origin': '*'
            }
        }
            

def lambda_handler(event, context):
    
    print(event)
    
    if event['httpMethod'] == 'POST':
        return add_tag(event, context)

    else:
        return{
            'statusCode': 200,
            "headers": {
                'Access-Control-Allow-Origin': '*'
            }
        }


