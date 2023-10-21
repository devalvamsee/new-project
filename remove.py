import boto3

def delete_instances(instance_ids):
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    response = ec2.terminate_instances(InstanceIds=instance_ids)
    return response['TerminatingInstances']

def remove_instance_data(instance_ids):
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('InstanceInfo')
    
    for instance_id in instance_ids:
        response = table.delete_item(
            Key={
                'InstanceId': instance_id
            }
        )
        # Optionally check response for errors
        # print(response)

try:
    # Replace with the actual instance IDs you want to delete
    instance_ids_to_delete = ['i-0abcd1234efgh5678', 'i-0abcd1234efgh5679']
    deleted_instances = delete_instances(instance_ids_to_delete)
    remove_instance_data(instance_ids_to_delete)
except Exception as e:
    print(f"An error occurred: {e}")
