import boto3

def delete_instances(instance_ids):
    ec2 = boto3.client('ec2')
    ec2.terminate_instances(InstanceIds=instance_ids)

def remove_instance_data(instance_ids):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('InstanceInfo')
    for instance_id in instance_ids:
        table.delete_item(Key={'InstanceId': instance_id})

instance_ids = ['i-0abcd1234efgh5678', 'i-0abcd1234efgh5679']  # Replace with your instance IDs
delete_instances(instance_ids)
remove_instance_data(instance_ids)
