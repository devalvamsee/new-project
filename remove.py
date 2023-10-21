import boto3

def get_instance_ids(name_prefix):
    ec2 = boto3.resource('ec2', region_name='ap-south-1')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': [f'{name_prefix}*']}]
    )
    return [instance.instance_id for instance in instances]

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

try:
    name_prefix = 'app-instance'  # Replace with your actual name prefix
    instance_ids_to_delete = get_instance_ids(name_prefix)
    if instance_ids_to_delete:
        deleted_instances = delete_instances(instance_ids_to_delete)
        remove_instance_data(instance_ids_to_delete)
    else:
        print(f"No instances found with name prefix: {name_prefix}")
except Exception as e:
    print(f"An error occurred: {e}")
